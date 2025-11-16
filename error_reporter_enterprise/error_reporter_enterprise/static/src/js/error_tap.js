/** @odoo-module **/

/**
 * Client-side error tap for Odoo pages
 * - Fetches QA token from /qa/errors/token (auth=user)
 * - Listens for window.onerror and unhandledrejection
 * - Computes a simple fingerprint and rate-limits posts (1 per 5s per fingerprint)
 * - Posts JSON payload to /qa/errors/ingest with header X-QA-TOKEN
 */

const RATE_LIMIT_MS = 5000; // 5 seconds per fingerprint
const MAX_MESSAGE_LENGTH = 5000; // Maximum message length
const recent = {}; // fingerprint -> lastSent timestamp
let QA_TOKEN = null;
let tokenFetchAttempted = false;

function now() { 
    return (new Date()).getTime(); 
}

function truncateMessage(message, maxLength = MAX_MESSAGE_LENGTH) {
    if (!message || message.length <= maxLength) {
        return message;
    }
    return message.substring(0, maxLength - 3) + '...';
}

function simpleFingerprint(source, scenario, url, message) {
    // lightweight fingerprint: first line + url + source
    const first = (message || '').split('\n')[0] || '';
    const key = source + '|' + scenario + '|' + url + '|' + first;
    try {
        return btoa(encodeURIComponent(key)).slice(0, 64);
    } catch (e) {
        // Fallback for invalid characters
        return btoa(key.replace(/[^\x00-\x7F]/g, "")).slice(0, 64);
    }
}

function rateAllow(fp) {
    const t = now();
    if (!recent[fp] || (t - recent[fp]) > RATE_LIMIT_MS) {
        recent[fp] = t;
        return true;
    }
    return false;
}

async function postEvent(payload) {
    if (!QA_TOKEN && !tokenFetchAttempted) {
        tokenFetchAttempted = true;
        // try to fetch token once
        try {
            const resp = await fetch('/qa/errors/token', { 
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin' 
            });
            if (resp && resp.ok) {
                const json = await resp.json();
                if (json && json.token) {
                    QA_TOKEN = json.token;
                } else if (json && json.error) {
                    console.warn('QA Error Reporter: Token fetch failed -', json.error);
                }
            }
        } catch (e) {
            console.warn('QA Error Reporter: Token fetch failed', e);
        }
    }

    // If still no token, skip (we don't want to expose a public ingest path)
    if (!QA_TOKEN) return;

    try {
        const response = await fetch('/qa/errors/ingest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-QA-TOKEN': QA_TOKEN,
            },
            body: JSON.stringify(payload),
        });
        
        if (!response.ok) {
            console.warn('QA error post failed with status:', response.status);
        }
    } catch (e) {
        // swallow network errors
        console.warn('QA error post failed', e);
    }
}

function sendIfAllowed(source, message, details, extra) {
    const url = (window.location && window.location.href) || extra.url || '';
    const scenario = extra.scenario || '';
    
    // Truncate message if too long
    const truncatedMessage = truncateMessage(message);
    const truncatedDetails = truncateMessage(details);
    
    const fp = simpleFingerprint(source, scenario, url, truncatedMessage);
    if (!rateAllow(fp)) return;

    // Get user info safely
    let userLogin = '';
    try {
        if (window.odoo && window.odoo.session_info && window.odoo.session_info.uid) {
            userLogin = String(window.odoo.session_info.uid);
        }
    } catch (e) {
        // ignore user detection errors
    }

    const payload = {
        source: source,
        severity: extra.severity || 'error',
        project: extra.project || '',
        scenario: scenario,
        user_login: userLogin,
        url: url,
        browser: navigator.userAgent || '',
        trace_url: extra.trace_url || '',
        message: truncatedMessage,
        details: truncatedDetails || '',
        tags: extra.tags || '',
    };

    postEvent(payload);
}

// JS error
window.addEventListener('error', function (event) {
    try {
        const msg = event && event.message ? event.message : String(event);
        let details = '';
        if (event && event.error && event.error.stack) {
            details = event.error.stack;
        } else if (event && event.filename && event.lineno) {
            details = `at ${event.filename}:${event.lineno}:${event.colno || 0}`;
        }
        sendIfAllowed('odoo_ui', msg, details, {});
    } catch (e) { 
        // ignore errors in error handling
    }
});

// Promise rejection
window.addEventListener('unhandledrejection', function (ev) {
    try {
        let msg = 'Unhandled Promise Rejection';
        let details = '';
        if (ev && ev.reason) {
            if (ev.reason instanceof Error) {
                msg = ev.reason.message || msg;
                details = ev.reason.stack || String(ev.reason);
            } else {
                msg = String(ev.reason);
                details = String(ev.reason);
            }
        }
        sendIfAllowed('odoo_ui', msg, details, {});
    } catch (e) { 
        // ignore errors in error handling
    }
});

// expose a manual reporter for tests or other scripts
window.QAErrorReporter = {
    report: function (message, details, opts) {
        try {
            const options = opts || {};
            const source = options.source || 'odoo_ui';
            sendIfAllowed(source, message, details, options);
        } catch (e) {
            // ignore errors in manual reporting
        }
    },
    
    // Utility to check if reporting is available
    isAvailable: function () {
        return !!QA_TOKEN || !tokenFetchAttempted;
    }
};
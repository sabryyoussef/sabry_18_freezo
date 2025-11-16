/* 
Error Reporter Demo Script
Run this in your browser console on any Odoo page to test error reporting
*/

console.log('🚀 Testing Error Reporter Module...');

// Test 1: Check if QAErrorReporter is available
if (typeof window.QAErrorReporter !== 'undefined') {
    console.log('✓ QAErrorReporter is available');
    
    // Test 2: Check if reporting is available
    if (window.QAErrorReporter.isAvailable()) {
        console.log('✓ Error reporting is ready');
        
        // Test 3: Report a demo error
        window.QAErrorReporter.report(
            'Demo Error: Testing error reporting functionality',
            'This is a test error generated from browser console to verify the error reporting system is working correctly.\n\nStack trace:\n  at TestFunction (console:1:1)\n  at <anonymous>:1:1',
            {
                source: 'odoo_ui',
                severity: 'info',
                project: 'Error Reporter Demo',
                scenario: 'Manual Testing',
                tags: 'demo,test,console'
            }
        );
        
        console.log('✓ Demo error reported successfully!');
        console.log('📊 Check Error Reporter → Error Events to see the new error');
        
        // Test 4: Report different severity levels
        setTimeout(() => {
            window.QAErrorReporter.report(
                'Demo Warning: This is a warning level test',
                'Warning level error for demonstration purposes',
                { severity: 'warning', project: 'Demo Module', scenario: 'Warning Test' }
            );
        }, 1000);
        
        setTimeout(() => {
            window.QAErrorReporter.report(
                'Demo Error: This is an error level test', 
                'Error level for demonstration purposes',
                { severity: 'error', project: 'Demo Module', scenario: 'Error Test' }
            );
        }, 2000);
        
        console.log('🎯 Multiple demo errors will be reported over the next few seconds');
        
    } else {
        console.log('❌ Error reporting not available (token not configured or other issue)');
    }
} else {
    console.log('❌ QAErrorReporter not found. Make sure the Error Reporter module is installed and the page is loaded correctly.');
}

// Test 5: Generate a real JavaScript error for testing
setTimeout(() => {
    console.log('🧪 Generating a real JavaScript error for testing...');
    try {
        // This will cause a real error
        var testObj = null;
        testObj.nonExistentProperty.someMethod();
    } catch (e) {
        console.log('✓ JavaScript error generated and should be automatically captured');
        console.log('Error was:', e.message);
    }
}, 3000);

console.log('🔍 Open Error Reporter → Error Events to see all the demo errors that were created');
console.log('📈 Also check Error Reporter → Analytics for visual representation');
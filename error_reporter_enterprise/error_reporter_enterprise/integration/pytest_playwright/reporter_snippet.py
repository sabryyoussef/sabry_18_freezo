def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        # Extract necessary information for the error report
        scenario = item.nodeid
        page_url = item.config.getoption("base_url") + item.config.getoption("path")
        trace_url = item.config.getoption("trace_url")
        
        # Build the payload
        payload = {
            "source": "playwright",
            "message": str(call.excinfo.value),
            "severity": "error",
            "project": item.config.getoption("project_name"),
            "scenario": scenario,
            "user_login": item.config.getoption("user_login"),
            "url": page_url,
            "browser": item.config.getoption("browser"),
            "trace_url": trace_url,
        }
        
        # Send the error report to the ingest endpoint
        import requests
        import os
        
        api_token = os.getenv("QA_ERROR_TOKEN")
        response = requests.post(
            f"{os.getenv('QA_ERROR_ENDPOINT')}/qa/errors/ingest",
            json=payload,
            headers={"X-QA-TOKEN": api_token}
        )
        
        if response.status_code != 200:
            print(f"Failed to report error: {response.text}")
def process_alert_data(data):
    """
    Process the AlertManager payload and extract key fields:
    - alertname
    - severity
    - ruleSource
    - summary
    Returns a formatted message string for Teams.
    """
    if not data or 'alerts' not in data or not data['alerts']:
        return "No valid alerts found in the payload."
    
    # Assume first alert for simplicity; extend for multiples if needed
    alert = data['alerts'][0]
    labels = alert.get('labels', {})
    annotations = alert.get('annotations', {})
    
    alertname = labels.get('alertname', 'Unknown Alert')
    severity = labels.get('severity', 'Unknown')
    rule_source = labels.get('ruleSource', 'Unknown Rule Source')
    summary = annotations.get('summary', 'No summary available')
    
    # Format the message for Teams (Markdown-friendly)
    formatted_message = f"""
    Alert Name: {alertname}
    Severity: {severity}
    Rule Source: {rule_source}
    Summary: {summary}
    Status: {data.get('status', 'Unknown')}"""
    
    return formatted_message
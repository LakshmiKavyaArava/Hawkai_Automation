import requests
from config.config import SNOW_API_URL, SNOW_API_USER, SNOW_API_PASS

def create_incident():
    payload = {
                "operation": "insert",
                "sys_id": "fa5c340946987625423k99h5h38htde32h7",
                "domain": "Juno Labs",
                "number": "INC010099858",
                "task_effective_number": "INC010099858",
                "short_description": "Low disk space alert – manual cleanup of backup files required.",
                "description": "The Windows server is experiencing low disk space due to accumulation of backup files on the D drive. Manual cleanup is required to delete obsolete backups as per retention policy, restore available storage, and clear disk utilization alerts while ensuring no impact to active backups or applications.",
                "state": "1",
                "incident_state": "1",
                "priority": "4",
                "urgency": "2",
                "impact": "3",
                "severity": "3",
                "active": "true",
                "opened_by": "Lakshmi Kavya Arava",
                "caller_id": "Juno Labs Integration User",
                "assigned_to": "",
                "assignment_group": "",
                "company": "Juno",
                "category": "Monitoring",
                "subcategory": "Backup Failure",
                "location": "",
                "opened_at": "01/27/2026 08:17:30 AM",
                "sys_created_on": "01/27/2026 08:18:05 AM",
                "sys_created_by": "Lakshmikavya.arava@resolvetech.com",
                "sys_updated_on": "01/27/2026 08:36:14 AM",
                "sys_updated_by": "svc.junolabs.inetgration.user",
                "close_code": "",
                "close_notes": "",
                "closed_at": "",
                "closed_by": "",
                "reopened_by": "",
                "reopened_time": "",
                "work_notes": "",
                "comments": "",
                "comments_and_work_notes": "",
                "approval": "not requested",
                "approval_history": "",
                "watch_list": "",
                "business_service": "",
                "business_impact": "",
                "rfc": "",
                "problem_id": "",
                "parent_incident": "",
                "child_incidents": "",
                "made_sla": "true",
                "notify": "1",
                "origin_id": "",
                "origin_table": "",
                "calendar_duration": "",
                "business_duration": "",
                "time_worked": "",
                "escalation": "",
                "reassignment_count": "",
                "reopen_count": "",
                "sys_mod_count": "1",
                "sys_tags": "",
                "calendar_stc": "",
                "business_stc": "",
                "delivery_plan": "",
                "delivery_task": "",
                "service_offering": "",
                "knowledge": "",
                "universal_request": "",
                "upon_approval": "proceed",
                "upon_reject": "cancel"
                }

    response = requests.post(
        SNOW_API_URL,
        auth=(SNOW_API_USER, SNOW_API_PASS),
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    print("STATUS CODE:", response.status_code)
    print("RAW RESPONSE:", response.text)

    response.raise_for_status()

    data = response.json()
    print("JSON RESPONSE:", data)

    # Return just the incident number from the response
    return data.get('external_ticket_id')  # or data.get('number') if that's the field name
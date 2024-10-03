from custom_modules.schema import *
import json
from custom_modules.lookups import status_id_lookup, severity_id_lookup, asset_id_lookup, ioc_id_lookup

def asset_build(asset_data:dict = {}) -> AssetSchema:
    # Asset Name
    asset = {
        "asset_name"          : asset_data.get("properties",{}).get("friendlyName","Name unable to be parsed"),
        "asset_description"   : asset_data.get("type",""),
        "asset_type_id"       : asset_id_lookup(asset_data.get("kind")),
        "asset_ip"            : "",
        "asset_domain"        : "",
        "asset_tags"          : "",
        "asset_enrichment"    : asset_data
    }
    return validate_data(schema_name='asset', data=asset)

def ioc_build(ioc_data:dict = {}) -> IOCSchema:
    # IOC Name
    ioc = {
        "ioc_value"           : ioc_data.get("properties",{}).get("friendlyName","Name unable to be parsed"),
        "ioc_description"     : f"{ioc_data.get("type","")} -- {ioc_data.get("kind","")}",
        "ioc_tlp_id"          : 1,
        "ioc_type_id"         : ioc_id_lookup(ioc_data.get("kind")),
        "ioc_tags"            : "",
        "ioc_enrichment"      : ioc_data
    }
    return validate_data(schema_name='ioc', data=ioc)


def convert_to_iris_alert (data):
    # Store incident into a variable
    try: 
        incident = data.get("object",{})
        if incident == None:
            raise ValueError(f"Unable to get the incident object")
    except ValueError as e:
        print(f"Value Error: {e}")
        return
    
    # Extract alerts
    try:
        alert_count = incident.get("properties",{}).get("additionalData",{}).get("alertsCount", 0)
        alerts = incident.get("properties",{}).get("alerts",[])
        if len(alerts) != alert_count:
            raise ValueError(f"Unable to get alerts from properties")
    except ValueError as e:
        print(f"Value Error: {e}")
        print(f"Expected {alert_count} alert(s)")

    # Extract Entities
    try: 
        entities = incident.get("properties",{}).get("relatedEntities",[])
        if not entities:
            raise ValueError(f"Unable to get the entities")
    except ValueError as e:
        print(f"Value Error: {e}")


    # Alert Title
    alert_title = incident.get("properties",{}).get("title","Title unable to be Parsed")
    
    # Alert Description and Alert Notes
    alert_description = f"<b>Incident URL: <a target='_blank' href='{incident.get("properties",{}).get("incidentUrl","Url unable to be parsed")}'>{incident.get("properties",{}).get("incidentUrl","Url unable to be parsed")}</a>"
    alert_notes = "<br>Notes:<br>"
    if alerts:
        x = 1
        alert_description += "<br><br><b>Alerts Associated with Incident:<b>"
        for alert in alerts:
            alert_description += f"<br>{x}.{alert.get("properties",{}).get("alertDisplayName","Title unable to be parsed")}"
            alert_description += f"<br>---{alert.get("properties",{}).get("description","Description unable to be parsed")}"
            alert_url = alert.get("properties",{}).get("alertLink",None)
            if alert_url:
                alert_description += f"<br>---<a target='_blank' href='{alert_url}'>{alert.get("properties",{}).get("alertDisplayName","Title unable to be parsed")}</a>"
            remediation = alert.get("properties",{}).get("remediationSteps",[])
            if remediation:
                alert_notes += f"&nbsp;&nbsp;&nbsp;&nbsp; Remediation Steps: {alert.get("properties",{}).get("alertDisplayName","Alert display name unable to be parsed.")}<br>"
                for step in remediation:
                    alert_notes += f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; * {step}<br>"
            else:
                alert_notes += "No Remediation Steps provided"
            x += 1
    # Alert Source
    alert_source_array = incident.get("properties",{}).get("additionalData",{}).get("alertProductNames","Alert sources unable to be parsed")
    alert_source = f"Source(s): {", ".join(set(alert_source_array))}"

    # Alert Source Reference
    alert_source_reference = ""

    # Alert Source Link
    alert_source_link = f"{incident.get("properties",{}).get("incidentUrl","Url unable to be parsed")}"

    # Alert Severity ID
    alert_severity_id = severity_id_lookup(incident.get("properties","Unknown").get("severity","Unknown"))

    # Alert Status ID
    alert_status_id = status_id_lookup(incident.get("properties","Open").get("status","Open"))

    # Alert Context
    alert_context = {
        "SentinelIncidentID" : incident.get("properties","Incident Id unable to be parsed").get("incidentNumber","Incident Id unable to be parsed")
    }

    # Alert Source Event Time
    alert_source_event_time = incident.get("properties", "").get("createdTimeUtc","")

    # Alert Tags
    tags = f"{', '.join(incident.get("properties",{}).get("additionalData",{}).get("tactics",None))}"
    if tags and alerts:
        for alert in alerts:
            tags += f", {', '.join(alert.get("properties",{}).get("tactics",[]))}"
    if tags:
        tags += ", "
    alert_tags = f"{tags}SI-{incident.get("properties","Incident Id unable to be parsed").get("incidentNumber","Incident Id unable to be parsed")}"

    # Alert Assets and IOCs
    alert_assets = []
    alert_iocs = []
    # Assets
    assets_kinds = [
        "Account", 
        "Host", 
        "IoTDevice", 
        "CloudApplication", 
        "Mailbox"
    ]
    # Indicators of Compromise (IOCs)
    indicators_of_compromise_kinds = [
        "AzureResource", 
        "Bookmark", 
        "DnsResolution", 
        "File", 
        "FileHash", 
        "Ip", 
        "MailCluster", 
        "MailMessage", 
        "Malware", 
        "Process", 
        "RegistryKey", 
        "RegistryValue", 
        "SecurityAlert", 
        "SecurityGroup", 
        "SubmissionMail", 
        "Url"
    ]
    entities = incident.get("properties",{}).get('relatedEntities',[])
    for entity in entities:
        if entity.get("kind",None) in assets_kinds:
            alert_assets.append(asset_build(entity))
        elif entity.get("kind",None) in indicators_of_compromise_kinds:
            alert_iocs.append(ioc_build(ioc_data = entity))
        else:
            pass

    # Alert Customer Id
    alert_customer_id = 1

    # Alert Classification Id
    alert_classification_id = 36

    alert = {
        "alert_title"               : alert_title ,
        "alert_description"         : alert_description,    
        "alert_source"              : alert_source,
        "alert_source_ref"          : alert_source_reference,    
        "alert_source_link"         : alert_source_link,    
        "alert_source_content"      : data,        
        "alert_severity_id"         : alert_severity_id,    
        "alert_status_id"           : alert_status_id,    
        "alert_context"             : alert_context,
        "alert_source_event_time"   : alert_source_event_time,            
        "alert_note"                : alert_notes,
        "alert_tags"                : alert_tags,
        "alert_iocs"                : alert_iocs,
        "alert_assets"              : alert_assets,
        "alert_customer_id"         : alert_customer_id,    
        "alert_classification_id"   : alert_classification_id            
    }

    return validate_data('alert', alert)
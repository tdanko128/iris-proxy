#lookups.py

# Severity ID
severity_table = {
    # The key is from sentinel
    "Medium"        : 1,
    "Unspecified"   : 2,
    "Informational" : 3,
    "Low"           : 4,
    "High"          : 5,
    "Critical"      : 6
}
def severity_id_lookup(severity_string: str = "Unknown") -> int:
    """
    Look up the severity ID based on the provided severity string.

    Args:
        severity_string (str): The severity level is derived from
        object.properties.severity. It can be one of the following:
        "High", "Medium", "Low", "Informational", or "Unknown".
        Defaults to "Unknown".

    Returns:
        int: The severity ID corresponding to the severity level,
        or a message indicating an unknown severity level.
    """
    return severity_table.get(severity_string, "Unknown severity level")

# Status ID
status_table = {
    "Active": 2,
    "New"   : 3,
    "Closed": 9
}
def status_id_lookup(status_string: str = "Open") -> int:
    """
    Look up the status ID based on the provided status string.

    Args:
        status_string (str): The status level is derived from 
        object.properties.status. It can be one of the following:
        "Open", "Acknowledged", "Resolved", "Closed", or "Cancelled".
        Defaults to "Open".

    Returns:
        int: The status ID corresponding to the alert status,
        or a message indicating an unknown status level.
    """
    return status_table.get(status_string, "Unknown status level")

# Asset table
asset_table = {
    "Account"           : 1,
    "Host"              : 9,
    "IoTDevice"         : 4,
    "CloudApplication"  : 1,
    "Mailbox"           : 1
}

def asset_id_lookup(asset_string: str = "Open") -> int:
    """
    Look up the status ID based on the provided status string.

    Args:
        asset_string (str): The type of asset to look up.
        It can be one of the following:
        "Account", "Host", "IoTDevice", "CloudApplication", or "Mailbox".
        Defaults to "Account".

    Returns:
        int: The status ID corresponding to the alert status,
        or a message indicating an unknown status level.
    """
    return asset_table.get(asset_string, "Unknown status level")

# Indicators of Compromise (IOC) table
ioc_table = {
    "AzureResource": 96,
    "Bookmark": 96,
    "DnsResolution": 21,
    "File": 37,
    "FileHash": 46,
    "Ip": 76,
    "MailCluster": 28,
    "MailMessage": 28,
    "Malware": 89,
    "Process": 107,
    "RegistryKey": 109,
    "RegistryValue": 109,
    "SecurityAlert": 96,
    "SecurityGroup": 96,
    "SubmissionMail": 28,
    "Url": 141,
    "Other": 96
}

def ioc_id_lookup(ioc_string: str = "Other") -> int:
    """
    Look up the IOC ID based on the provided IOC type string.

    Args:
        ioc_string (str): The type of IOC to look up.
        It can be one of the following:
        "AzureResource", "Bookmark", "DnsResolution", "File", "FileHash", 
        "Ip", "MailCluster", "MailMessage", "Malware", "Process", 
        "RegistryKey", "RegistryValue", "SecurityAlert", "SecurityGroup", 
        "SubmissionMail", or "Url".
        Defaults to "Other".

    Returns:
        int: The IOC ID corresponding to the provided IOC type,
        or a message indicating an unknown IOC type.
    """
    return ioc_table.get(ioc_string, "Unknown IOC type")

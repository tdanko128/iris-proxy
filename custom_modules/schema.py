from marshmallow import Schema, fields, ValidationError

# Define schemas as before
class EnrichmentSchema(Schema):
    free_form_enrichment = fields.Dict(keys=fields.Str(), values=fields.Raw())

class IOCSchema(Schema):
    ioc_value = fields.Str(required=True)
    ioc_description = fields.Str(required=True)
    ioc_tlp_id = fields.Int(required=True)
    ioc_type_id = fields.Int(required=True)
    ioc_tags = fields.Str(required=True)
    ioc_enrichment = fields.Dict(keys=fields.Str(), values=fields.Raw())

class AssetSchema(Schema):
    asset_name = fields.Str(required=True)
    asset_description = fields.Str(required=True)
    asset_type_id = fields.Int(required=True)
    asset_ip = fields.Str(required=True)
    asset_domain = fields.Str()
    asset_tags = fields.Str(required=True)
    asset_enrichment = fields.Dict(keys=fields.Str(), values=fields.Raw())

class AlertSchema(Schema):
    alert_title = fields.Str(required=True)
    alert_description = fields.Str(required=True)
    alert_source = fields.Str(required=True)
    alert_source_ref = fields.Str(required=True)
    alert_source_link = fields.Str(required=True)
    alert_source_content = fields.Dict(keys=fields.Str(), values=fields.Raw())
    alert_severity_id = fields.Int(required=True)
    alert_status_id = fields.Int(required=True)
    alert_context = fields.Dict()
    alert_source_event_time = fields.Str(required=True)
    alert_note = fields.Str(required=True)
    alert_tags = fields.Str(required=True)
    alert_iocs = fields.List(fields.Nested(IOCSchema), required=True)
    alert_assets = fields.List(fields.Nested(AssetSchema), required=True)
    alert_customer_id = fields.Int(required=True)
    alert_classification_id = fields.Int(required=True)

# Schema mapping
SCHEMA_MAP = {
    'alert': AlertSchema,
    'ioc': IOCSchema,
    'asset': AssetSchema
}

# Dynamic validation function
def validate_data(schema_name, data):
    schema_class = SCHEMA_MAP.get(schema_name)
    if schema_class is None:
        raise ValueError(f"Schema '{schema_name}' is not defined.")

    schema = schema_class()
    try:
        result = schema.load(data)
        return result
    except ValidationError as err:
        raise ValueError(f"Validation errors: {err.messages}")



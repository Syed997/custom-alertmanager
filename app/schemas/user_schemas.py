from marshmallow import Schema, fields, validate, ValidationError

def validate_allowed_domain(value):
    allowed_domains = ["robi.com.bd", "reddotdigitalit.com", "axentec.com.bd"]
    if "@" not in value:
        raise ValidationError("Invalid email format.")

    domain = value.split("@")[-1].lower()
    if domain not in allowed_domains:
        raise ValidationError(f"Email domain '{domain}' is not allowed. Allowed domains: {', '.join(allowed_domains)}")

class UserSignUpSchema(Schema):
    mail = fields.Email(
        required=True,
        validate=validate_allowed_domain,
        error_messages={
            "required": "Email is required.",
            "invalid": "Invalid email format."
        }
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=50, error="Password must be between 6 and 50 characters."),
        error_messages={"required": "Password is required."}
    )
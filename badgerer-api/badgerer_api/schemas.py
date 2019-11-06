from marshmallow import Schema, fields


class UserRequestSchema(Schema):
    """Schema for a create user request."""

    first_name = fields.Str(data_key="firstName")
    last_name = fields.Str(data_key="lastName")
    email = fields.Email()
    password = fields.Str()


class UserResponseSchema(Schema):
    id = fields.Integer()
    first_name = fields.Str(data_key="firstName")
    last_name = fields.Str(data_key="lastName")
    email = fields.Email()
    roles = fields.List(fields.String())


class LoginRequestSchema(Schema):
    email = fields.String()
    password = fields.String()

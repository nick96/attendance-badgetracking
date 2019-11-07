"""Schemas for validating requests and serialising models properly."""

from marshmallow import Schema, fields


class UserRequestSchema(Schema):
    """Schema for validating a request containing a user entity."""

    first_name = fields.Str(data_key="firstName")
    last_name = fields.Str(data_key="lastName")
    email = fields.Email()
    password = fields.Str()


class UserResponseSchema(Schema):
    """Schema to for serialising a user entity."""

    id = fields.Integer()
    first_name = fields.Str(data_key="firstName")
    last_name = fields.Str(data_key="lastName")
    email = fields.Email()
    roles = fields.List(fields.String())


class LoginRequestSchema(Schema):
    """Schema for validating a login request."""

    email = fields.String()
    password = fields.String()

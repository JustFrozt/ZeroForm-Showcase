from .extensions import ma
from .models import User, Note
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)


class NoteSchema(ma.SQLAlchemyAutoSchema):
    user_id = fields.Int(dump_only=True)

    class Meta:
        model = Note
        load_instance = True
        include_relationships = True
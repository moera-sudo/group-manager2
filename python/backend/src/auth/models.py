from tortoise import fields
from tortoise.models import Model
import uuid 


class User(Model):

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    telegram_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=64, null=True)
    first_name = fields.CharField(max_length=128)
    last_name = fields.CharField(max_length=128, null=True)
    lang_code = fields.CharField(max_length=8, null=True)
    is_active = fields.BooleanField(default=True)
    profile_photo = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users"
        ordering = ['first_name', 'telegram_id']

    def __str__(self):
        return f"User({self.telegram_id} - {self.username or self.first_name})"

from django.db import models
from core.models import BaseModel, StatusChoice


class Category(BaseModel):
    name = models.CharField(max_length=255)
    status = models.PositiveIntegerField(choices=StatusChoice.choices,
                                         default=StatusChoice.ACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'

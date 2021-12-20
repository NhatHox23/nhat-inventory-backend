from django.db import models
from core.models import BaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Category(BaseModel):
    class CategoryStatus(models.IntegerChoices):
        ACTIVE = 1
        INACTIVE = 2
        OUT_OF_STOCK = 3

    name = models.CharField(max_length=255)
    status = models.IntegerField(choices=CategoryStatus.choices,
                                 default=CategoryStatus.ACTIVE)

    class Meta:
        db_table = "category"

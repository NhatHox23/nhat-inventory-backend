from django.db import models
from core.models import BaseModel


# Create your models here.


class Category(BaseModel):
    class CategoryStatus(models.IntegerChoices):
        ACTIVE = 1
        INACTIVE = 2
        OUT_OF_STOCK = 3

    name = models.CharField(max_length=255)
    status = models.IntegerField(choices=CategoryStatus.choices,
                                 default=CategoryStatus.ACTIVE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"

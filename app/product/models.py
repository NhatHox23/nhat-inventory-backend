from django.db import models

from core.models import BaseModel, StatusChoice


# Create your models here.

class Product(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)
    status = models.PositiveIntegerField(choices=StatusChoice.choices,
                                         default=StatusChoice.ACTIVE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'
        unique_together = ['name', 'category']

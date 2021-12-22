from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampModel):
    created_by = models.ForeignKey('account.User', related_name="+",
                                   on_delete=models.CASCADE,
                                   null=True, blank=True)
    updated_by = models.ForeignKey('account.User', related_name="+",
                                   on_delete=models.CASCADE,
                                   null=True, blank=True)

    class Meta:
        abstract = True

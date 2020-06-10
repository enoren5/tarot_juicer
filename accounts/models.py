from django.core.exceptions import ValidationError
from django.db import models


class AuthToggle(models.Model):
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.pk and AuthToggle.objects.exists():
            raise ValidationError('There is can be only one AuthToggle instance')
        return super(AuthToggle, self).save(*args, **kwargs)

    def __str__(self):
        return "Authentication is currently {}".format("enabled" if self.active else "disabled")

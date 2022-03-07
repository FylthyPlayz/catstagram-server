from django.db import models

class Like(models.Model):
    like = models.BooleanField(default=False)
from django.db import models
from catstagramapi.models.catstagramer import Catstagramer


class Like(models.Model):
    user = models.ForeignKey(Catstagramer, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    
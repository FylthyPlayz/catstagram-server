from django.db import models

class UserRating(models.Model):
    rating = models.IntegerField(null=True)
    user = models.ForeignKey("Catstagramer", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
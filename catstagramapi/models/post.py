from django.db import models


class Post(models.Model):
    image = models.ImageField(null=False)
    publication_date = models.DateField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey("Catstagramer", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", through="PostTag")
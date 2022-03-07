from django.db import models


class Post(models.Model):
    image = models.ImageField(null=True)
    publication_date = models.DateField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey("Catsagramer", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", through="PostTag")
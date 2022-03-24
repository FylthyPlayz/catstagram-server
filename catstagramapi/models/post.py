from django.db import models


class Post(models.Model):
    image = models.ImageField(null=True)
    publication_date = models.DateField(auto_now_add=True)
    content = models.TextField()
    user = models.ForeignKey("Catstagramer", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", through="PostTag")
    likes = models.ManyToManyField("Catstagramer", through="Like", related_name="likes")


    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
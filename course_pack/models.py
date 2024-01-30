from django.contrib.auth.models import User
from django.db import models


class CoursePack(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='course_pack')

    def __str__(self):
        return self.title


class ViewCoursePack(models.Model):
    ip = models.GenericIPAddressField()
    course_pack = models.ForeignKey(CoursePack, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.ip

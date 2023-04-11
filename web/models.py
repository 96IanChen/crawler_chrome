from django.db import models

# Create your models here.

class Div(models.Model):
    content = models.TextField("內容", default='')
    status = models.BooleanField("狀態", default=False)
    divnumber = models.IntegerField("編號", default=0)

    def __str__(self):
        return self.content

class Text(models.Model):
    content = models.TextField("內容", default='')
    status = models.BooleanField("狀態", default=False)
    div = models.ForeignKey(Div, on_delete=models.CASCADE, related_name='text', default="", null=True, blank=True)

    def __str__(self):
        return self.content

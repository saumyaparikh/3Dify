# from typing_extensions import Required
from django.db import models
from django.http import request


class StereoImages(models.Model):
	
	email=models.CharField(max_length=500,default="")
	
	StereoImg = models.ImageField(upload_to='images/', null=True, blank=True)


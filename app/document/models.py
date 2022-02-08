from xml.dom.minidom import Document
from django.db import models
from app.accounts.models import Customer

class Upload(models.Model):
    title = models.CharField(max_length=50, verbose_name="Título")
    document = models.FileField()
    customer = models.ForeignKey(
        Customer, verbose_name=("Cliente"), on_delete=models.CASCADE, blank=True, null=True
    )
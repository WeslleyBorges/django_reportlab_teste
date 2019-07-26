from django.db import models

# Create your models here.
class Teste(models.Model):
    descricao = models.CharField(max_length=50)
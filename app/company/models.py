from django.db import models
from validate_docbr import CNPJ
from django.core.exceptions import ValidationError

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nome")
    address = models.CharField(max_length=255, verbose_name="Endereço")
    city = models.CharField(max_length=50, verbose_name="Cidade")
    cnpj = models.CharField(max_length=20, verbose_name="CNPJ")
    is_active = models.BooleanField(default=True,help_text=("Designates whether this company should be treated as active. Unselect this instead of deleting accounts."), verbose_name="Ativo?",)
    district = models.CharField(max_length=255, blank=True, null=True, verbose_name=("Bairro"))

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        validate = CNPJ()
        if validate.validate(self.cnpj):
            return super().clean()   
        else:
            raise ValidationError('CNPJ inválido')


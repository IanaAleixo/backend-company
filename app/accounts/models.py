from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from app.accounts.managers import UserManager
from app.common import choices
from validate_docbr import CPF
from django.core.exceptions import ValidationError

validate = CPF()

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255,verbose_name="Nome")
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False, help_text=("Designates whether the user can log into this admin site."),)
    is_active = models.BooleanField(default=True,help_text=("Designates whether this user should be treated as active. Unselect this instead of deleting accounts."), verbose_name="Ativo?",)
    type = models.PositiveIntegerField(choices=choices.TYPE_USER, blank=True, default=0, verbose_name="Tipo de usuário", editable=False)
    USERNAME_FIELD = "email"
    phone = models.CharField(max_length=30, verbose_name="Telefone", blank=True, null=True)
    cpf = models.CharField(max_length=14, verbose_name="CPF", blank=True, null=True)
    gender = models.CharField(choices=choices.GENDER, max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=("Endereço"))
    address_number = models.CharField(max_length=30, blank=True, null=True, verbose_name=("Número"))
    cep = models.CharField(max_length=255, blank=True, null=True, verbose_name=("CEP"))
    complement = models.CharField(max_length=255, blank=True, null=True, verbose_name=("Complemento"))
    district = models.CharField(max_length=255, blank=True, null=True, verbose_name=("Bairro"))
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name=("País"))
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name=("Estado"))
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name=("Cidade"))
    manager = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name=("manager_user"), verbose_name=("Gerente"))

    objects = UserManager()

    def __str__(self) -> str:
        return self.name

class ManagerUser(models.Manager):
    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop("type", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(type=self.type)

    def create(self, **kwargs):
        kwargs.update({"type": self.type})
        return super().create(**kwargs)  

class Admin(User):
    objects = ManagerUser(type=choices.TYPE_USER.admin)
    
    class Meta:
        proxy = True
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

class Customer(User):
    objects = ManagerUser(type=choices.TYPE_USER.customer)

    class Meta:
        proxy = True
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = False
        self.type = 1
        if self.manager.is_active == False:
            self.is_staff = False
        return super().save(*args, **kwargs)

    def clean(self) -> None:
        if validate.validate(self.cpf):
            return super().clean()   
        else:
            raise ValidationError('CPF inválido') 

class Manager(User):
    objects = ManagerUser(type=choices.TYPE_USER.manager)

    class Meta:
        proxy = True
        verbose_name = "Gerente"
        verbose_name_plural = "Gerentes"
    
    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = False
        self.type = 2
        super().save(*args, **kwargs)
        self.groups.add(1)

    def clean(self) -> None:
        if validate.validate(self.cpf):
            return super().clean()   
        else:
            raise ValidationError('CPF inválido')
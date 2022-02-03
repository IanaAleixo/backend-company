from django import forms

class RequestCPF(forms.ModelForm):
    def _init_(self, *args, **kwargs):
        super(RequestCPF, self)._init_(*args, **kwargs)
        self.fields['cpf'].required = True
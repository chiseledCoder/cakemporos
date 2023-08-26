from django import forms
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Baker

class ProductForm(forms.ModelForm):
	class Meta:
		model = Baker
		fields = ('__all__')
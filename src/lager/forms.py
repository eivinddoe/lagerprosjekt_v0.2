from django.forms import ModelForm
from .models import Artikkel

class ArtikkelForm(ModelForm):
	class Meta:
		model = Artikkel
		fields = '__all__'
from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.forms import ModelForm

from .models import Artikkel

class ArtikkelForm(ModelForm):
	class Meta:
		model = Artikkel
		fields = '__all__'


class TestForm(ModelForm):
	class Meta:
		model = Artikkel
		exclude = ['tid_for_vurdering', 'lagerkost_aar', 'kostnad_ved_defekt', 'tid_inne', 'levetid', 'lager', 'kritisk_dato']
		widgets = {
		'art_nr': forms.TextInput(attrs= {'placeholder': 	''}),
		'pris': forms.TextInput(attrs= {'placeholder': 	'kr'}),
		'leveringstid': forms.TextInput(attrs= {'placeholder': 	''}),
		'sist_byttet': DatePickerInput(format='%m/%d/%Y'),
		'planlagt_byttet': DatePickerInput(format='%m/%d/%Y'),
		'forbrenning_grad': forms.TextInput(attrs= {'placeholder': 	'0-100 (%)'}),
		'stromprod_grad': forms.TextInput(attrs= {'placeholder': 	'0-100 (%)'}),
		'kost_alternativ_drift': forms.TextInput(attrs= {'placeholder': 	'kr'})
		}

		labels = {
		'art_nr': 'Artikkelnummer',
		'pris': 'Pris',
		'leveringstid': 'Leveringstid (i uker)',
		'sist_byttet': 'Delen ble sist byttet (dato)',
		'planlagt_byttet': 'Delen er planlagt byttet (dato)',
		'skal_byttes': 'Planlagt bytte er sikkert/usikkert',
		'type_levetid': 'Gjenværende/forventet levetid',
		'levetid_aar': 'Levetid (i år)',
		'forbrenning_konsekvens': 'Konsekvens for avfallsforbrenning',
		'forbrenning_grad': 'Grad av stans i avfallsforbrenning',
		'stromprod_konsekvens': 'Konsekvens for strømproduksjon',
		'stromprod_grad': 'Grad av stans i strømproduksjon'
		}
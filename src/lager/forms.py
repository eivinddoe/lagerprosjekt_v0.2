from bootstrap_datepicker_plus import DatePickerInput
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

		labels = {
		'art_nr': 'Artikkelnummer',
		'leveringstid': 'Leveringstid (i uker)',
		'sist_byttet': 'Delen ble sist byttet (dato)',
		'planlagt_byttet': 'Delen er planlagt byttet (dato)',
		'skal_byttes': 'Planlagt bytte er sikker/usikker',
		'type_levetid': 'Gjenværende/forventet levetid',
		'levetid_aar': 'Levetid (i år)',
		'forbrenning_konsekvens': 'Defekt har konsekvens for avfallsforbrenning (ja/nei)',
		'forbrenning_grad': 'Grad av stans i avfallsforbrenning (0-1)',
		'stromprod_konsekvens': 'Defekt har konsekvens for strømproduksjon (ja/nei)',
		'stromprod_grad': 'Grad av stans i strømproduksjon (0-1)'

		}


		widgets = {'sist_byttet': DatePickerInput(format='%d/%m/%Y'),
		'planlagt_byttet': DatePickerInput(format='%d/%m/%Y')}
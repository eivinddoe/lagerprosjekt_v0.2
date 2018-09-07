from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import pre_save

# Models
class FastParameter(models.Model):
	PARAMETER_VALG = (
		('Lagerkost', 'Lagerkost'),
		('Kost ved driftsstans (gatefee)', 'Kost ved driftsstans (gatefee)'),
		('Kost ved stans i strømproduksjon', 'Kost ved stans i strømproduksjon'),
		)
	parameter = models.CharField(max_length = 40, choices = PARAMETER_VALG, unique = True, null = True)
	parameter_verdi = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)

	class Meta:
		verbose_name_plural = 'Faste parametere'

	def __str__(self):
		return self.parameter

class Artikkel(models.Model):

	# Hente parameterverdier for stanskost
	kost_gatefee = int(FastParameter.objects.get(parameter = 'Kost ved driftsstans (gatefee)').parameter_verdi)
	kost_stromprod = int(FastParameter.objects.get(parameter = 'Kost ved stans i strømproduksjon').parameter_verdi)


	art_nr = models.IntegerField('Artikkelnummer')
	tid_for_vurdering = models.DateTimeField('Tid for vurdering', auto_now_add = True, null = True)
	pris = models.IntegerField('Pris')
	lagerkost_aar = models.DecimalField('Årlig lagerkost', max_digits = 10, decimal_places = 2, null = True, blank = True)
	leveringstid = models.IntegerField('Leveringstid i uker')
	sist_byttet = models.DateField('Sist byttet')
	tid_inne = models.IntegerField('Tid inne', null = True, blank = True)
	planlagt_byttet = models.DateField('Planlagt byttet', blank = True, null = True)
	skal_byttes = models.CharField('Sikkert/usikkert bytte', max_length = 10, blank = True, null = True, 
		choices = (
			('Sikkert', 'Sikkert'), 
			('Usikkert', 'Usikkert'),
			))

	LEVETID_VALG = (
		('Gjenværende levetid', 'Gjenværende levetid'), 
		('Forventet levetid', 'Forventet levetid'),
		)
	type_levetid = models.CharField(max_length = 30, choices = LEVETID_VALG)
	levetid = models.IntegerField('Levetid i år')

	KONSEKVENSER_VALG = (
		('Stans i forbrenning', 'Stans i forbrenning'),
		('Stans i strømproduksjon', 'Stans i strømproduksjon'),
		('Alternativ/justert drift', 'Alternativ/justert drift'),
		('Ingen avbrudd', 'Ingen avbrudd'),
		)
	type_konsekvens = models.CharField(max_length = 30, choices = KONSEKVENSER_VALG, null = True)

	kost_alternativ_drift = models.IntegerField('Kostnad (per døgn) ved alternativ drift', 
		blank = True, null = True)

	REDUSERT_DRIFT_VALG = (
		('50%', '50%'),
		('60%', '60%'),
		('70%', '70%'),
		('80%', '80%'),
		('90%', '90%'),
		)
	redusert_drift = models.CharField(max_length = 5, choices = REDUSERT_DRIFT_VALG, 
		null = True, blank = True)

	class Meta:
		ordering = ['art_nr']
		verbose_name_plural = 'artikler'

	def __str__(self):
		return str(self.art_nr)

def pre_save_artikkel_receiver(sender, instance, *args, **kwargs):
		lagerkost = float(FastParameter.objects.get(parameter = 'Lagerkost').parameter_verdi)
		lagerkost_aar = lagerkost * instance.pris
		instance.lagerkost_aar = lagerkost_aar

		tid_inne = (datetime.today().date()-instance.sist_byttet).days
		instance.tid_inne = tid_inne

pre_save.connect(pre_save_artikkel_receiver, sender = Artikkel)
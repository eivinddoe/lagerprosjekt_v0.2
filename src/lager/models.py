from datetime import datetime, timedelta
from django.db import models
from django.db.models.signals import pre_save

import math

# Models

class FastParameter(models.Model):
	PARAMETER_VALG = (
		('Lagerkost', 'Lagerkost'),
		('Kost ved driftsstans (gatefee)', 'Kost ved driftsstans (gatefee)'),
		('Kost ved stans i strømproduksjon', 'Kost ved stans i strømproduksjon'),
		('Weibull Shape Parameter', 'Weibull Shape Parameter'),
		('Weibull Scale Parameter', 'Weibull Scale Parameter'),
		)
	parameter = models.CharField(max_length = 40, choices = PARAMETER_VALG, unique = True, null = True)
	parameter_verdi = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)

	class Meta:
		verbose_name_plural = 'Faste parametere'

	def __str__(self):
		return self.parameter

class Konsekvenser(models.Model):
	konsekvens = models.CharField(max_length = 30)

	def __str__(self):
		return self.konsekvens

class Artikkel(models.Model):

	art_nr = models.IntegerField('Artikkelnummer')
	tid_for_vurdering = models.DateTimeField('Tid for vurdering', auto_now_add = True, null = True)
	pris = models.IntegerField('Pris')
	lagerkost_aar = models.DecimalField('Årlig lagerkost', max_digits = 10, decimal_places = 2, null = True, blank = True)
	kostnad_ved_defekt = models.IntegerField('Daglig kostnad ved defekt', null = True, blank = True)
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
	levetid_aar = models.IntegerField('Levetid i år', null = True)
	levetid = models.IntegerField('Levetid i dager', blank = True, null = True)

	forbrenning_konsekvens = models.BooleanField(null = True, default = False)
	forbrenning_grad = models.DecimalField(max_digits = 2, decimal_places = 1, null = True, blank = True)
	stromprod_konsekvens = models.BooleanField(null = True, default = False)
	stromprod_grad = models.DecimalField(max_digits = 2, decimal_places = 1, null = True, blank = True)

	kost_alternativ_drift = models.IntegerField('Kostnad (per døgn) ved alternativ drift', 
		blank = True, null = True)

	lager = models.BooleanField('Skal bestilles', null = True, blank = True, default = False)
	kritisk_dato = models.DateField('Kritisk dato', null = True, blank = True)

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

		# Kostnad ved defekt
		# Hente parameterverdier for stanskost
		kost_gatefee = int(FastParameter.objects.get(parameter = 'Kost ved driftsstans (gatefee)').parameter_verdi)
		kost_stromprod = int(FastParameter.objects.get(parameter = 'Kost ved stans i strømproduksjon').parameter_verdi)

		kost_defekt = 0

		if instance.forbrenning_konsekvens:
			kost_defekt += instance.forbrenning_grad * kost_gatefee
		if instance.stromprod_konsekvens:
			kost_defekt += instance.stromprod_grad * kost_stromprod
		if instance.kost_alternativ_drift:
			kost_defekt += instance.kost_alternativ_drift

		instance.kostnad_ved_defekt = kost_defekt

		# Levetid i dager
		if instance.type_levetid == 'Gjenværende levetid':
			levetid = tid_inne + instance.levetid_aar*365
			instance.levetid = levetid
		elif instance.type_levetid == 'Forventet levetid':
			levetid = instance.levetid_aar * 365
			instance.levetid = levetid

		# Mekke sannsynligheter for ting som koster noe om går i stykker
		if kost_defekt > 0:
			if tid_inne >= levetid:
				instance.lager = True
				instance.kritisk_dato = datetime.today().date()
			else:
				def WeibullCDF(x, lmbd, k):
					q = pow(x / lmbd, k)
					return 1.0 - math.exp(-q)

				weib_shape = int(FastParameter.objects.get(parameter = 'Weibull Shape Parameter').parameter_verdi)
				cdf_start = WeibullCDF(tid_inne, levetid, weib_shape)
				survival_start = 1 - cdf_start

				p_nede = []
				p_survival = []
				for i in range(tid_inne, levetid):
					p_nede.append((WeibullCDF(i, levetid, weib_shape) - cdf_start) / survival_start)
					p_survival.append((1 - WeibullCDF(i, levetid, weib_shape)))

				# Beregne vektet nedetidskostnad
				kost_defekt = float(kost_defekt)
				vektet_nedetidskost = [i * kost_defekt for i in p_nede]

				# Beregne vektet lagerkostnad
				if instance.skal_byttes == 'Sikkert':
					max_lagertid = (instance.planlagt_byttet - datetime.today().date()).days
				elif instance.skal_byttes == 'Usikkert':
					max_lagertid = int(0.5*((instance.planlagt_byttet - datetime.today().date()).days)+0.5*levetid)
				else:
					max_lagertid = levetid

				lagerkost_dag = lagerkost_aar / 365
				vektet_lagerkostnad_dag = [i * lagerkost_dag for i in p_survival]
				vektet_lagerkost = [sum(vektet_lagerkostnad_dag[i:max_lagertid]) for i in range(0, max_lagertid)]

				i = 0
				while vektet_nedetidskost[i] < vektet_lagerkost[i]:
					i += 1
					if i == max_lagertid:
						break

				kritisk_dato = datetime.today().date() + timedelta(days=i)
				instance.kritisk_dato = kritisk_dato

				if kritisk_dato <= datetime.today().date() + timedelta(days=(instance.leveringstid*7)):
					instance.lager = True
				else:
					instance.lager = False	
		else:
			instance.lager = False


pre_save.connect(pre_save_artikkel_receiver, sender = Artikkel)
from django.contrib import admin

# Register your models here.
from .models import Artikkel, FastParameter

@admin.register(Artikkel)
class ArtikkelAdmin(admin.ModelAdmin):
	list_display = ('art_nr', 'pris', 'lagerkost_aar', 'sist_byttet', 'tid_inne', 'type_konsekvens', 'levetid', 'tid_for_vurdering')
	list_filter = ('lagerkost_aar', 'levetid', 'tid_inne', 'type_konsekvens', 'tid_for_vurdering')

@admin.register(FastParameter)
class FastParameterAdmin(admin.ModelAdmin):
	list_display = ('parameter', 'parameter_verdi')
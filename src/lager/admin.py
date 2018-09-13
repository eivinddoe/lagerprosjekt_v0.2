from django.contrib import admin

# Register your models here.
from .models import Artikkel, FastParameter, Feedback

@admin.register(Artikkel)
class ArtikkelAdmin(admin.ModelAdmin):
	list_display = ('art_nr', 'pris', 'lagerkost_aar', 'sist_byttet', 'tid_inne', 'levetid', 'tid_for_vurdering', 'kostnad_ved_defekt', 'kritisk_dato', 'lager')
	list_filter = ('lager',)

@admin.register(FastParameter)
class FastParameterAdmin(admin.ModelAdmin):
	list_display = ('parameter', 'parameter_verdi')

admin.site.register(Feedback)
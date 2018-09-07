from datetime import datetime, timedelta
from django.shortcuts import render
from .forms import ArtikkelForm

# Create your views here.
def main(request):
    if request.method == 'POST': # hva som skal skje når skjemaet sendes
        lagerkost = 0.05
        today = datetime.today().date()

        form = ArtikkelForm(request.POST)

        context = {
        'form': form
        }

        if form.is_valid(): # Hvis det som er lagt inn i skjemaet er gyldige greier
            art_nr = form.cleaned_data['art_nr']
            pris = form.cleaned_data['pris']
            leveringstid = form.cleaned_data['leveringstid']
            sist_byttet = form.cleaned_data['sist_byttet']
            planlagt_byttet = form.cleaned_data['planlagt_byttet']
            hvor_sikkert = form.cleaned_data['skal_byttes']

            context.update({
                'art_nr': art_nr,
                'pris': pris,
                'leveringstid': leveringstid,
                'sist_byttet': sist_byttet,
                'planlagt_byttet': planlagt_byttet,
                'hvor_sikkert': hvor_sikkert
                })


    else:
        form = ArtikkelForm()
        context = {
        'form': form
        }

    return render(request, 'index.html', context)
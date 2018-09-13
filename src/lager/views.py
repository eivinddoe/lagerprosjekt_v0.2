from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render

from .forms import ArtikkelForm, TestForm, FeedbackForm
# from .functions import Nedetidskost, WeibullCDF, ProbNede, ProbSurvival
from .models import Artikkel, FastParameter, Feedback

import json

# Create your views here.
def test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            decision = True
            form.save()
            instance = form.save()
            queryset = Artikkel.objects.get(pk = instance.pk)
            context = {'decision': decision, 'form': form, 'queryset': queryset}
        else:
            context = {'form': form}
    else:
        form = TestForm()
        context = {'form': form}

    return render(request, 'index.html', context)

def feed(request):
    if request.method == "POST":
        feedback = FeedbackForm(request.POST)
        if feedback.is_valid():
            success = True
            feedback.save()
            context = {'feedback': feedback, 'success': success}
        else:
            feedback = FeedbackForm()
            context = {'feedback': feedback}
    else: 
        feedback = FeedbackForm()
        context = {'feedback': feedback}
    return render(request, 'feedback.html', context)

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
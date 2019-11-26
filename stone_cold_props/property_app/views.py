from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from .models import *
from django.template import loader
from .search import searchForm, resultForm
from django.views.generic.list import ListView


def index(request):

	 return HttpResponse("Hello world, this is Stone Cold Steve Austin.")


def table(request):
	template_name = loader.get_template('property_app/generic_table.html')
	table = Tenant
	items = table.objects.all()
	print(items)
	context = {
		'items': items,
	}

	return HttpResponse(template_name.render(context, request))


def search(request):

	if request.method == 'POST':
		form = searchForm(request.POST)
		if form.is_valid():

			type =form.cleaned_data['type']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			result = Address.objects.filter(city = city, state = state)
			request.session['result'] = serializers.serialize('json', result)
			request.session.modified = True
			return redirect('search_results')



	form = searchForm()
	return render(request, 'property_app/search.html', {'form': form})


def search_results(request):
	template_name = loader.get_template('property_app/results.html')

	query = [i.object for i in serializers.deserialize('json',request.session['result'])]
	context = {'query': query}
	return(HttpResponse(template_name.render(context, request)))



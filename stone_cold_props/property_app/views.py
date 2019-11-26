from itertools import chain

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from .models import *
from django.template import loader
from .forms import searchForm, loginForm
import json
import django_tables2 as tables


def index(request):

	# return HttpResponse("Hello world, this is Stone Cold Steve Austin.")
	if request.method == 'POST':
		form = loginForm(request.POST)
		if form.is_valid():
			print("valid")



	form = loginForm()
	return render(request, 'property_app/login.html', {'form': form})


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
			result2 =  Unit.objects.none()
			type =form.cleaned_data['type']
			found = list()
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			bedrooms = form.cleaned_data['Minimum_Bedrooms']
			bathrooms = form.cleaned_data['Minimum_Bathrooms']
			rent = form.cleaned_data['Max_Rent']
			result = Unit.objects.filter(available = 1)


			for x in result:
				print(x.rent)

				building = Building.objects.get(pk=x.building.building_id)
				address = Address.objects.get(pk=x.building.building_id)

				# filter out units based on search parameters:
				if (int(rent)>x.rent and  x.bedrooms >= int(bedrooms) and x.bathrooms >= int(bathrooms)
						and (address.city.strip() == city or city == '*') and (address.state.strip() == state or state == '*')
						and (building.type.strip() == type or type == "*")):

					found.append({'rent':int(x.rent),
								  'address':" ".join([address.street,address.city.strip(), address.state.upper(), str(address.zip)]),
								  'bathrooms': int(x.bathrooms),
								  'bedrooms': int(x.bedrooms),
								  'type': building.type,
								  'unit': str(int(x.unit_number))
								  })



			request.session['result'] = json.dumps(found)
			request.session.modified = True
			return redirect('search_results')



	form = searchForm()
	return render(request, 'property_app/search.html', {'form': form})


def search_results(request):
	template_name = loader.get_template('property_app/results.html')

	# query = [i.object for i in serializers.deserialize('json',request.session['result'])]
	query = json.loads(request.session['result'])

	class UnitTable(tables.Table):
		address = tables.Column()
		unit = tables.Column()
		rent = tables.Column()
		bathrooms = tables.Column()
		bedrooms = tables.Column()
		type = tables.Column()


	table = UnitTable(query)




	context = {'table': table}
	return(HttpResponse(template_name.render(context, request)))



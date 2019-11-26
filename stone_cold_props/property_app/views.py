from itertools import chain

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from .models import *
from django.template import loader
from .forms import searchForm, loginForm
from django.views.generic.list import ListView


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
			#result = Address.objects.all().filter(city = city, state = state)
			#for x in result:
			#	if x.bedrooms < bedrooms
			#result = result.filter(city = city, state = state, bedrooms = result.bedrooms)
			result = Unit.objects.filter(available = 1)


			for x in result:
				print(x.rent)

				building = Building.objects.get(pk=x.building.building_id)
				address = Address.objects.get(pk=x.building.building_id)


				if (int(rent)>x.rent and  x.bedrooms >= int(bedrooms) and x.bathrooms >= int(bathrooms) and (address.city.strip() == city or city == '*') and (address.state.strip() == state or state == '*')  and (building.type.strip() == type or type == "*")):			#filtering out all that dosent habve enough bathrooms ect
					print('found one')
					found.append(x)

			result3 = list(chain(result2, found))
			request.session['result'] = serializers.serialize('json', result3)
			request.session.modified = True
			return redirect('search_results')



	form = searchForm()
	return render(request, 'property_app/search.html', {'form': form})


def search_results(request):
	template_name = loader.get_template('property_app/results.html')

	query = [i.object for i in serializers.deserialize('json',request.session['result'])]
	context = {'query': query}
	return(HttpResponse(template_name.render(context, request)))



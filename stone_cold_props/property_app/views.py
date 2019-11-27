from itertools import chain

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from .models import *
from django.template import loader
from .forms import *
import json
import django_tables2 as tables
from datetime import date
from dateutil.relativedelta import relativedelta


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


def search_by_address(request):

	if request.method == 'POST':
		form = searchForm(request.POST)
		if form.is_valid():
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
			return redirect('results_by_address')



	form = searchForm()
	return render(request, 'property_app/search_by_address.html', {'form': form})


def results_by_address(request):

	template_name = loader.get_template('property_app/results_by_address.html')
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

def expiring_contracts_search(request):

	if request.method == 'POST':
		form = expiringContractForm(request.POST)
		if form.is_valid():
			contracts = Contract.objects.all()
			expring_contracts = []
			for contract in contracts:

				# get expiring contracts:
				end = contract.end_date
				today = date.today()
				months_ahead = int(form.cleaned_data['expr'])
				end_of_window = today + relativedelta(months=+months_ahead)

				if end < end_of_window:
					# get information about building, its address, and client
					building = Building.objects.get(pk=contract.building.building_id)
					address = Address.objects.get(pk=contract.building.building_id)
					client = Client.objects.get(pk=contract.ssn.ssn)

					expring_contracts.append(
						{
							'name': " ".join([client.first_name, client.last_name]),
							'phone': client.phone,
							'building_id': int(building.building_id),
							'address': " ".join([address.street,address.city.strip(), address.state.upper(), str(address.zip)]),
							'end': str(contract.end_date),
							'pay': int(contract.payment)
						}
					)
			request.session['expiring_contract_result'] = json.dumps(expring_contracts)
			request.session.modified = True
			return redirect('expiring_contracts_results')

	form = expiringContractForm()
	return render(request, 'property_app/expiring_contracts_search.html', {'form':form})

def expiring_contracts_results(request):
	template_name = loader.get_template('property_app/expiring_contracts_results.html')
	query = json.loads(request.session['expiring_contract_result'])


	class ExpiringContractTable(tables.Table):

		name = tables.Column()
		phone = tables.Column()
		building_id = tables.Column()
		address = tables.Column()
		pay = tables.Column()
		end = tables.Column()

	table = ExpiringContractTable(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))






def tentant_search(request):
	if request.method == 'POST':
		form = tenantSearchForm(request.POST)
		if form.is_valid():
			tentants_found = []
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			street = form.cleaned_data['address']
			zip = form.cleaned_data['zip']
			unit = form.cleaned_data['unit']
			manager = form.cleaned_data['manager']
			owner = form.cleaned_data['owner']
			leases = Lease.objects.all()
			for x in leases:
				id = x.building.building_id
				address = Address.objects.get(pk=id)

				contract = Contract.objects.all().filter(building=id)
				#client = Client.objects.get(pk=contract.SSN)			#TODO IT SAYS SSN IS NOT AN ATRIBUTE OF CONTRACTS EVEN THOUGH IT IS? FIX THIS AND WELL BE GOOD
				if 		((address.city.strip() == city or city == '*') and
						(address.state.strip() == state or state == '*') and
						(address.zip == zip or zip == '*') and
						(address.street.strip() == street or street == '*') and
						(x.unit == unit or unit == '*') and
						(x.prop_man == manager or manager== '*') #and
						#(client.first_name + " " + client.last_name == owner or owner=='*')):
				):
					found_tanant = Tenant.objects.get(pk =x.tenant )
					tentants_found.append(
						{
							'name': " ".join([found_tanant.first_name, found_tanant.last_name]),
							'phone': found_tanant.phone,
							'address': " ".join(
								[address.street, address.city.strip(), address.state.upper(), str(address.zip), str(x.unit)]),

						}
					)

			request.session['tenants_search'] = json.dumps(tentants_found)
			request.session.modified = True
			return redirect('tenant_search_results')

	form = tenantSearchForm()
	return render(request, 'property_app/tenant_search.html', {'form':form})


def tenant_search_results(request):
	template_name = loader.get_template('property_app/tenant_search_result.html')
	query = json.loads(request.session['tenants_search'])
	class tenantInfoTable(tables.Table):

		name = tables.Column()
		phone = tables.Column()
		address = tables.Column()


	table = tenantInfoTable(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))
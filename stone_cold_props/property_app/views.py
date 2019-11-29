from itertools import chain

from django.shortcuts import render, redirect
from decimal import Decimal
from django.db import connection
from django.http import HttpResponse
from django.core import serializers
from .models import *
from django.template import loader
from .forms import *
from.tables import *
import json
from datetime import date
from dateutil.relativedelta import relativedelta
import pyrebase.pyrebase
from django.shortcuts import get_object_or_404

# Connection for employees to firebase login authentification
config = {
	'apiKey': "AIzaSyBIiU-vYyoHB3WqAkzgX9B2FtMzyKu9PSk",
	'authDomain': "database-258713.firebaseapp.com",
	'databaseURL': "https://database-258713.firebaseio.com/",
	'projectId': "database-258713",
	'storageBucket': "database-258713.appspot.com",
	'messagingSenderId': "225140590988",
	'appId': "1:225140590988:web:b5f4f273d0250782e6eea9"
}
# firebase = pyrebase.initialize_app(config)
#
# auth = firebase.auth()

# Admin connection
configAdmin = {
    'apiKey': "AIzaSyCX3rg4fptOdNpsll4iUu0JgjGHMLiAOOE",
    'authDomain': "homework4-256814.firebaseapp.com",
    'databaseURL': "https://homework4-256814.firebaseio.com",
    'projectId': "homework4-256814",
    'storageBucket': "homework4-256814.appspot.com",
    'messagingSenderId': "999208004782",
    'appId': "1:999208004782:web:cf8047d08b5e438725913f"
}
# Initialize FirebaseAdmin
# firebaseAdmin = pyrebase.initializeApp(configAdmin)
#
# auth2 = firebaseAdmin.auth()


def signIn(request):
	return render(request, 'property_app/signIn.html')


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
			type = form.cleaned_data['type']
			found = list()
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			bedrooms = form.cleaned_data['Minimum_Bedrooms']
			bathrooms = form.cleaned_data['Minimum_Bathrooms']
			rent = form.cleaned_data['Max_Rent']
			result = Unit.objects.filter(available=1)
			sqFt = form.cleaned_data['Minimum_SqFt']

			for x in result:
				print(x.rent)

				building = Building.objects.get(pk=x.building.building_id)
				address = Address.objects.get(pk=x.building.building_id)

				# filter out units based on search parameters:
				if (int(rent) > x.rent and x.bedrooms >= int(bedrooms) and x.bathrooms >= int(bathrooms)
						and (address.city.strip() == city or city == '*') and (
								address.state.strip() == state or state == '*')
						and (building.type.strip() == type or type == "*")
						and (int(sqFt) < x.sqft)):
					found.append({'rent': int(x.rent),
								  'address': " ".join(
									  [address.street, address.city.strip(), address.state.upper(), str(address.zip)]),
								  'bathrooms': int(x.bathrooms),
								  'bedrooms': int(x.bedrooms),
								  'type': building.type,
								  'unit': str(int(x.unit_number)),
								  'sqft': str(x.sqft)
								  })

			request.session['result'] = json.dumps(found)
			request.session.modified = True
			return redirect('results_by_address')
	# Allows for employees to login if valid entries
	email = request.POST.get('email')
	password = request.POST.get('pass')
	user = auth.sign_in_with_email_and_password(email, password)

	form = searchForm()
	return render(request, 'property_app/search_by_address.html', {'form': form})


def results_by_address(request):
	template_name = loader.get_template('property_app/results_by_address.html')
	query = json.loads(request.session['result'])


	table = UnitTable(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))


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
							'address': " ".join(
								[address.street, address.city.strip(), address.state.upper(), str(address.zip)]),
							'end': str(contract.end_date),
							'pay': int(contract.payment)
						}
					)
			request.session['expiring_contract_result'] = json.dumps(expring_contracts)
			request.session.modified = True
			return redirect('expiring_contracts_results')

	form = expiringContractForm()
	return render(request, 'property_app/expiring_contracts_search.html', {'form': form})


def expiring_contracts_results(request):
	template_name = loader.get_template('property_app/expiring_contracts_results.html')
	query = json.loads(request.session['expiring_contract_result'])

	table = ExpiringContractTable(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))


def tentant_search(request):
	if request.method == 'POST':
		form = tenantSearchForm(request.POST)
		if form.is_valid():
			tentants_found = []
			city = form.cleaned_data['city'].strip()
			state = form.cleaned_data['state'].strip()
			street = form.cleaned_data['address'].strip()
			zip = form.cleaned_data['zip']
			unit = form.cleaned_data['unit'].strip()
			manager = form.cleaned_data['manager'].strip()
			owner = form.cleaned_data['owner'].strip()
			first_name = form.cleaned_data['first_name'].strip()
			last_name = form.cleaned_data['last_name'].strip()
			leases = Lease.objects.all()
			for x in leases:
				id = x.building.building_id
				print(x.prop_man + " 1")
				print(manager + " 2")
				address = Address.objects.get(pk=id)
				manager_object = get_object_or_404(PropertyManager, pk=x.prop_man)
				contract = Contract.objects.filter(
					building=id)  # this is return a query set and not an indvidual object
				for w in contract:
					contract = w
				temp_tenant = Tenant.objects.get(pk=x.tenant)

				client = Client.objects.get(pk=contract.ssn.ssn)
				if ((address.city.strip() == city or city == '*') and
						(address.state.strip() == state or state == '*') and
						(address.zip == zip or zip == '*') and
						(address.street.strip() == street or street == '*') and
						(x.unit == unit or unit == '*') and
						(manager_object.first_name + " " + manager_object.last_name == manager or manager == '*') and
						(client.first_name + " " + client.last_name == owner or owner == '*') and
						(
								temp_tenant.first_name.strip() == first_name or first_name == '*') and  # TODO KEVIN IN DATABASE HAS A " " BEFORE HIS NAME AND .STRIP() DOSENT REMOVE IT SO KEVINS FIRST NAME SEACH DOSENT WORK
						(temp_tenant.last_name.strip() == last_name or last_name == '*')):
					found_tanant = Tenant.objects.get(pk=x.tenant)
					tentants_found.append(
						{
							'name': " ".join([found_tanant.first_name, found_tanant.last_name]),
							'phone': found_tanant.phone,
							'address': " ".join(
								[address.street, address.city.strip(), address.state.upper(), str(address.zip),
								 str(x.unit)]),

						}
					)

			request.session['tenants_search'] = json.dumps(tentants_found)
			request.session.modified = True
			return redirect('tenant_search_results')

	form = tenantSearchForm()
	return render(request, 'property_app/tenant_search.html', {'form': form})


def tenant_search_results(request):
	template_name = loader.get_template('property_app/tenant_search_result.html')
	query = json.loads(request.session['tenants_search'])

	table = tenantInfoTable(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))


def property_manager_search_by_address(request):
	if request.method == 'POST':
		form = managerAddressSearchForm(request.POST)
		if form.is_valid():
			managers_found = []
			city = form.cleaned_data['city'].strip()
			state = form.cleaned_data['state'].strip()
			street = form.cleaned_data['address'].strip()
			zip = form.cleaned_data['zip']


			leases = Lease.objects.all()
			managers_found = []
			for lease in leases:
				building = Building.objects.get(pk=lease.building.building_id)
				address = Address.objects.get(pk=building)

				if (state == address.state.strip() or state == '*') and (city == address.city.strip() or city == '*')\
						and (city == address.city.strip() or city == '*') and (street == address.street.strip() or street == '*')\
						and (zip == str(address.zip) or zip == '*'):
					man = PropertyManager.objects.get(pk=lease.prop_man)
					managers_found.append(
						{
							'name': " ".join([man.first_name, man.last_name]),
							'phone': man.phone,
							'ssn': man.phone
						}
					)



		request.session['managers_search_address'] = json.dumps(managers_found)
		request.session.modified = True
		return redirect('manager_results_address')


	form = managerAddressSearchForm()
	return render(request, 'property_app/manager_search.html', {'form': form})


def manager_results_by_address(request):
	template_name = loader.get_template('property_app/manager_search_result_address.html')
	query = json.loads(request.session['managers_search_address'])

	table = managerInfoTable(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))

def manager_search_by_owner(request):
	if request.method == 'POST':
		form = ManagerOwnerSearchForm(request.POST)
		if form.is_valid():
			owner_first, owner_last = form.cleaned_data['owner'].strip().split()

			# get buildings owned by owner:
			client = Client.objects.get(first_name=owner_first,last_name=owner_last).ssn
			buildings = [i.building.building_id for i in Contract.objects.filter(ssn=client)]

			# get managers that manage any of those buildings:
			managers = []
			for building_id in buildings:
				ssn = Manages.objects.get(building=building_id).ssn
				manager = PropertyManager.objects.get(pk=ssn.strip())
				managers.append(
					{
						'name': " ".join([manager.first_name, manager.last_name]),
						'phone': manager.phone,
						'ssn': manager.ssn
					}
				)
			request.session['managers_search_owners'] = json.dumps(managers)
			request.session.modified = True
			return redirect('manager_results_owner')

	form = ManagerOwnerSearchForm()
	return render(request, 'property_app/manager_search.html', {'form': form})


def manager_results_by_owner(request):
	template_name = loader.get_template('property_app/manager_search_result_address.html')
	query = json.loads(request.session['managers_search_owners'])

	table = managerInfoTable(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))


def building_search(request):
	if request.method == 'POST':
		form = buildingSearchForm(request.POST)
		if form.is_valid():

			# get buildings owned by owner:
			found_building = form.cleaned_data['building'].strip()
			print(found_building)
			found_building = Building.objects.get(pk=found_building)

			# get managers that manage any of those buildings:
			unit_list = Unit.objects.all()
			#Lease_list = Lease.objects.get(building = found_building)
			totalRent=0
			numberOfUnits=0
			buildingInfo = []
			for x in unit_list:
				print(x.building.building_id)
				print(found_building.building_id)
				print('___________')
				if x.building.building_id == found_building.building_id:
					print(x)
					totalRent=totalRent + x.rent
					numberOfUnits += 1
			cost = Contract.objects.get(building = found_building).payment
			print(cost)
			buildingInfo.append(
				{
					'building_ID': str(found_building.building_id),
					'type': str(found_building.type),
					'floors':str(found_building.floors),
					'units' : str(numberOfUnits),
					'total_rent_amount': str(totalRent),
					'Building_cost' : str(cost)
				}
			)
			request.session['building_search_results'] = json.dumps(buildingInfo)
			request.session.modified = True
			return redirect('building_results')

	form = buildingSearchForm()
	return render(request, 'property_app/building_search.html', {'form': form})


def building_results(request):
	template_name = loader.get_template('property_app/building_search_results.html')
	query = json.loads(request.session['building_search_results'])

	table = BuildingInfo(query)
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))



def admin_page(request):
	email = request.POST.get('email2')
	password = request.POST.get('pass2')
	user = auth.sign_in_with_email_and_password(email, password)
	return render(request, 'property_app/adminPage.html')

def admin_sql_bar(request):

	if request.method == 'POST':

		form = AdminSQLForm(request.POST)

		if form.is_valid():
			result = []
			query = form.cleaned_data['query']
			cursor = connection.cursor()
			try:
				cursor.execute(query)
			except:
				return redirect('admin_sql')
			header = [i[0] for i in cursor.description]
			for row in cursor.fetchall():
				columns = {k: v for k, v in zip(header, [i for i in row])}
				for column in columns:
					if type(columns[column]) == Decimal:

						columns[column] = float(columns[column])
					if type(columns[column] == date):
						columns[column] = str(columns[column])
				result.append(columns)

			request.session['sql_results'] = json.dumps(result)
			request.session.modified = True
			return redirect('sql_results')

	form = AdminSQLForm()
	return render(request, 'property_app/admin_sql_bar.html', {'form': form})

def sql_results(request):
	template_name = loader.get_template('property_app/sql_results.html')
	query = json.loads(request.session['sql_results'])
	columns = query[0].keys()
	table = SQLResultsTable(query,extra_columns=[(column, tables.Column()) for column in columns])
	context = {'table': table}
	return (HttpResponse(template_name.render(context, request)))
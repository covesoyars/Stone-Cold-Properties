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
import pyrebase
from django.shortcuts import get_object_or_404

config = {
    'apiKey': "AIzaSyBIiU-vYyoHB3WqAkzgX9B2FtMzyKu9PSk",
    'authDomain': "database-258713.firebaseapp.com",
    'databaseURL': "https://database-258713.firebaseio.com/",
    'projectId': "database-258713",
    'storageBucket': "database-258713.appspot.com",
    'messagingSenderId': "225140590988",
    'appId': "1:225140590988:web:b5f4f273d0250782e6eea9"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()


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

    email = request.POST.get('email')
    password = request.POST.get('pass')
    user = auth.sign_in_with_email_and_password(email, password)

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
        sqft = tables.Column()

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

    class tenantInfoTable(tables.Table):
        name = tables.Column()
        phone = tables.Column()
        address = tables.Column()

    table = tenantInfoTable(query)
    context = {'table': table}
    return (HttpResponse(template_name.render(context, request)))


def property_manager_search(request):
    if request.method == 'POST':
        form = managerSearchForm(request.POST)
        if form.is_valid():
            managers_found = []
            city = form.cleaned_data['city'].strip()
            state = form.cleaned_data['state'].strip()
            street = form.cleaned_data['address'].strip()
            zip = form.cleaned_data['zip']
            tenant = form.cleaned_data['tenant'].strip()
            owner = form.cleaned_data['owner'].strip()
            first_name = form.cleaned_data['first_name'].strip()
            last_name = form.cleaned_data['last_name'].strip()
            level = form.cleaned_data['level']
            promotion = form.cleaned_data['expr']
            leases = Lease.objects.all()
            for x in leases:
                id = x.building.building_id

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
                        # (manager_object.first_name + " " + manager_object.last_name == manager or manager == '*') and
                        # (client.first_name + " " + client.last_name == owner or owner == '*') and
                        # (temp_tenant.first_name.strip() == first_name or first_name == '*') and
                        (temp_tenant.last_name.strip() == last_name or last_name == '*')):

                    found_manager = PropertyManager.objects.get(
                        pk=x.prop_man)
					# trying to pull from Level table but keeps saying canot use colum "id" but both the modles and database dont have a ID feild
                    # i also found this "Cannot resolve keyword 'level_level_exact' into field. Choices are: commission, id, level, salary, ssn, ssn_id
                    # WHERE IS SSN_ID AND ID COMMING FROM????/
                    #
                    # Level | CREATE TABLE `Level` (
                    # `level` decimal(1,0) NOT NULL,
                    # `salary` decimal(8,2) DEFAULT NULL,

                    # `commission` decimal(2,2) DEFAULT NULL,
                    # `SSN` char(11) DEFAULT NULL,
                    # KEY `SSN` (`SSN`),
                    # CONSTRAINT `Level_ibfk_1` FOREIGN KEY (`SSN`) REFERENCES `Property_Manager` (`SSN`)
                    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8
                    #
                    #straight from the database and no id or ssn_id to be found
                    # is there an on old file im not updating????
                    #
                    #

                    # found_level = Level.objects.all()
                    # for w in found_level:
                    #	if w.ssn == x.prop_man:
                    #		found_level2=w.level
                    # print(found_level2)
                    managers_found.append(
                        {
                            'name': " ".join([found_manager.first_name, found_manager.last_name]),
                            'phone': found_manager.phone,
                            'ssn': found_manager.ssn,
                            'start': str(found_manager.start_date),
                            'level': '3',  # found_level.level,
                            'salary': '23444'

                        }
                    )

            request.session['managers_search'] = json.dumps(managers_found)
            request.session.modified = True
            return redirect('manager_results')

    form = managerSearchForm()
    return render(request, 'property_app/manager_search.html', {'form': form})


def manager_results(request):
    template_name = loader.get_template('property_app/manager_search_result.html')
    query = json.loads(request.session['managers_search'])

    class managerInfoTable(tables.Table):
        name = tables.Column()
        phone = tables.Column()
        ssn = tables.Column()
        start_date = tables.Column()
        level = tables.Column()
        salary = tables.Column()

    table = managerInfoTable(query)
    context = {'table': table}
    return (HttpResponse(template_name.render(context, request)))

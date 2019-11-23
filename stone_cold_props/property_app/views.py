from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.template import loader

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

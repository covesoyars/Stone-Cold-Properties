from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from django.template import loader
from .search import searchForm


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
			type = form.cleaned_data['type']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			print(type, state, city)
	form = searchForm()
	return render(request, 'property_app/search.html', {'form': form})




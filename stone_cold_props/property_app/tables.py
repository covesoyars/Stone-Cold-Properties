import django_tables2 as tables

class managerInfoTable(tables.Table):
	name = tables.Column()
	phone = tables.Column()
	ssn = tables.Column()


class tenantInfoTable(tables.Table):
	name = tables.Column()
	phone = tables.Column()
	address = tables.Column()


class ExpiringContractTable(tables.Table):
	name = tables.Column()
	phone = tables.Column()
	building_id = tables.Column()
	address = tables.Column()
	pay = tables.Column()
	end = tables.Column()


class UnitTable(tables.Table):
	address = tables.Column()
	unit = tables.Column()
	rent = tables.Column()
	bathrooms = tables.Column()
	bedrooms = tables.Column()
	type = tables.Column()
	sqft = tables.Column()

class SQLResultsTable(tables.Table):
	static = tables.Column(visible=False)




class BuildingInfo(tables.Table):

	building_ID =  tables.Column()
	type =  tables.Column()
	floors = tables.Column()
	units =  tables.Column()
	total_rent_amount =  tables.Column()
	Building_cost = tables.Column()
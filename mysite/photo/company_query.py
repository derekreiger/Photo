# srs/company_query.py
# Model for Company records

#from django.contrib.auth.models import User
from os.path import join,exists
from os      import mkdir

from employee_query import add_employee 
from company_model  import Company
from mysite.settings   import BASE_DIR
from faker import fake_company, fake_ID_number

# Get a table listing from the database
def select_company(user=None):
    if user:
        return Company.objects.filter(user=user)
    else:
        return Company.objects.all()
    return [ f.values() for f in objects ]


# Get a table listing from the database
def query_company(user=None):
    return [ f.values() for f in select_company(user) ]


# Return a single contact
def get_company(user,id):
    a =  Company.objects.filter(pk=id)
    if len(a)==1:
        return a[0].table()


# Count the saved Company records
def count():
    return len(Company.objects.all())


# Print the object fields as a table
def print_company(company):
    for x in company.table():
        print '    %-10s:  %s' % (x[0],x[1])
    print


# Print the object list as a table
def print_list():
    all = Company.objects.all()
    print 'Company list:  %d records' % len(all)
    for c in all:
        print_company(c)


# Create company
def create_company(companyName,companyID,adminId,adminEmail):
    c = add_company([ companyName, companyID, None ])
    e = add_employee([adminId, 'Administrator', adminEmail, True, True, c, 'None'])
    e.isProvider = True
    e.isCompany  = True
    e.save()
    d = data_dir(c)
    if not exists(d):
        mkdir(d)
    return True


# Add a new record from a file
def add_company(data):
    o =  Company.objects.filter(name=data[0])
    if len(o)==1:
        c = o[0]
    else:
        c = Company()
    c.name, c.companyID, c.provider = data
    c.save()
    return c


# Add some fake Company records
def add_fake_company(num=1):
    for i in range(num):
        data = [ fake_company(), fake_ID_number(), None ]
        add_company(data)


# Test Company code
def test_company():
    return Company.objects.get(name='Impact QA')


# Look up the data location for this company
def data_dir(company):
    d = company.name.replace(' ','_').replace('/','_')
    d = join(BASE_DIR,'data','companies',d)
    return d

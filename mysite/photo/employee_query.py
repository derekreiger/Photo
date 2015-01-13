# srs/employee_query.py
# Model for Employee records

from django.contrib.auth.models import User
from random import choice

from employee_model import Employee
from company_model  import Company
from faker          import fake_ID_number,fake_first_name,fake_last_name,fake_email
#from notification_service import notify_newEmployee
from util.log            import append_log


# Return the employee record for the requested user
def me(request):
    return Employee.objects.get(user=request.user)

# Return the employee record for the requested user
def findEmployeeByEmail(email):
    o =  Employee.objects.filter(user__email=email)
    if len(o)==1:
        return o[0]
    return None

# Lookup the company for this user
def my_company(user):
    return Employee.objects.get(user=user).company


# Make sure there is one Test Robot user
def add_user(email):
    try:
        pw =  'x'
        user = User.objects.create_user(email, email, pw)
        user.is_staff = True
        user.save()
        return user
    except:
        append_log('error: user object already exists, '+email, 'srserror')
        return User.objects.get(username=email)


# Get a table listing from the database
def select_employee(user=None):
    if user:
        return Employee.objects.filter(user=user)
    else:
        return Employee.objects.all()
    return [ f.values() for f in objects ]


# Get a table listing from the database
def query_employee(user=None):
    return [ f.values() for f in select_employee(user) ]


# Return a single contact
def get_employee(user,id):
    a =  Employee.objects.filter(pk=id)
    if len(a)==1:
        return a[0].table()


# Count the saved Employee records
def count_employees():
    return len(Employee.objects.all())


# Print the object fields as a table
def print_employee(employee):
    for x in employee.table():
        print '    %-10s:  %s' % (x[0],x[1])
    print


# Print the object list as a table
def print_list(company=None):
    if company:
        all = Employee.objects.filter(company=company)
    else:
        all = Employee.objects.all()
    print 'Employee list:  %d records' % len(all)
    for c in all:
        print_employee(c)


# Remove the all employees from the database
def reset_list():
    from company_query  import test_company
    Employee.objects.filter(company=test_company()).delete()


# Add a new record from a file
def add_employee(data):
    newEmployee = False
    #print 'add employee :',data
    o =  Employee.objects.filter(employeeID=data[0],company=data[6])
    if len(o)==1:
        e = o[0]
        if not e.user.username == data[3]:
            e.user.username = data[3]
            e.user.email    = data[3]
            e.user.save()
    else:
        e = Employee()
        e.user = add_user(data[3])
        newEmployee = True

    e.employeeID, e.firstName, e.lastName, e.email, e.isManager, e.isActive, e.company = data[:7]
    e.name = e.firstName+' '+e.lastName
    if not e.screenName:
        e.screenName = e.name

    if len(data) > 7:  e.middleName = data[7]
    if len(data) > 8:  e.managerID  = data[8]
    if len(data) > 9:  e.department = data[9]
    if len(data) > 10: e.jobTitle   = data[10]
    if len(data) > 11: e.function   = data[11]
    if len(data) > 12: e.location   = data[12]
    if len(data) > 13: e.query1     = data[13]
    if len(data) > 14: e.query2     = data[14]
    if len(data) > 15: e.query3     = data[15]
    if len(data) > 16: e.query4     = data[16]

    e.save()

#    if newEmployee:
#        notify_newEmployee(e)
    return e


# Lookup the test user
def test_user():
    return User.objects.get(username='TestRobot@impactsrs.com')


# Add some fake Employee records
def add_fake_employee(num=1):
    for i in range(num):
        company = Company.objects.get(name='Impact QA')
        data = [ fake_ID_number(),  fake_first_name(), fake_last_name(),fake_email(), False, True, company ]
        add_employee(data)


# Select a random employee
def random_employee():
    from company_query  import test_company
    return choice(Employee.objects.filter(company=test_company()))


# Test Employee code
def fix_employee_names():
    for e in Employee.objects.all():
        if not e.firstName or not e.lastName and e.name:
            print 'first:%s last:%s name:%s'%(e.firstName, e.lastName, e.name)
            s = e.name.split(' ')
            if len(s)==2:
                e.firstName = s[0]
                e.lastName  = s[1]
            else:
                print "error: Bad file name"
                append_log('error: first:%s last:%s name:%s'%\
                           (e.firstName, e.lastName, e.name),'srserror')


# Detect any employee that has a loop in the manager chain
def is_manager_loop(e):
    for i in range(10):
        if not e:
            return False
        e = e.manager
    return True


# Check all records for manager loops
def check_manager_list():
    for e in Employee.objects.all():
        if e.managerID:
            e.manager =  Employee.objects.get(company=e.company,employeeID=e.managerID)
            print "Set Company:%s, ID:%s, Name:%s, Manager:%s" %(e.company,e.employeeID,e.name,e.manager)
            e.manager = None
            e.save()
    for e in Employee.objects.all():
        if is_manager_loop(e):
            print 'LOOP:  employee: %s, manager: %s'%(e.name,e.manager.name)
            e.manager = None
            e.managerID = None
            e.save()
        # else:
        #     print 'employee: %d, manager: %s'%(e.pk,e.manager)
        #     print 'No Loop'


# Test Employee code
def test_employee():
    fix_employee_names()
    check_manager_list()
    return Employee.objects.get(user=test_user())


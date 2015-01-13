from django.contrib.auth.decorators import login_required
from django.forms       import ModelForm
from django.http        import HttpResponseRedirect,HttpResponse
from django.shortcuts   import render
from django.template    import Context,RequestContext,loader
from os                 import listdir,remove
from os.path            import isfile,join
from time               import sleep

from photo_model        import Photo
from employee_model     import Employee
from app.settings       import BASE_DIR
from glob import glob

# Form to add a new photo
class PhotoForm (ModelForm):
    class Meta:
        model=Photo


# Create the view for the details
def display_form (request, context, instance):

    if request.method == 'POST':
        if not request.POST.get('cancel', None):
            form = PhotoForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                me = form.instance.employee
                remove_photo (me)
                form.save()
                me.photo = my_photo(me)
                me.thumbnail = me.photo.replace('.','-tn.')
                me.save()
                sleep(3)
                return HttpResponseRedirect('/photo') 
    else:
        form = PhotoForm(instance=instance) 

    context['form'] = form
    return render(request,  'photo.html', context)

# Lookup my company name
def my_company(me):
    return me.company.name.replace(' ','_').replace('/','_')

# Get the image name that matches
def my_photo(me):
    directory = join(BASE_DIR,'data','companies',my_company(me),'photos')
    employeeID = me.employeeID
    files =  filter(isfile, glob (join (directory, employeeID+".*")))
    if len(files)>0:
        return files[0].replace(join(BASE_DIR,'data','companies/'), '')
    else:
        return 'blank.jpg'


# Remove previous image
def remove_photo (me):
    p = my_photo(me)
    if p!='blank.jpg':
        p = join(BASE_DIR,'data','companies',p)
        remove (p)


# Show the existing photos and a form to replace mine
@login_required
def photo_view (request): 
    me = Employee.objects.get(user=request.user)
    i  = Photo()
    i.employee = me
    photo      =  my_photo(me)
    photo_url  = join('/photos',photo)
    photo_path = join(BASE_DIR,'data','companies',photo)
    context =  {
        'title'    : 'New Profile Image', 
        'instance' : i,
        'employee' : me,
        'photo'    : photo_url,
        'path'     : photo_path,
    }
    return display_form(request,context,i)


from django.conf     import settings
from django.db       import models
from django.forms    import ModelForm
from os.path         import splitext,join,exists
from os              import remove,mkdir
from PIL             import Image

from employee_model  import Employee
from company_query   import data_dir
from mysite.settings import PHOTOS_DIR,BASE_DIR
from util.log        import append_log


# Model for photos
class Photo(models.Model):

    image    = models.ImageField(upload_to=PHOTOS_DIR, \
                                 help_text='Images above 200x200 will be resized.')
    thumb    = models.ImageField(upload_to=PHOTOS_DIR, editable=False)
    employee = models.ForeignKey (Employee, related_name='profile_photo', editable=False)

    # String of photo is title
    def __unicode__(self):
        return  str(self.image)

    # Form the file name for the image
    def filename (self):
        return  str(self.image)

    # Location to store photos for this employee
    def photo_dir (self):
        company_name = self.employee.company.name.replace(' ','_').replace('/','_')
        d = join(BASE_DIR,'data','companies',company_name,'photos')

        if not exists(d): 
            mkdir(d)

        return d

    # Location to store photos for this employee
    def photo_path (self):
        fn,ext = splitext(self.filename())
        employeeID   = self.employee.employeeID
        return join(self.photo_dir(), employeeID+ext)

    # Limit the size of the original and create a thumbnail.
    def save(self, force_insert=False, force_update=False):
        super(Photo, self).save(force_insert, force_update)

        if self.image:
            photo = self.photo_path ()
            infile = join(PHOTOS_DIR, self.filename())
            create_thumbnails(infile, photo)
            super(Photo, self).save(force_insert, force_update)

# Save image file after resize
def save_image_file(filename, image, width, height, imtype):
    append_log("Photo Upload : %s, %d x %d "%(filename, width, height),'photos')
    max_size = width, height
    if image.size > max_size:
        image.thumbnail(max_size, Image.ANTIALIAS)
    image.save (filename, imtype)
    return image

# Create a small and large rendering of this image
def create_thumbnails(infile, photo):
        
    try:
        fn,ext = splitext(photo)
        tn     = fn + "-tn" + ext
        image  = Image.open(infile)
        remove(infile)
        imtype = ext.replace('.jpg','JPEG').replace('.png','PNG')
        save_image_file(photo, image, 300, 300, imtype)
        save_image_file(tn, image, 50, 50, imtype)
        append_log("Photo Upload Successful, "+photo,'photos')

    except IOError:
        append_log("error: cannot create thumbnails for '%s'" % infile,'photos')


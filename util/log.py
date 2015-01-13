# Read and write a system log file

from os import remove
from os.path import join,dirname
from datetime import datetime

from files import read_text,list_files
from settings import LOG_DIR


# Setup the file name
def log_file(logFile):
    return join(LOG_DIR, logFile+'.log')


# Log the page hit in page.log  (time, ip, user, page, doc) 
def append_log(doc, filename='page'):
    f=open(log_file(filename),'a')
    f.write(str(datetime.now())+',  '+doc+'\n')
    f.close()


# Log the page hit in page.log  (time, ip, user, page, doc) 
def log_page(request,title=None):
    if not request or request.user.is_anonymous():
         append_log('Anonymous '+str(title))
    else:
         append_log(request.user.username+' '+str(title))


# Get the contents of a log file
def show_log(filename='page'):
    return read_text(log_file(filename))


# Get the contents of a log file
def list_logs():
    d = join(dirname(BASE_DIR), 'logs')
    for f in list_files(d):
        f = f.replace('.log','')
        log = show_log(f)
        print len(log.split('\n')), log_file(f)


# Get the contents of a log file
def clear_logs():
    d = join(dirname(BASE_DIR), 'logs')
    for f in list_files(d):
        f = f.replace('.log','')
        print 'remove', log_file(f)
        remove(log_file(f))

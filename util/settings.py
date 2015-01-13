from os.path import join,dirname

# Location of mysite directory
# TODO change the "mysite" directory to "app"
BASE_DIR    = dirname(dirname(dirname(__file__)))
LOG_DIR     = join(BASE_DIR, 'mysite', 'logs')
DOC_ROOT    = join(BASE_DIR, 'mysite', 'user_doc')
SCRIPTS_DIR = join(BASE_DIR, 'mysite', 'scripts')

from random  import choice, randrange
from os      import environ,mkdir,getenv
from os.path import exists
from django.contrib.auth.models import User
from mysite.settings import BASE_DIR

# // JS random selection

# function choose(choices) {
#   var index = Math.floor(Math.random() * choices.length);
#   return choices[index];
# }


# Read in a data file for generating a type of fake data
def read_lines(f):
    return open(BASE_DIR+'/data/faker/'+f).read().split('\n')[:-1]


# Select from a list of choices
def pick(selections):
    return selections[randrange(len(selections))]

# Pick a few random digits
def pick_digits(digits=4):
    return ''.join([ str(randrange(10)) for i in range(digits) ])


# Fake praise
def fake_praise():
    return pick(praise)

# Fake names
def fake_name():
    return pick(first) +' ' + pick(last)

# Fake names
def fake_first_name():
    return pick(first)

# Fake names
def fake_last_name():
    return pick(last)

# Fake ID numbers
def fake_ID_number():
    return  pick_digits()

# Fake ID numbers
def fake_phone_number():
    return  pick_digits(3) +'-'+ pick_digits(3) +'-'+ pick_digits()

# Fake address
def fake_address():
    return fake_ID_number() +' '+ pick(streets) + ' Ave'

# Fake email
def fake_email():
    return pick(last) +'.'+ fake_ID_number() +'@fake.org'

# Company names
def fake_company():
    return pick(adjectives) +' '+  pick(adjectives) +' '+  pick(nouns)

# Comment
def fake_comment():
    return pick(comment) +' '+  pick(comment)

# Idea
def fake_idea():
    return pick(ideas) +' '+  pick(ideas)

# Award
def fake_award():
    return pick(awards)

first       = read_lines('first_names')
last        = read_lines('last_names')
adjectives  = read_lines('adjectives')
nouns       = read_lines('nouns')
streets     = read_lines('streets')
praise      = read_lines('praise')
comment     = read_lines('comment')
ideas       = read_lines('ideas')
awards      = read_lines('awards')

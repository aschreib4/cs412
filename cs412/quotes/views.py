from django.shortcuts import render

from django.http import HttpRequest, HttpResponse #new

import time #new
import random #new

quotes = [
    "Food is maybe the only universal thing that really has the power to bring everyone together.",
    "Flavortown is a mythical place, a state of mind, where fun and food meet in perfect harmony.",
    "This is the flavor temple. I want to lay down in it.",
    "It's never too late to get good at something.",
    "Peace, love, and taco grease!"

]

images = [
    "https://i.insider.com/61293c5712b9cc0019633149?width=800&format=jpeg&auto=webp",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSR_eQSTYLY8tmg7DBsbkRYb4vHkD35jvWuNQ&s",
    "https://cdn.sobewff.org/wp-content/uploads/2024/07/fieri_guy_2024.jpg?strip=all&lossy=1&quality=92&webp=92&ssl=1",
    "https://media.gq.com/photos/59dfc6d9d61cb80476584e18/4:3/w_1600%2Cc_limit/guy-fieiri-flame.jpg",
    "https://www.ocregister.com/wp-content/uploads/migration/kpl/kpl7ri-17fieri2.jpg?w=620"
]

# Create your views here.

def home(request):
    '''Fund to respond to the "home" request.'''

    response_text = f'''
    <html>
    <h1>Hello, world!</h1>
    The current time is {time.ctime()}.
    </html
    '''

    return HttpResponse(response_text)

def quote(request):
    '''Respond to the URL '', delegate work to a template.'''
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    template_name = 'quotes/quote.html'
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
        'random_quote': random_quote,
        'random_image': random_image
        
    }
    return render(request, template_name, context)

def base(request):
    '''Respond to the URL 'base', delegate work to a template.'''

    template_name = 'quotes/base.html'
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
    }
    return render(request, template_name, context)

def about(request):
    '''Respond to the URL 'about', delegate work to a template.'''

    template_name = 'quotes/about.html'
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
    }
    return render(request, template_name, context)

def show_all(request):
    '''Respond to the URL 'show_all', delegate work to a template.'''

    template_name = 'quotes/show_all.html'
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
    }
    return render(request, template_name, context)

'''
def display_random_quote_and_image(request):

    random_quote = random.choice(quotes)
    random_image = random.choice(images)

    template_name = 'quotes/quote.html'
    
    context = {
        'random_quote': random_quote,
        'random_image': random_image
    }
    return render(request, template_name, context)
'''
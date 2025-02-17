## restaurant/views.py
## views for the 'restaurant' app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse #new

import time #new
import random #new
from decimal import Decimal

# Create your views here.

def main(request):
    '''Show the main page to the user'''

    template_name = 'restaurant/main.html'
    return render(request, template_name)

MENU_ITEMS = [
    {'name': 'Hamburger', 'price': 14.00, 'options': ['BBQ', 'Cheese', 'Bacon']},
    {'name': 'Mac n Cheese', 'price': 8.50, 'options': None},
    {'name': 'Pizza', 'price': 4.00, 'options': ['Cheese', 'Pepperoni', 'Pineapple']},
    {'name': 'Chili Cheese Dog', 'price': 7.00, 'options': None}
]

DAILY_SPECIALS = [
    {'name': 'Taco Salad', 'price': 9.50, 'options': None, 'details': 'Everything you love in a taco--as a salad.'},
    {'name': 'Burrito', 'price': 8.00, 'options': None, 'details': 'Meat, cheese, veggies, and everything else you want in a tortilla.'},
    {'name': 'Quesadilla', 'price': 4.00, 'options': None, 'details': 'Tortilla, cheese, and whatever else you please!'}
]

def order(request):
    '''Show the form to the user'''

    dailySpecial = random.choice(DAILY_SPECIALS)

    context = {
        'menu_items': MENU_ITEMS,
        'daily_special': dailySpecial
    }

    template_name = 'restaurant/order.html'
    return render(request, template_name, context)

def confirmation(request):
    '''Process the form submission, and generate a result.'''

    template_name = 'restaurant/confirmation.html'
    #print(request.POST)

    if request.POST:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_instructions = request.POST['special_instructions']
        current_time = time.time()
        randomMinutes = random.randint(30, 60)
        readyTimeTimestamp = current_time + (randomMinutes * 60)
        readyTimeReadable = time.localtime(readyTimeTimestamp)
        readytime = time.strftime('%I:%M %p', readyTimeReadable)

        ordered_items = []
        total_price = Decimal('0.00')

        for item in MENU_ITEMS:
            if item['name'] in request.POST.getlist('order_items'):
                selected_options = request.POST.getlist(f'{item["name"]}_options')
                #ordered_items.append(item['name'])
                ordered_items.append({
                    'name': item['name'],
                    'price': item['price'],
                    'options': selected_options if selected_options else None
                })
                total_price += Decimal(str(item['price']))
        
        for items in DAILY_SPECIALS:
            if items['name'] in request.POST.getlist('daily_special'):
                selected_options2 = request.POST.getlist(f'{items["name"]}_options')
                #ordered_items.append(items['name'])
                ordered_items.append({
                    'name': items['name'],
                    'price': items['price'],
                    'options': selected_options2 if selected_options2 else None
                })
                total_price += Decimal(str(items['price']))

        context = {
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions,
            'ordered_items': ordered_items,
            'total_price': total_price,
            'readytime': readytime,
        }

    return render(request, template_name, context)


from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
from catalog.models import CakeOfTheDay
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
from accounts.models import UserAccount
# Create your views here.
def Index(request):
	user = request.user
	if user.is_active == False:
		logout(request)
	localities = Locality.objects.exclude(locality_name="All").filter(status=True)
	sub_localities = Sub_Locality.objects.all()
	template = "index.html"
	site_name = "Order cakes online in Mumbai and Thane"
	context = {
	"localities":localities,
	"sub_localities":sub_localities,
	"site_name": site_name
	}
	return render(request, template, context)

def About(request):
	template = "core/about.html"
	site_name = "About Cakemporos"
	context = {
	"site_name": site_name
	}
	return render(request, template, context)

def Terms(request):
	template = "core/tnc.html"
	site_name = "Terms & Conditions of Cakmeporos"
	context = {
	"site_name": site_name
	}
	return render(request, template, context)

def Privacy(request):
	template = "core/privacy.html"
	site_name = "Privacy Policy of Cakemporos"
	context = {
	"site_name": site_name
	}
	return render(request, template, context)

def Contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		# for key, value in form.cleaned_data.iteritems():
		# 	print key, value
		# 	#print form.cleaned_data.get(key)
		form_email = form.cleaned_data.get("email")
		form_message = form.cleaned_data.get("message")
		form_full_name = form.cleaned_data.get("full_name")
		# print email, message, full_name
		subject = 'Cakemporos Support'
		from_email = "support@cakemporos.in"
		to_email = [from_email, 'nikhil.salome@gmail']
		contact_message = "%s: %s via %s"%( 
				form_full_name, 
				form_message, 
				form_email)
		some_html_message = """
		<h1>hello</h1>
		"""
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				html_message=some_html_message,
				fail_silently=True)
	template = "core/contact.html"
	site_name = "Contact Us"
	context = {
	"site_name": site_name,
	"form":form,
	}
	return render(request, template, context)

def Delivery(request):
	template = "core/delivery.html"
	site_name = "Cakemporos Logistics"
	context = {
	"site_name": site_name
	}
	return render(request, template, context)

def Corporate(request):
	template = "core/corporate.html"
	site_name = "Corporate Offers"
	context = {
	"site_name": site_name
	}
	return render(request, template, context)

def offers_page(request):
	template = "core/offers.html"
	site_name = "Special Offers"
	offers = Offers.objects.filter(status=True)
	context = {
	"site_name": site_name,
	"offers":offers,
	}
	return render(request, template, context)

def Cake_Of_The_Day(request):
	cake_of_the_day = CakeOfTheDay.objects.all()
	template = "core/cake_of_the_day.html"
	site_name = "Cake of The Day"
	context = {
	"cake_of_the_day": cake_of_the_day,
	"site_name": site_name
	}
	return render(request, template, context)

def F_A_Q(request):
	faq = FAQ.objects.all()
	template = "core/faq.html"
	site_name = "Frequently Asked Question"
	context = {
	"faq": faq,
	"site_name": site_name
	}
	return render(request, template, context)

def RewardPage(request):
	user = request.user
	useraccount = UserAccount.objects.get(user=user)
	template = "core/reward.html"
	site_name = "Share reward code with friends"
	context = {
	"site_name": site_name,
	"useraccount": useraccount,
	}
	return render(request, template, context)

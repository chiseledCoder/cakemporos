import operator
import re
import urllib
import pprint
import logging
import datetime
import requests
import simplejson
from datetime import datetime, date
from operator import itemgetter, attrgetter
from django.http import JsonResponse
from django.shortcuts import render, render_to_response, HttpResponseRedirect, Http404, HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.timezone import datetime, timedelta

# Create your views here.
def mycakebox_baker_book(request):
	template = "mycakebox_baker/book.html"
	return render(request, template)

def get_distance(request):
	distance_data ={}
	if request.method == "POST" and request.is_ajax:
		if 'autocomplete' not in request.POST:
			destination = "Mumbai, Maharashtra"
		else:
			destination = request.POST['autocomplete']
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=Rutu Park, Panchsheel Nagar, Thane West, Thane, Maharashtra 400601, India&destinations="+destination+"&key=AIzaSyCRcKLBQYizfeHi8fc1GzihE5TK4KTOYEY"
		googleResponse = urllib.urlopen(url)
		jsonResponse = simplejson.loads(googleResponse.read())
		print "Origin: "+ jsonResponse['origin_addresses'][0]
		print "Destination: "+ jsonResponse['destination_addresses'][0]
		print "Distance: "+ jsonResponse['rows'][0]['elements'][0]['distance']['text']
		print "Duration: "+ jsonResponse['rows'][0]['elements'][0]['duration']['text']
		distance_data['origin'] = jsonResponse['origin_addresses'][0]
		distance_data['destination'] = jsonResponse['destination_addresses'][0]
		distance_data['distance'] = jsonResponse['rows'][0]['elements'][0]['distance']['text']
		distance_data['duration'] = jsonResponse['rows'][0]['elements'][0]['duration']['text']
		return HttpResponse(JsonResponse(distance_data))
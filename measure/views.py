from django.shortcuts import render, get_object_or_404
from .models import Measure
from .forms import MeasureModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_center_cordinates, get_zoom, get_ip_address
import folium


def distance_calculate_view(request):
    distance = None
    destination = None
    obj = get_object_or_404(Measure, id=1)
    form = MeasureModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measure')

    ip_ = get_ip_address(request)
    print(ip_)
    ip = '103.28.86.193'
    country, city, lat, lon = get_geo(ip)

    location = geolocator.geocode(city)

    # Location Cordinates
    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    # Initial Folium map Setup
    m = folium.Map(width=1100, height=600, location=get_center_cordinates(l_lat, l_lon), zoom_start=2)
    # location Marker
    folium.Marker([l_lat, l_lon], tooltip='click here for more', popup=city['city'],
                  icon=folium.Icon(color='purple')).add_to(m)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        # Destinates Coordinates
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB = (d_lat, d_lon)

        # Distance Calculation
        distance = round(geodesic(pointA, pointB).km, 2)

        # Map Modifications
        m = folium.Map(width=1100, height=600, location=get_center_cordinates(l_lat, l_lon, d_lat, d_lon),
                       zoom_start=get_zoom(distance))
        # location Marker
        folium.Marker([l_lat, l_lon], tooltip='this is your location', popup=city['city'],
                      icon=folium.Icon(color='purple')).add_to(m)
        # Destination Marker
        folium.Marker([d_lat, d_lon], tooltip='this is your destination', popup=destination,
                      icon=folium.Icon(color='red', icon='cloud')).add_to(m)

        # Draw a line
        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color='blue')
        m.add_child(line)
        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()

    context = {
        'distance': distance,
        'destination': destination,
        'form': form,
        'map': m
    }
    return render(request, 'measures/index.html', context)

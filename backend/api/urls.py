from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EarthquakeViewSet, EarthquakeStatsView, update_earthquakes

router = DefaultRouter()
router.register(r'earthquakes', EarthquakeViewSet, basename='earthquake')

urlpatterns = [
    # Stats endpoint
    path('earthquakes/stats/', EarthquakeStatsView.as_view(), name='earthquake-stats'),
    # Update endpoint to trigger XML fetch and parse
    path("earthquakes/update/", update_earthquakes, name="update-earthquakes"),
    # Earthquake endpoints
    path('', include(router.urls)),
]

    # DefaultRouter automatically creates endpoints for the Earthquake model:

    # GET /earthquakes/ → list all earthquakes

    # GET /earthquakes/<id>/ → retrieve a single earthquake

    # POST /earthquakes/ → create a new earthquake

    # PUT /earthquakes/<id>/ → update an existing one

    # DELETE /earthquakes/<id>/ → delete an earthquake

    # The stats endpoint is at /earthquakes/stats/
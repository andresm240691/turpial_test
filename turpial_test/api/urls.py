from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pokemons', views.PokemonViewSet,basename="pokemons")


urlpatterns = [
   path('', include(router.urls)),
    
]
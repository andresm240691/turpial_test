from . import views as api_views
from django.urls import path
from rest_framework.authtoken import views


urlpatterns = [
   path('login/', views.obtain_auth_token),
   path('pokemons', api_views.PokemonsListView.as_view()),
   path('pokemons/<int:pk>', api_views.PokemonsDetailView.as_view()),
   path('pokemons/own/', api_views.PokemonsOwnCRViewSet.as_view()),
   path('pokemons/own/<int:pk>', api_views.PokemonOwnRUDView.as_view()),
   path('pokemons/own/party/', api_views.PokemonOwnParty.as_view()),
   path('pokemons/own/swap/', api_views.PokemonOwnSwap.as_view()),
   path('regions', api_views.RegionListView.as_view()),
   path('regions/<int:pk>', api_views.RegionDetailView.as_view()),
   path('location/<int:pk>', api_views.LocationDetail.as_view()),
]
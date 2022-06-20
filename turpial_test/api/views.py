from rest_framework import viewsets
from .serializers import PokemonListSerializer
from .models import Pokemon


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonListSerializer

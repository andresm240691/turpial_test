from .serializers import (
    PokemonListSerializer,
    PokemonPartySerializer,
    PokemonPartyInSerializer
)
from .models import (
    Pokemon,
    PokemonParty
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView
)


class PokemonsListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Pokemon.objects.all()
    serializer_class = PokemonListSerializer


class PokemonsDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Pokemon.objects.all()
    serializer_class = PokemonListSerializer


class PokemonsOwnCRViewSet(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PokemonParty.objects.all()
    serializer_class = PokemonPartySerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user, is_party_member=True).all()[:6]

    def create(self, request, *args, **kwargs):
        try:
            in_pokemon_party = PokemonPartyInSerializer(data=request.data)
            if in_pokemon_party.is_valid():
                data = in_pokemon_party.data
                specie = Pokemon.objects.get(id=data.get('specie'))
                if specie:
                    data.update(user=self.request.user, specie=specie)
                    pp = PokemonParty(**data)
                    pp.save()
                    return Response(status=201, data=PokemonPartySerializer(pp).data)
                else:
                    return Response(status=400, data={'message': 'Specie does not exist'})
            else:
                return Response(status=400, data=in_pokemon_party.errors)
        except Exception as e:
            return Response(status=400, data={'message': str(e)})


class PokemonOwnRUDView(UpdateAPIView,
                        DestroyAPIView,
                        RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PokemonParty.objects.all()
    serializer_class = PokemonPartySerializer

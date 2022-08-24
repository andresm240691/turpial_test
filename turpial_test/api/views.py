from .serializers import (
    PokemonListSerializer,
    PokemonPartySerializer,
    PokemonPartyInSerializer,
    PokemonPartyDetailSerializer,
    RegionListSerializer,
    RegionDetailSerializer,
    LocationDetailSerializer,
    AreaCustomDetailSerializer,
)
from .models import (
    Pokemon,
    PokemonParty,
    Region,
    Location,
    Area
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView


class PokemonsDetailView(RetrieveAPIView):
    """  Pokemon specie detail """
    permission_classes = (IsAuthenticated,)
    queryset = Pokemon.objects.all()
    serializer_class = PokemonListSerializer


class PokemonsOwnCRViewSet(ListCreateAPIView):
    """ Pokemon Storage / Pokemon catch """
    permission_classes = (IsAuthenticated,)
    queryset = PokemonParty.objects.all()
    serializer_class = PokemonPartySerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            is_party_member=True
        ).all()[:6]

    def create(self, request, *args, **kwargs):
        try:
            count_pokemons = PokemonParty.objects.filter(
                user=self.request.user)
            if count_pokemons.count() <= 6:
                in_pokemon_party = PokemonPartyInSerializer(
                    data=request.data)
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
            return Response(status=200, data={'message': 'You can only have 6 pokemon'})
        except Exception as e:
            return Response(status=400, data={'message': str(e)})


class PokemonOwnRUDView(UpdateAPIView,
                        DestroyAPIView,
                        RetrieveAPIView):
    """ Pokemon rename / Pokemon release """
    permission_classes = (IsAuthenticated,)
    queryset = PokemonParty.objects.all()
    serializer_class = PokemonPartySerializer


class PokemonOwnParty(ListCreateAPIView):
    """ Pokemon party """
    permission_classes = (IsAuthenticated,)
    queryset = PokemonParty.objects.all()
    serializer_class = PokemonPartyDetailSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user,
            is_party_member=True
        ).all()[:6]


class PokemonOwnSwap(APIView):
    """  PokemonOwnSwap """
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            data = self.request.data
            if data.get('entering_the_party'):
                pp_member = PokemonParty.objects.get(pk=data.get(
                    'entering_the_party'))
                pp_member.is_party_member = True
                pp_member.save()
            if data.get('leaving_the_party'):
                pp_leaving = PokemonParty.objects.get(pk=data.get(
                    'leaving_the_party'))
                pp_leaving.is_party_member = False
                pp_leaving.save()
            all_pp = PokemonParty.objects.filter(
                user=self.request.user,
                is_party_member=True
            ).all()[:6]
            return Response(status=200, data=PokemonPartyDetailSerializer(
                all_pp, many=True).data)
        except Exception as e:
            return Response(status=400, data={'message': str(e)})


class RegionListView(ListAPIView):
    """ Regions list """
    permission_classes = (IsAuthenticated,)
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer


class RegionDetailView(RetrieveAPIView):
    """ Regions detail """
    permission_classes = (IsAuthenticated,)
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer


class LocationDetailView(RetrieveAPIView):
    """ Location detail """
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer


class AreaDetailView(RetrieveAPIView):
    """ Area detail """
    permission_classes = (IsAuthenticated,)
    queryset = Area.objects.all()
    serializer_class = AreaCustomDetailSerializer

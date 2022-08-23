from rest_framework import serializers
from api.models import (
    Pokemon, 
    Move, 
    Stat,
    Type,
    Area,
    Ability,
    Location,
    Region,
    PokemonParty
)
from django.db.models.functions import Lower


class MoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Move
        fields = '__all__'


class StatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stat
        fields = [
            'id',
            'name',
            'value'
        ]


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=150)
    pokemons = serializers.ListField(
        child=serializers.CharField(max_length=150))

    class Meta:
        model = Area
        fields = [
            'id',
            'name',
            'location',
            'pokemons'
        ]

    def create(self, validated_data):
        location = validated_data.pop('location')
        pokemons = validated_data.pop('pokemons')
        area = Area(**validated_data)

        location_query = Location.objects.annotate(
            name_lower=Lower('name')).filter(
            name_lower__icontains=location).first()
        if not location_query:
            location_query = Location(name=location)
            location_query.save()

        area.location_id = location_query.id
        area.save()
        pokemons_query = Pokemon.objects.annotate(
            name_lower=Lower('name')).filter(
            name_lower__in=pokemons).all()
        area.pokemon.set(pokemons_query)
        area.save()
        return area


class RegionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = [
            'id',
            'name',
        ]


class LocationDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['name']


class RegionDetailSerializer(RegionListSerializer):

    locations = LocationDetailSerializer(
        read_only=True, allow_null=True, many=True)

    class Meta(RegionListSerializer.Meta):
        model = Region
        fields = [
            'id',
            'name',
            'locations'
        ]


class RegionSerializer(serializers.ModelSerializer):
    locations = serializers.ListField(
        child=serializers.CharField(max_length=150)
    )

    class Meta:
        model = Region
        fields = [
            'id',
            'name',
            'locations',
        ]

    def create(self, validated_data):
        locations = validated_data.pop('locations')
        region = Region(**validated_data)
        region.save()
        locations_list = []
        for location in locations:
            location_query = Location.objects.annotate(
                name_lower=Lower('name')).filter(
                name_lower__icontains=location).first()
            if not location_query:
                location_query = Location(name=location)
                location_query.save()
            locations_list.append(location_query)
        region.locations.set(locations_list)
        return region


class AreaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


class AbilitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ability
        fields = '__all__'


class PokemonSerializer(serializers.ModelSerializer):

    moves = serializers.ListField(
        child=serializers.CharField(max_length=150)
    )
    stats = StatSerializer(many=True)
    types = serializers.ListField(
        child=serializers.CharField(max_length=150)
    )
    abilities = serializers.ListField(
        child=serializers.CharField(max_length=150),
    )

    class Meta:
        model = Pokemon
        fields = '__all__'

    def create(self, validated_data):
        moves = validated_data.pop('moves')
        stats = validated_data.pop('stats')
        types = validated_data.pop('types')
        abilities = validated_data.pop('abilities')
        pokemon = Pokemon(**validated_data)
        pokemon.save()
        
        for item in moves:
            mv = Move.create(item)
            if mv:
                pokemon.moves.add(mv)

        for item in stats:
            stat = Stat.create(item)
            if stat:
                pokemon.stats.add(stat)

        for item in types:
            new_type = Type.create(item)
            if new_type:
                pokemon.types.add(new_type)
        
        for item in abilities:
            ability = Ability.create(item)
            if ability:
                pokemon.abilities.add(ability)

        pokemon.save()
        return pokemon

    
class PokemonListSerializer(serializers.ModelSerializer):

    stats = StatSerializer(many=True, read_only=True)
    moves = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()
    abilities = serializers.SerializerMethodField()

    def get_moves(self, obj):
        return [item.name for item in obj.moves.all()]

    def get_abilities(self, obj):
        return [item.name for item in obj.abilities.all()]

    def get_types(self, obj):
        return [item.name for item in obj.types.all()]

    class Meta:
        model = Pokemon
        fields = [
            'id',
            'color',
            'capture_rate',
            'height',
            'name',
            'weight',
            'flavor_text',
            'sprites',
            'abilities',
            'moves',
            'stats',
            'types',
        ]


class RegionsSerializer(serializers.ModelSerializer):
    areas = serializers.ListField(
        child=serializers.CharField(max_length=150)
    )
    region = serializers.CharField(max_length=150)

    class Meta:
        model = Region
        fields = [
            'id',
            'areas',
            'region',
            'name'
        ]

    def create(self, validated_data):
        region = validated_data.pop('region')
        areas = validated_data.pop('areas')
        location = Location(**validated_data)
        return location


class PokemonDetailSerializer(serializers.ModelSerializer):

    moves = MoveSerializer(read_only=True, many=True)
    stats = StatSerializer(read_only=True, many=True)
    types = TypeSerializer(read_only=True, many=True)
    abilities = AbilitiesSerializer(read_only=True,many=True)

    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = PokemonParty
        fields = '__all__'


class PokemonPartyInSerializer(serializers.Serializer):
    specie = serializers.IntegerField(required=True)
    nick_name = serializers.CharField(required=True)
    is_party_member = serializers.BooleanField(required=True)


class PokemonPartyDetailSerializer(serializers.ModelSerializer):

    specie = PokemonDetailSerializer(
        read_only=True, allow_null=True)

    class Meta:
        model = PokemonParty
        fields = (
            'id',
            'specie',
            'nick_name',
            'is_party_member'
        )


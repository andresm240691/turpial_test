from rest_framework import serializers
from api.models import (
    Pokemon, 
    Move, 
    Stat,
    Type,
    Area,
    Ability
)

class MoveSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Move
        fields = '__all__'

class StatSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Stat
        fields = '__all__'

class TypeSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = '__all__'

class AreaSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'

class AbilitiesSerialzier(serializers.ModelSerializer):

    class Meta:
        model = Ability
        fields = '__all__'


class PokemonSerializer(serializers.ModelSerializer):

    moves = serializers.ListField(
        child = serializers.CharField(max_length=150)
    )
    stats = StatSerialzier(many=True)
    types = serializers.ListField(
        child = serializers.CharField(max_length=150)
    )
    abilities = serializers.ListField(
        child = serializers.CharField(max_length=150),
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
            ability = Type.create(item)
            if ability:
                pokemon.types.add(ability)

        return pokemon

    
    
class PokemonListSerializer(serializers.ModelSerializer):

    
    moves = serializers.ListField(
        child = serializers.CharField(max_length=150)
    )
    stats = StatSerialzier(many=True)
    types = serializers.ListField(
        child = serializers.CharField(max_length=150)
    )
    abilities = serializers.ListField(
        child = serializers.CharField(max_length=150),
    )



    class Meta:
        model = Pokemon
        fields = '__all__'
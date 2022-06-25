from django.db import models


# Create your models here.
class Ability(models.Model):
    name = models.CharField(max_length=150,  unique=True)

    @classmethod
    def create(cls, str_name):
        obj = Ability.objects.filter(name=str_name)
        if not obj.exists():
            new_item = cls(name=str_name)
            new_item.save()
            return new_item
        return obj.first()


class Move(models.Model):
    name = models.CharField(max_length=150,  unique=True)
    
    @classmethod
    def create(cls, str_name):
        obj = Move.objects.filter(name=str_name)
        if not obj.exists():
            new_item = cls(name=str_name)
            new_item.save()
            return new_item
        return obj.first()


class Stat(models.Model):
    name = models.CharField(max_length=150)
    value = models.IntegerField()

    @classmethod
    def create(cls, item):
        obj = Type.objects.filter(name=item.get('name'))
        if not obj.exists():
            new_item = cls(
                name=item.get('name'),
                value=item.get('value')
            )
            new_item.save()
            return new_item
        return obj.first()


class Type(models.Model):
    name = models.CharField(max_length=150, unique=True)

    @classmethod
    def create(cls, str_name):
        obj = Type.objects.filter(name=str_name)
        if not obj.exists():
            new_item = cls(name=str_name)
            new_item.save()
            return new_item
        return obj.first()


class Location(models.Model):
    name = models.CharField(max_length=150, unique=True)

    @classmethod
    def create(cls, str_name):
        obj = Location.objects.filter(name=str_name)
        if not obj.exists():
            new_item = cls(name=str_name)
            new_item.save()
            return new_item
        return obj.first()


class Region(models.Model):
    name = models.CharField(max_length=150, unique=True)
    locations = models.ManyToManyField(Location)


class Pokemon(models.Model):
    color = models.CharField(max_length=150)
    capture_rate = models.IntegerField()
    height = models.FloatField()
    name = models.CharField(max_length=150)
    weight = models.FloatField()
    flavor_text = models.TextField()
    sprites = models.JSONField()
    abilities = models.ManyToManyField(Ability, related_name='pokemon_abilities')
    moves = models.ManyToManyField(Move, related_name='pokemon_move')
    stats = models.ManyToManyField(Stat, related_name='pokemon_stat')
    types = models.ManyToManyField(Type, related_name='pokemon_type')


class Area(models.Model):
    name = models.CharField(max_length=150, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    pokemon = models.ManyToManyField(Pokemon, related_name='area_pokemon')

    @classmethod
    def create(cls, str_name):
        obj = Location.objects.filter(name=str_name)
        if not obj.exists():
            new_item = cls(name=str_name)
            new_item.save()
            return new_item
        return obj.first()
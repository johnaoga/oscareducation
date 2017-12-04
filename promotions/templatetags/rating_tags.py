from django import template
from resources.models import Resource
from rating.models import Rating
import json


register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def get_average_student(id):
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        print("Error: Resource with id %d doesn't exist" % id)
        return 0
    student,prof = resource.average()
    return student

@register.simple_tag
def get_average_prof(id):
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        print("Error: Resource with id %d doesn't exist"%id)
        return 0
    student,prof = resource.average()
    return prof

@register.simple_tag
def has_rated(user,id):
    try:
        resource = Resource.objects.get(pk=id)
    except Resource.DoesNotExist:
        print("Error: Resource with id %d doesn't exist"%id)
        return False
    if Rating.objects.filter(resource=resource,user=user).exists():
        return True
    else:
        return False

@register.filter
def get_json(dictionary):
    return json.dumps(dictionary)
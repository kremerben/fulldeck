from django import template
from random import shuffle
import datetime
register = template.Library()


@register.filter
def first(list):
    if list is not None and len(list):
        return list[0]


@register.filter
def suit(list, suit_type):
    return [item for item in list if item.get_suit_display() == suit_type]


@register.filter
def rank(list, rank):
    return [item for item in list if item.rank == rank]


@register.filter
def random(cards):
    newlist = list(cards)
    shuffle(newlist)
    return newlist

@register.filter
def random2(list):
    newlist = list[:]
    shuffle(newlist)
    return newlist


@register.filter
def dealsrandom(list, amount):
    newlist = list[:]
    shuffle(newlist)
    return newlist[:amount]

@register.filter
def deals(list, amount):
    return list[:amount]


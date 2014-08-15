from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from fulldeck import settings
from forms import EmailUserCreationForm, AddBalance, Bet
from models import Card, WarGame, Player
import time
from datetime import datetime
from django.db.models import Count, Sum

@cache_page(60)
def home(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'cards.html', data)

def clubs(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'clubs_only.html', data)

def diamonds_hearts(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'diamonds_hearts_only.html', data)

def this_spade(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'this_is_a_spade.html', data)

def faces(request):
    data = {
        'cards': Card.objects.all(), 'faces': ['jack', 'queen', 'king', 'ace'],
    }
    return render(request, 'faces.html', data)

def faces2(request):
    faces = ['jack', 'queen', 'king', 'ace']
    data = {
        'cards': Card.objects.filter(suit)
    }
    return render(request, 'faces.html', data)

def card_filter(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'card_filters.html', data)


def card_custom_filter(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'card_custom_filter.html', data)

@login_required
def profile(request):
    war_wins = request.user.wargame_set.filter(result=WarGame.WIN).count()
    # request.user.WarGame_set.filter(  = same as =  WarGame.objects.filter(player=request.user,
    war_ties = request.user.wargame_set.filter(result=WarGame.TIE).count()
    war_losses = request.user.wargame_set.filter(result=WarGame.LOSS).count()
    total_games = request.user.wargame_set.count()
    percent_win = 0
    if total_games != 0:
        percent_win = war_wins*100.0/total_games
    score = war_wins - war_losses
    total_war_wins = WarGame.objects.filter(result=WarGame.WIN).count()
    total_war_ties = WarGame.objects.filter(result=WarGame.TIE).count()
    total_war_losses = WarGame.objects.filter(result=WarGame.LOSS).count()
    total_total_games = WarGame.objects.count()
    total_percent_win = 0
    if total_total_games != 0:
        total_percent_win = total_war_wins*100.0/total_total_games
    total_score = total_war_wins - total_war_losses
    winners_list = WarGame.objects.values('player__first_name').annotate(Sum('result')).order_by('-result__sum')
    data = {
        'cards': Card.objects.all(),
        'war_games': WarGame.objects.filter(player=request.user),
        'war_wins': war_wins,
        'war_ties': war_ties,
        'war_losses': war_losses,
        'percent_win': percent_win,
        'score': score,
        'total_war_wins': total_war_wins,
        'total_war_ties': total_war_ties,
        'total_war_losses': total_war_losses,
        'total_percent_win': total_percent_win,
        'total_score': total_score,
        'winners_list': winners_list,
    }
    return render(request, 'profile.html', data)

def faq(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'faq.html', data)

def deal5(request):
    data = {
        'cards': Card.objects.all()
    }
    return render(request, 'deal5.html', data)

@login_required
def blackjack(request):
    cards = Card.objects.order_by('?')
    user_cards = cards[:2]
    for card in user_cards:
        if card.rank == 'ace':
            text_content = 'Congrats {} Ace of {}s at {}.'.format(request.user.first_name, card.rank, datetime.now() )
            html_content = '<h2>Congrats {} Ace of {}s at {}.</h2>'.format(request.user.first_name, card.get_suit_display(), datetime.now())
            msg = EmailMultiAlternatives("Ace!", text_content, settings.DEFAULT_FROM_EMAIL, [request.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    dealer_cards = cards[2:4]
    data = {
        'user_cards': user_cards,
        'dealer_cards': dealer_cards,
    }
    return render(request, 'blackjack.html', data)

def poker(request):
    data = {
        'cards': Card.objects.order_by('?')[:5]
    }
    return render(request, 'poker.html', data)

def hearts(request):
    data = {
        'cards': Card.objects.filter(suit=Card.HEART)
    }
    return render(request, 'hearts.html', data)

def not_faces(request):
    faces = ['jack', 'queen', 'king', 'ace']
    data = {
        'cards': Card.objects.exclude(rank__in=faces)
    }
    return render(request, 'not_faces.html', data)

def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # # user.email_user("Welcome!", "Thank you, {} {} for signing up for our website.".format(user.first_name, user.last_name))
            # text_content = 'Thank you {} {} for signing up for our website on {}.'.format(user.first_name, user.last_name, user.date_joined)
            # html_content = '<h2>Thanks {} {} for signing up on {}!</h2> <div>I hope you enjoy using our site</div>'.format(user.first_name, user.last_name, user.date_joined.strftime("%B %d, %Y"))
            # msg = EmailMultiAlternatives("Welcome! {} {}".format(user.first_name, user.last_name), text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            return redirect("profile")
    else:
        form = EmailUserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


def add_balance(request):
    if request.method == 'POST':
        form = AddBalance(request.POST)
        if form.is_valid():
            add_balance = form.cleaned_data['add_to']
            request.user.balance += add_balance
            request.user.save()
            return redirect("add_balance")
    else:
        form = AddBalance()
    return render(request, "add_balance.html", {
        'form': form,
    })

# def bet(request):
#     if request.method == 'POST':
#         form = Bet(request.POST)
#         if form.is_valid():
#             bet_amount = form.cleaned_data['bet_amount']
#
#             request.user.balance += bet_amount
#             request.user.save()
#             return redirect("war")
#     else:
#         form = Bet()
#     return render(request, "war.html", {
#         'form': form,
#     })

@login_required()
def war(request):
    cards = list(Card.objects.order_by('?'))
    user_card = cards[0]
    dealer_card = cards[1]
    result = user_card.get_war_result(dealer_card)
    WarGame.objects.create(result=result, player=request.user)

    if request.method == 'POST':
        form = Bet(request.POST)
        if form.is_valid():
            bet_amount = form.cleaned_data['bet_amount']
            request.user.balance += result * bet_amount
            request.user.save()
            return redirect("war")
    else:
        form = Bet()

    return render(request, 'war.html', {
        'user_cards': [user_card],
        'dealer_cards': [dealer_card],
        'result': result,
        'form': form,
    })

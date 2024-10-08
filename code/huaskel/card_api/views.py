from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from accounts.models import User
from .serializer import CardSerializer, CardRegistriesSerializer
from rest_framework import status
from django.http import JsonResponse
from django.db.models import Q
import logging

logger = logging.getLogger('card_api')


@api_view(['GET'])
def getCards(request, filter=False, filterString=""):
    cards = Card.objects.all()
    if filter:
        cards = Card.objects.filter(Q(owner_full_name__icontains=filterString) | Q(id__icontains=filterString))

    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)


def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['POST'])
def checkInCard(request):
    station_address = get_ip_address(request)

    logger.info('Getting check-in request from: %s', station_address)

    station = get_object_or_404(Station, station_address=station_address)


    card_physical_id = request.data.get("id")
    # I know there must be a better way to do this but its 3 am and I am tired
    if card_physical_id == None:
        print(str(request.get_full_path))
        my_string = str(request.get_full_path)
        #check if it contains ID
        if "id=" in my_string:
            my_string = my_string.split("id=", 1)[1]
            id = my_string[:len(my_string) - 3]
            print(id)
        else:
            logger.warning("No id found in request")
            return Response(status.HTTP_400_BAD_REQUEST)

        card_physical_id = id




    if station.is_waiting_for_pair:

        card = station.card_to_pair_with
        logger.info('Pairing card with id: %s with physical id: %s', str(card.id), card_physical_id)

        card.physical_card_id = card_physical_id
        card.save()
        station.is_waiting_for_pair = False
        station.card_to_pair_with = None
        station.save()
    else:
        logger.info('Attempting to check-in card with physical id: %s', card_physical_id)
        card = get_object_or_404(Card, physical_card_id=card_physical_id)
        card.times_checked_in += 1
        card.save()
        is_checkout = False
        if CardRegistries.objects.filter(owner_id=card.owner).exists():
            last_registry = CardRegistries.objects.filter(owner_id=card.owner).order_by('-id')[0]
            is_checkout = not (last_registry.is_checkout)

        registry_obj = CardRegistries(owner=card.owner, station_id=station.id, card_id=card.id, is_checkout=is_checkout)
        registry_obj.save()
        logger.info('Card %s checked-in', str(card.id))

    return Response(status.HTTP_200_OK)


@api_view(['GET'])
def getCardRegistriesForUser(request):
    user = get_object_or_404(User, id=request.user.id)

    registries = get_list_or_404(CardRegistries, owner_id=user.id)
    serializer = CardRegistriesSerializer(registries, many=True)

    return Response(serializer.data)
    # return JsonResponse(data=serializer.data, status=201 , safe=False)
    # if serializer.is_valid():
    # return JsonResponse(serializer.data, status=201)
    # return JsonResponse(serializer.errors, status=400)


def manualCheckIn(request):

    card = get_object_or_404(Card, owner_id=request.user.id)
    logger.info('Attempting to MANUALLY check-in card :%s', card)
    card.times_checked_in += 1
    card.save()
    is_checkout = False
    if CardRegistries.objects.filter(owner_id=card.owner).exists():
        last_registry = CardRegistries.objects.filter(owner_id=card.owner).order_by('-id')[0]
        is_checkout = not (last_registry.is_checkout)

    registry_obj = CardRegistries(owner=card.owner, station_id=Station.objects.all()[0].id, card_id=card.id, is_checkout=is_checkout)
    registry_obj.save()
    logger.info('Card %s checked-in', str(card.id))
    return redirect('/')
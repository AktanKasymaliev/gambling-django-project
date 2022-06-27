from random import choices, shuffle

# import requests
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpRequest
from rest_framework import views, response, status, permissions
from django.contrib.auth import get_user_model

from gamble.models import Session, Slot, CurrentRound, SlotMachine
from gamble.serializers import SessionSerializer
# from config.settings import HOST


User = get_user_model()

class GetTheRandomBoxView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __add_user_to_session(self, slot_machine: SlotMachine, request: HttpRequest):
        """
        "If the user is not already in the session, add them."
        
        The first thing we do is check if the user is already in the session. If they are, we don't need to
        do anything. If they aren't, we need to add them
        
        :param slot_machine: The slot machine that the user is trying to join
        :type slot_machine: SlotMachine
        :param request: The request object
        :type request: HttpRequest
        """
        try:
            with transaction.atomic():
                Session.objects.create(
                    slot_machine=slot_machine,
                    user=request.user
                    )
        except IntegrityError:
            pass

    def __get_current_round_and_slot_machine(self, request, slot_machine_id: int) -> tuple:
        """
        It creates a new CurrentRound object and returns it
        
        :param slot_machine_id: The id of the slot machine that the user is playing on
        :return: The current round of the slot machine.
        """
        slot_machine = self.__get_slot_machine(slot_machine_id)
        try:
            current_round = CurrentRound.objects.get(slot_machine=slot_machine_id)
        except CurrentRound.DoesNotExist:
            current_round = CurrentRound.objects.create(slot_machine=slot_machine)
            # requests.get(f'http://{HOST}/api/auto-complete/{slot_machine_id}/')

        self.__add_user_to_session(slot_machine, request)
        return current_round, slot_machine

    def __get_slot_machine(self, slot_machine_id: int) -> SlotMachine:
        """
        > This function returns a slot machine object from the database
        
        :param slot_machine_id: The id of the slot machine that the user is playing
        :return: The slot machine object with the id that is passed in.
        """
        try:
            return SlotMachine.objects.get(id=slot_machine_id)
        except SlotMachine.DoesNotExist:
            return response.Response(
                "Please, add new slot machine for continue.", 
                status=status.HTTP_404_NOT_FOUND)


    def __return_response(self, current_round: int, box: Slot) -> response.Response:
        """
        > The function returns a response object with the current round, the box id, the weight of the box,
        and whether or not the box is a jackpot
        
        :param current_round: int
        :type current_round: int
        :param box: Slot
        :type box: Slot
        :return: The response is being returned.
        """
        return response.Response(
                {"round": current_round.round,
                 "id_of_box": box.box,
                 "your_box": box.weight,
                 "is_jackpot": box.is_jackpot
                 }, status=status.HTTP_200_OK
                )
    
    def __increase_round_counter(self, state_of_round: CurrentRound) -> None:
        """
        > This function increases the round counter by one
        
        :param state_of_round: CurrentRound
        :type state_of_round: CurrentRound
        """
        state_of_round.round += 1 
        state_of_round.save()
    
    def __increase_round_played_field(
        self, request: HttpRequest, slot_machine: SlotMachine) -> None:
        """
        It increases the number of rounds played by one
        
        :param request: HttpRequest
        :type request: HttpRequest
        :param slot_machine: The slot machine object that the user is playing
        :type slot_machine: SlotMachine
        """
        session = Session.objects.get(slot_machine=slot_machine, user=request.user)
        session.round_played += 1
        session.save()
    
    def __delete_slot_instance(self, slot_machine_id: int, box: Slot) -> None:
        """
        "Delete all slot instances that are associated with the given slot machine and box."
        
        The first thing we do is get the slot machine id and the box. We then use the Django ORM to delete
        all slot instances that are associated with the given slot machine and box
        
        :param slot_machine_id: The id of the slot machine
        :type slot_machine_id: int
        :param box: The box that the slot machine is in
        :type box: Slot
        """
        Slot.objects.filter(box=box, slot_machine=slot_machine_id).delete()

    def __reload_round(self, current_round: CurrentRound, slot_machine_id: int) -> None:
        """
        It deletes the current round and all sessions
        
        :param current_round: The current round object that is being reloaded
        :type current_round: CurrentRound
        :param slot_machine_id: The id of the slot machine that the round is being reloaded for
        :type slot_machine_id: int
        """
        current_round.delete()
        Session.objects.all().delete()


    def post(self, request, slot_machine_id: int):
        """
        The function gets the current round of the slot machine, if the current round is less than 11, it
        gets all the boxes that are not jackpot boxes, then it chooses a random box from the list of
        boxes, then it increments the current round by 1 and returns the round, the id of the box and the
        weight of the box
        
        :param request: The request object
        :param slot_machine_id: The id of the slot machine
        :return: The current round, the id of the box, and the weight of the box.
        """
        current_round, slot_machine = self.__get_current_round_and_slot_machine(request, slot_machine_id)
        if current_round.round < 10:
            try:
                boxes = list(Slot.objects.filter(slot_machine=slot_machine_id, is_jackpot=False))
                shuffle(boxes)
                randome_box = choices(boxes)[-1]

                self.__delete_slot_instance(slot_machine_id, randome_box.box)
                self.__increase_round_played_field(request, slot_machine)
                self.__increase_round_counter(current_round)

                return self.__return_response(current_round, randome_box)

            except (IndexError, Slot.DoesNotExist):
                return response.Response(
                    "Please, add new slots for continue.",
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            jackpot_box = Slot.objects.get(slot_machine=slot_machine_id, is_jackpot=True)
            self.__delete_slot_instance(slot_machine_id, jackpot_box.box)
            self.__increase_round_counter(current_round)

            self.__reload_round(current_round, slot_machine_id)
            return self.__return_response(current_round, jackpot_box)

    def get(self, request, slot_machine_id: int):
        """
        It gives info about the game.
        
        :param request: The request object that was sent to the view
        :param slot_machine_id: int - the id of the slot machine
        :type slot_machine_id: int
        :return: A list of all the users that are currently playing on the slot machine.
        """
        slot_machine = SlotMachine.objects.get(id=slot_machine_id)
        session = Session.objects.filter(slot_machine=slot_machine)

        return response.Response({
            "users": SessionSerializer(session, many=True).data
        })

class AutoCreatePatternSlotsView(views.APIView):
    """
    This view only for me)
    View for do more comfotable code process
    """
    def get(self, request, slot_machine_id: int):
        machine = SlotMachine.objects.get(id=slot_machine_id)
        Slot.objects.create(slot_machine=machine, box=1, weight="20")
        Slot.objects.create(slot_machine=machine, box=2, weight="100")
        Slot.objects.create(slot_machine=machine, box=3, weight="45")
        Slot.objects.create(slot_machine=machine, box=4, weight="70")
        Slot.objects.create(slot_machine=machine, box=5, weight="15")
        Slot.objects.create(slot_machine=machine, box=6, weight="140")
        Slot.objects.create(slot_machine=machine, box=7, weight="20")
        Slot.objects.create(slot_machine=machine, box=8, weight="20")
        Slot.objects.create(slot_machine=machine, box=9, weight="140")
        Slot.objects.create(slot_machine=machine, box=10, weight="45")
        Slot.objects.create(slot_machine=machine, box=11, weight="Jackpot", is_jackpot=True)
        return response.Response("Auto complete done")
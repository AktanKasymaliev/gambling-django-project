from random import choices, shuffle

from gamble.models import Slot, CurrentRound, SlotMachine
# from gamble.serializers import RoundSerializer
from config.settings import HOST

import requests
from rest_framework import views, response, status, permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class GetTheRandomBoxView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __get_current_round(self, request, slot_machine_id: int) -> CurrentRound:
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

        # current_round.users.add(request.user)

        return current_round

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
        return response.Response(
                {"round": current_round.round,
                 "id_of_box": box.box,
                 "your_box": box.weight}, status=status.HTTP_200_OK
                )
    
    def __increase_round_counter(self, state_of_round: CurrentRound) -> None:
        state_of_round.round += 1 
        state_of_round.save()
    
    def __delete_slot_instance(self, slot_machine_id: int, box: Slot) -> None:
        Slot.objects.filter(box=box, slot_machine=slot_machine_id).delete()

    def __reload_round(self, current_round: CurrentRound, slot_machine_id: int) -> None:
        current_round.delete()


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
        current_round = self.__get_current_round(request, slot_machine_id)
        if current_round.round < 10:
            try:
                boxes = list(Slot.objects.filter(slot_machine=slot_machine_id, is_jackpot=False))
                shuffle(boxes)
                randome_box = choices(boxes)[-1]

                self.__delete_slot_instance(slot_machine_id, randome_box.box)
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
        pass

class AutoCreatePatternSlotsView(views.APIView):
    """
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
from random import choices
import requests

from gamble.models import Slot, CurrentRound, SlotMachine
from config.settings import HOST

from rest_framework import views, response, status

class GetTheRandomBoxView(views.APIView):

    def __get_current_round(self, slot_machine_id: int) -> CurrentRound:
        """
        It creates a new CurrentRound object and returns it
        
        :param slot_machine_id: The id of the slot machine that the user is playing on
        :return: The current round of the slot machine.
        """
        slot_machine = self.__get_slot_machine(slot_machine_id)
        try:
            current_round = CurrentRound.objects.get(slot_machine=slot_machine)
        except CurrentRound.DoesNotExist:
            current_round = CurrentRound.objects.create(slot_machine=slot_machine)

        return current_round

    def __get_slot_machine(self, slot_machine_id: int) -> SlotMachine:
        """
        > This function returns a slot machine object from the database
        
        :param slot_machine_id: The id of the slot machine that the user is playing
        :return: The slot machine object with the id that is passed in.
        """
        return SlotMachine.objects.get(id=slot_machine_id)

    def __return_response(self, current_round: int, box: Slot) -> response.Response:
        return response.Response(
                {"Round": current_round.round,
                 "Id of box": box.box,
                 "Your box": box.weight}, status=status.HTTP_200_OK
                )
    
    def __increase_round_counter(self, state_of_round: CurrentRound) -> None:
        state_of_round.round += 1 
        state_of_round.save()
    
    def __delete_slot_instances(self, box: Slot) -> None:
        Slot.objects.filter(box=box).delete()

    def __reload_round(self, current_round: CurrentRound) -> None: 
        current_round.delete()
        requests.get(f'http://{HOST}/api/auto-complete/')


    def get(self, request, slot_machine_id: int):
        """
        The function gets the current round of the slot machine, if the current round is less than 11, it
        gets all the boxes that are not jackpot boxes, then it chooses a random box from the list of
        boxes, then it increments the current round by 1 and returns the round, the id of the box and the
        weight of the box
        
        :param request: The request object
        :param slot_machine_id: The id of the slot machine
        :return: The current round, the id of the box, and the weight of the box.
        """
        current_round = self.__get_current_round(slot_machine_id)
        if current_round.round <= 11:
            try:
                boxes = Slot.objects.filter(is_jackpot=False)
                randome_box = choices(boxes)[-1]
                self.__delete_slot_instances(randome_box.box)
                self.__increase_round_counter(current_round)

                return self.__return_response(current_round, randome_box)

            except IndexError:
                jackpot_box = Slot.objects.get(is_jackpot=True)
                self.__delete_slot_instances(jackpot_box.box)
                self.__increase_round_counter(current_round)

                self.__reload_round()
                return self.__return_response(current_round, jackpot_box)

class AutoCreatePatternSlotsView(views.APIView):
    """
    View for do more comfotable code process
    """
    def get(self, request):
        Slot.objects.create(box=1, weight="20")
        Slot.objects.create(box=2, weight="100")
        Slot.objects.create(box=3, weight="45")
        Slot.objects.create(box=4, weight="70")
        Slot.objects.create(box=5, weight="15")
        Slot.objects.create(box=6, weight="140")
        Slot.objects.create(box=7, weight="20")
        Slot.objects.create(box=8, weight="20")
        Slot.objects.create(box=9, weight="140")
        Slot.objects.create(box=10, weight="45")
        Slot.objects.create(box=11, weight="Jackpot", is_jackpot=True)
        return response.Response("Auto complete done")
        
        #TODO make post request and finish get request by test task
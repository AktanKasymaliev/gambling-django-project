from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from gamble.models import SlotMachine, Slot

User = get_user_model()

class BaseTestCaseSlot(TestCase):

    def setUp(self) -> None:
        self.user = {
            "email": "test@gmail.com", 
            "username": "test",
            "password": "password", 
            }
        self.slot_machine = SlotMachine.objects.create()

        self.login_url = reverse('login')
        self.register_url = reverse('signup')
        self.spin_url = reverse('spin', kwargs={'slot_machine_id': self.slot_machine.id})
        self.auto_complete_url = reverse('auto-complete', kwargs={'slot_machine_id': self.slot_machine.id})

        self.client.post(self.register_url, data=self.user)


class SlotChooseTest(BaseTestCaseSlot):

    def __auto_complete_slots(self, slot_machine_id: int) -> None:
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
    
    def __login(self) -> str:
        login_response = self.client.post(self.login_url, self.user)
        return login_response.json()['access']
    
    def __spint_slot_with_token(self, jwt_token: str) -> HttpResponse:
        return self.client.post(self.spin_url, HTTP_AUTHORIZATION=f'JWT {jwt_token}')

    def test_on_spining_slot(self):
        jwt_token = self.__login()
        self.__auto_complete_slots(self.slot_machine.id)
        spin_response = self.__spint_slot_with_token(jwt_token)
        self.assertEqual(spin_response.status_code, 200)

    def test_on_spining_slot_without_login(self):
        spin_response = self.client.post(self.spin_url)
        self.assertEqual(spin_response.status_code, 403)
    
    def test_on_spining_slot_without_slots(self):
        jwt_token = self.__login()
        spin_response = self.__spint_slot_with_token(jwt_token)
        self.assertEqual(spin_response.status_code, 404)
    
    def test_get_jackpot(self):
        jwt_token = self.__login()
        self.__auto_complete_slots(self.slot_machine.id)

        jackpot_string: str
        for _ in range(11):
            spin_response = self.__spint_slot_with_token(jwt_token)
            spin_data = spin_response.json()
            if spin_data["your_box"] == "Jackpot":
                jackpot_string = spin_data["your_box"]

        self.assertEqual(spin_response.status_code, 200)
        self.assertEqual(jackpot_string, "Jackpot")
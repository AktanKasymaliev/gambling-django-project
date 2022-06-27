from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SlotMachine(models.Model):
    
    def __str__(self) -> str:
        return f"Machine - {self.id}"

    class Meta:
        db_table = 'slot_machine_db'
        verbose_name = 'Slot Machine'
        verbose_name_plural = 'Slot Machines'

class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slot_machine = models.ForeignKey(SlotMachine, on_delete=models.CASCADE)
    round_played = models.PositiveSmallIntegerField(verbose_name='All played round', default=0)

    def __str__(self) -> str:
        return f"Session on - {self.slot_machine.id} machine ({self.user.username})"

    class Meta:
        db_table = 'session_db'
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'

class Slot(models.Model):
    slot_machine = models.ForeignKey(SlotMachine, on_delete=models.CASCADE, related_name='slot')
    box = models.PositiveSmallIntegerField(verbose_name='Box of cell')
    weight = models.CharField(verbose_name='Weight of box', max_length=10)
    is_jackpot = models.BooleanField(verbose_name="Is this box jackpot", default=False)

    def __str__(self) -> str:
        return f"Box - {self.box}"

    class Meta:
        db_table = 'slot_db'
        verbose_name = 'Slot'
        verbose_name_plural = 'Slots'

class CurrentRound(models.Model):
    slot_machine = models.OneToOneField(SlotMachine, on_delete=models.CASCADE)
    round = models.PositiveSmallIntegerField(verbose_name='Round', default=0)

    def __str__(self) -> str:
        return f"Round - {self.round}"
    
    class Meta:
        db_table = 'round_db'
        verbose_name = 'Round'
        verbose_name_plural = 'Rounds'
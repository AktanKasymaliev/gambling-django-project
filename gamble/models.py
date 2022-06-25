from django.db import models

class SlotMachine(models.Model):
    
    def __str__(self) -> str:
        return f"Machine - {self.id}"

    class Meta:
        db_table = 'slot_machine_db'
        verbose_name = 'Slot Machine'
        verbose_name_plural = 'Slot Machines'

class Slot(models.Model):
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
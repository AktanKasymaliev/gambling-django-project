from django.db import models

class SlotMachine(models.Model):
    box = models.PositiveSmallIntegerField(verbose_name='Box of cell')
    weight = models.CharField(verbose_name='Weight of box', max_length=10)

    def __str__(self) -> str:
        return f"Box - {self.box}"

    class Meta:
        db_table = 'slot_db'
        verbose_name = 'Slot Machine'
        verbose_name_plural = 'Slot Machines'
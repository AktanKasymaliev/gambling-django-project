from django.contrib import admin

from gamble.models import SlotMachine

@admin.register(SlotMachine)
class SlotMachineAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin

from gamble.models import CurrentRound, Session, Slot, SlotMachine

@admin.register(SlotMachine)
class SlotMachineAdmin(admin.ModelAdmin):
    pass

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    pass

@admin.register(CurrentRound)
class CurrentRoundAdmin(admin.ModelAdmin):
    pass

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass
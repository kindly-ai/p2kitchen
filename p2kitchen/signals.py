from django.db.models.signals import post_save
from django.dispatch import receiver

from p2kitchen.messaging import send_full_machine_update
from p2kitchen.models import Brew, BrewReaction


@receiver(post_save, sender=BrewReaction)
def create_brew_reaction_event(*args, **kwargs):
    send_full_machine_update()


@receiver(post_save, sender=Brew)
def brew_saved_event(*args, **kwargs):
    send_full_machine_update()

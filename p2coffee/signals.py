from django.db.models.signals import post_save
from django.dispatch import receiver

from p2coffee.messaging import send_group_message
from p2coffee.models import BrewReaction


@receiver(post_save, sender=BrewReaction)
def create_brew_reaction_event(sender, instance: BrewReaction, created: bool, **kwargs):
    brew_reaction = instance
    if created:
        message = f"{brew_reaction.user} reacted with {brew_reaction.reaction} to {brew_reaction.brew}"
        send_group_message(message=message)

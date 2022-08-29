from django.db.models.signals import post_save
from django.dispatch import receiver

from p2kitchen.messaging import send_group_message
from p2kitchen.models import BrewReaction, Machine


@receiver(post_save, sender=BrewReaction)
def create_brew_reaction_event(sender, instance: BrewReaction, created: bool, **kwargs):
    brew_reaction = instance
    if created:
        # FIXME: Hook up these events at a later time
        message = f"{brew_reaction.user} reacted with {brew_reaction.reaction} to {brew_reaction.brew}"
        send_group_message(message=message)
        send_group_message(
            message_type="machine.update", machine_ids=list(Machine.objects.values_list("id", flat=True))
        )

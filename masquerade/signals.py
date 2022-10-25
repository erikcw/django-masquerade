from django.dispatch import Signal

# providing_args=['mask_username',]
mask_on = Signal()

# providing_args=['mask_username',]
mask_off = Signal()

import django.db.models.options as options

custom_names = (
    'RLSable',
)


def set_custom_option_names(*args, **kwargs):
    options.DEFAULT_NAMES = options.DEFAULT_NAMES + custom_names

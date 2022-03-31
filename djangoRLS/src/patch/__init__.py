from .custom_options import set_custom_option_names

patches = (
    (set_custom_option_names, None, None),
)


def apply():
    for func, args, kwargs in patches:
        args = args or []
        kwargs = kwargs or {}
        func(*args, **kwargs)

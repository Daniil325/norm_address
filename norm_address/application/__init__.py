from dishka import Provider, provide, Scope

from norm_address.application.usecases import NormalizeAddressCommand


class CommandsProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self):
        super().__init__()

    normalize_address_command = provide(NormalizeAddressCommand)

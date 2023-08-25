class SteamError(Exception):
    pass


class SteamAPI429Error(SteamError):
    pass


class SteamItemNameIdNotFoundError(SteamError):
    pass


class BuffError(Exception):
    pass

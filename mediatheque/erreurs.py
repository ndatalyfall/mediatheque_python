class MediathequeError(Exception):
    """Exception de base pour la médiathèque."""
    pass


class DocumentIndisponible(MediathequeError):
    """Le document demandé est déjà prêté."""
    pass


class TropDEmprunts(MediathequeError):
    """L'adhérent a atteint la limite d'emprunts."""
    pass


class DocumentInconnu(MediathequeError):
    """Le document n'existe pas dans la médiathèque."""
    pass

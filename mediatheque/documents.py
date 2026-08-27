from abc import ABC, abstractmethod


class Document(ABC):

    def __init__(self, titre: str, annee: int, code: str):
        self._titre = titre
        self._annee = annee
        self._code = code
        self._disponible = True

    @property
    def titre(self) -> str:
        return self._titre

    @property
    def annee(self) -> int:
        return self._annee

    @property
    def code(self) -> str:
        return self._code

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, value: bool):
        self._disponible = value

    @abstractmethod
    def duree_pret(self) -> int:
        ...

    def __eq__(self, other) -> bool:
        if not isinstance(other, Document):
            return False
        return self._code == other._code

    def __hash__(self) -> int:
        # Deux documents de meme code doivent avoir le meme hash,
        # coherent avec __eq__. Permet d'utiliser un Document dans
        # un set ou comme cle de dict si besoin.
        return hash(self._code)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} \"{self._titre}\" ({self._annee}) - a rendre sous {self.duree_pret()} jours"

    def __repr__(self) -> str:
        # Representation technique, utile pour le debogage
        return f"{self.__class__.__name__}(titre={self._titre!r}, annee={self._annee}, code={self._code!r})"


class Livre(Document):

    def __init__(self, titre: str, annee: int, code: str, auteur: str = "", nb_pages: int = 0):
        super().__init__(titre, annee, code)
        self._auteur = auteur
        self._nb_pages = nb_pages

    @property
    def auteur(self) -> str:
        return self._auteur

    @property
    def nb_pages(self) -> int:
        return self._nb_pages

    def duree_pret(self) -> int:
        return 21

    def __str__(self) -> str:
        return super().__str__()


class DVD(Document):

    def __init__(self, titre: str, annee: int, code: str, realisateur: str = "", duree_min: int = 0):
        super().__init__(titre, annee, code)
        self._realisateur = realisateur
        self._duree_min = duree_min

    @property
    def realisateur(self) -> str:
        return self._realisateur

    @property
    def duree_min(self) -> int:
        return self._duree_min

    def duree_pret(self) -> int:
        return 7

    def __str__(self) -> str:
        return super().__str__()
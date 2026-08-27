class Adherent:

    _compteur = 0

    def __init__(self, nom: str):
        Adherent._compteur += 1
        self._nom = nom
        self._numero = f"A{Adherent._compteur:03d}"
        self._emprunts = []

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def emprunts(self):
        return list(self._emprunts)

    def emprunter(self, document):
        # C'est desormais l'adherent lui-meme qui gere sa liste d'emprunts,
        # au lieu de laisser Mediatheque toucher directement a _emprunts.
        self._emprunts.append(document)

    def rendre(self, document):
        self._emprunts.remove(document)

    def __len__(self) -> int:
        return len(self._emprunts)

    def __repr__(self) -> str:
        return f"Adherent(nom={self._nom!r}, numero={self._numero!r})"

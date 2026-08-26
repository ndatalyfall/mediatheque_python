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

    def __len__(self) -> int:
        return len(self._emprunts)

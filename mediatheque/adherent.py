from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pret import Pret
    from documents import Document


class Adherent:

    _compteur = 0

    def __init__(self, nom: str):
        Adherent._compteur += 1
        self._nom = nom
        self._numero = f"A{Adherent._compteur:03d}"
        self._emprunts: list["Pret"] = []

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def numero(self) -> str:
        return self._numero

    @property
    def emprunts(self):
        return list(self._emprunts)

    def emprunter(self, pret: "Pret"):
        # C'est desormais Adherent qui gere sa propre liste d'emprunts
        # (encapsulation) : Mediatheque ne touche plus _emprunts directement.
        self._emprunts.append(pret)

    def rendre(self, document: "Document") -> bool:
        # Retire le pret correspondant au document rendu.
        # Renvoie True si un pret a ete retire, False si l'adherent
        # n'avait pas ce document en cours.
        for pret in self._emprunts:
            if pret.document == document:
                self._emprunts.remove(pret)
                return True
        return False

    def __len__(self) -> int:
        return len(self._emprunts)

    def __repr__(self) -> str:
        return f"Adherent(nom={self._nom!r}, numero={self._numero!r}, emprunts_en_cours={len(self._emprunts)})"
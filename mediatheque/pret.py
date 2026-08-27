from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import TYPE_CHECKING

from documents import Document

# Import uniquement pour l'annotation de type, pas au runtime :
# evite un import circulaire avec adherent.py
if TYPE_CHECKING:
    from adherent import Adherent


@dataclass
class Pret:
    """Represente un emprunt : quel document, par quel adherent, depuis quand."""

    document: Document
    adherent: "Adherent"
    date_emprunt: date = field(default_factory=date.today)

    @property
    def date_retour_prevue(self) -> date:
        return self.date_emprunt + timedelta(days=self.document.duree_pret())

    @property
    def en_retard(self) -> bool:
        return date.today() > self.date_retour_prevue

    def __str__(self) -> str:
        retard = " (EN RETARD)" if self.en_retard else ""
        return (f"{self.document} — emprunte le {self.date_emprunt.strftime('%d/%m/%Y')}, "
                f"a rendre avant le {self.date_retour_prevue.strftime('%d/%m/%Y')}{retard}")
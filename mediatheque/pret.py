from dataclasses import dataclass, field
from datetime import date, timedelta

from .documents import Document
from .adherent import Adherent


@dataclass
class Pret:
    """Represente un emprunt en cours : quel document, par qui, depuis quand."""

    document: Document
    adherent: Adherent
    date_emprunt: date = field(default_factory=date.today)

    @property
    def date_retour_prevue(self) -> date:
        return self.date_emprunt + timedelta(days=self.document.duree_pret())

    @property
    def en_retard(self) -> bool:
        return date.today() > self.date_retour_prevue

    def __str__(self) -> str:
        return (f"{self.document.titre} emprunte par {self.adherent.nom} "
                f"le {self.date_emprunt:%d/%m/%Y} - a rendre avant le {self.date_retour_prevue:%d/%m/%Y}")

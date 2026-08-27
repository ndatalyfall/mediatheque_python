from .documents import Document, Livre, DVD
from .adherent import Adherent
from .pret import Pret
from .erreurs import DocumentIndisponible, TropDEmprunts, DocumentInconnu


class Mediatheque:

    LIMITE_EMPRUNTS = 3

    def __init__(self, nom: str):
        self._nom = nom
        self._documents = {}
        self._adherents = {}
        self._prets = []

    @property
    def nom(self) -> str:
        return self._nom

    def ajouter_document(self, document: Document):
        self._documents[document.code] = document

    def inscrire(self, nom: str) -> Adherent:
        adherent = Adherent(nom)
        self._adherents[adherent.numero] = adherent
        return adherent

    def emprunter(self, numero: str, code: str) -> Document:
        if numero not in self._adherents:
            raise DocumentInconnu(f"Adhérent {numero} inconnu")

        if code not in self._documents:
            raise DocumentInconnu(f"Document {code} inconnu")

        adherent = self._adherents[numero]
        document = self._documents[code]

        if not document.disponible:
            raise DocumentIndisponible(f"Le document \"{document.titre}\" est déjà prêté")

        if len(adherent) >= self.LIMITE_EMPRUNTS:
            raise TropDEmprunts(f"{adherent.nom} a déjà {self.LIMITE_EMPRUNTS} emprunts en cours")

        document.disponible = False
        adherent.emprunter(document)
        self._prets.append(Pret(document=document, adherent=adherent))
        return document

    def rendre(self, numero: str, code: str):
        if numero not in self._adherents:
            raise DocumentInconnu(f"Adhérent {numero} inconnu")

        if code not in self._documents:
            raise DocumentInconnu(f"Document {code} inconnu")

        adherent = self._adherents[numero]
        document = self._documents[code]

        if document in adherent.emprunts:
            adherent.rendre(document)
            document.disponible = True
            self._prets = [
                p for p in self._prets
                if not (p.document == document and p.adherent is adherent)
            ]

    def rechercher(self, mot: str):
        # Generateur : les resultats sont produits a la demande.
        mot_lower = mot.lower()
        for doc in self._documents.values():
            if mot_lower in doc.titre.lower():
                yield doc

    def documents_disponibles(self):
        # Generateur, meme principe que rechercher().
        for doc in self._documents.values():
            if doc.disponible:
                yield doc

    def emprunts_de(self, numero: str) -> list:
        if numero not in self._adherents:
            raise DocumentInconnu(f"Adhérent {numero} inconnu")
        return self._adherents[numero].emprunts

    def prets_en_retard(self):
        # Generateur : ne produit que les prets dont la date de retour prevue est depassee.
        for pret in self._prets:
            if pret.en_retard:
                yield pret

    def __len__(self) -> int:
        # len(mediatheque) renvoie le nombre de documents references
        return len(self._documents)

    def __iter__(self):
        # Rend la mediatheque directement iterable : for doc in mediatheque
        return iter(self._documents.values())

    def __repr__(self) -> str:
        return (f"Mediatheque(nom={self._nom!r}, "
                f"documents={len(self._documents)}, adherents={len(self._adherents)})")

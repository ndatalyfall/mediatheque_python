from .documents import Document
from .adherent import Adherent
from .erreurs import DocumentIndisponible, TropDEmprunts, DocumentInconnu


class Mediatheque:

    def __init__(self, nom: str):
        self._nom = nom
        self._documents = {}
        self._adherents = {}

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

        if len(adherent) >= 3:
            raise TropDEmprunts(f"{adherent.nom} a déjà 3 emprunts en cours")

        document.disponible = False
        adherent._emprunts.append(document)
        return document

    def rendre(self, numero: str, code: str):
        if numero not in self._adherents:
            raise DocumentInconnu(f"Adhérent {numero} inconnu")

        if code not in self._documents:
            raise DocumentInconnu(f"Document {code} inconnu")

        adherent = self._adherents[numero]
        document = self._documents[code]

        if document in adherent._emprunts:
            adherent._emprunts.remove(document)
            document.disponible = True

    def rechercher(self, mot: str) -> list:
        mot_lower = mot.lower()
        return [doc for doc in self._documents.values() if mot_lower in doc.titre.lower()]

    def documents_disponibles(self) -> list:
        return [doc for doc in self._documents.values() if doc.disponible]

    def emprunts_de(self, numero: str) -> list:
        if numero not in self._adherents:
            raise DocumentInconnu(f"Adhérent {numero} inconnu")
        return self._adherents[numero].emprunts

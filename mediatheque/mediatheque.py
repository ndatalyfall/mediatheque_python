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

    def rechercher(self, mot: str):
        # Generateur : les resultats sont produits a la demande,
        # sans construire toute la liste en memoire d'un coup.
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

    def __len__(self) -> int:
        # len(mediatheque) renvoie le nombre de documents references
        return len(self._documents)

    def __iter__(self):
        # Rend la mediatheque directement iterable : for doc in mediatheque
        return iter(self._documents.values())

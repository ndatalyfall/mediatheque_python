import pytest

from ..mediatheque.mediatheque import Mediatheque
from ..mediatheque.documents import Livre, DVD
from ..mediatheque.erreurs import DocumentIndisponible, TropDEmprunts, DocumentInconnu


@pytest.fixture
def mediatheque():
    m = Mediatheque("Test")
    m.ajouter_document(Livre("Livre A", 2000, "L001"))
    m.ajouter_document(Livre("Livre B", 2001, "L002"))
    m.ajouter_document(Livre("Livre C", 2002, "L003"))
    m.ajouter_document(DVD("DVD A", 2010, "D001"))
    return m


def test_inscrire_genere_un_numero(mediatheque):
    adherent = mediatheque.inscrire("Fatou")
    assert adherent.nom == "Fatou"
    assert adherent.numero.startswith("A")


def test_emprunter_rend_document_indisponible(mediatheque):
    adherent = mediatheque.inscrire("Fatou")
    mediatheque.emprunter(adherent.numero, "L001")
    doc = mediatheque._documents["L001"]
    assert doc.disponible is False


def test_emprunter_document_deja_prete_leve_indisponible(mediatheque):
    a1 = mediatheque.inscrire("Fatou")
    a2 = mediatheque.inscrire("Modou")
    mediatheque.emprunter(a1.numero, "L001")
    with pytest.raises(DocumentIndisponible):
        mediatheque.emprunter(a2.numero, "L001")


def test_limite_emprunts(mediatheque):
    adherent = mediatheque.inscrire("Fatou")
    mediatheque.emprunter(adherent.numero, "L001")
    mediatheque.emprunter(adherent.numero, "L002")
    mediatheque.emprunter(adherent.numero, "L003")
    with pytest.raises(TropDEmprunts):
        mediatheque.emprunter(adherent.numero, "D001")


def test_adherent_inconnu_leve_document_inconnu(mediatheque):
    with pytest.raises(DocumentInconnu):
        mediatheque.emprunter("A999", "L001")


def test_document_inconnu_leve_document_inconnu(mediatheque):
    adherent = mediatheque.inscrire("Fatou")
    with pytest.raises(DocumentInconnu):
        mediatheque.emprunter(adherent.numero, "L999")


def test_rendre_remet_le_document_disponible(mediatheque):
    adherent = mediatheque.inscrire("Fatou")
    mediatheque.emprunter(adherent.numero, "L001")
    mediatheque.rendre(adherent.numero, "L001")
    doc = mediatheque._documents["L001"]
    assert doc.disponible is True
    assert len(adherent) == 0


def test_rechercher_est_un_generateur(mediatheque):
    resultats = mediatheque.rechercher("livre")
    assert hasattr(resultats, "__next__")  # bien un generateur, pas une liste
    assert len(list(resultats)) == 3


def test_documents_disponibles(mediatheque):
    adherent = mediatheque.inscrire("Fatou")
    mediatheque.emprunter(adherent.numero, "L001")
    disponibles = list(mediatheque.documents_disponibles())
    assert len(disponibles) == 3
    assert all(doc.code != "L001" for doc in disponibles)


def test_mediatheque_est_iterable_et_a_une_longueur(mediatheque):
    assert len(mediatheque) == 4
    assert len(list(mediatheque)) == 4


def test_aucun_pret_nest_en_retard_juste_apres_emprunt(mediatheque):
    adherent = mediatheque.inscrire("Fatou")
    mediatheque.emprunter(adherent.numero, "L001")
    assert list(mediatheque.prets_en_retard()) == []

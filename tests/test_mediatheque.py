import pytest
from mediatheque import Mediatheque, Livre, DVD, DocumentIndisponible, TropDEmprunts


def test_emprunt_rend_le_document_indisponible():
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    adherent = media.inscrire("Awa")

    media.emprunter(adherent.numero, "L001")

    assert not livre.disponible


def test_emprunter_document_deja_prete_lève_exception():
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    a = media.inscrire("Awa")
    m = media.inscrire("Moussa")

    media.emprunter(a.numero, "L001")

    with pytest.raises(DocumentIndisponible):
        media.emprunter(m.numero, "L001")


def test_quatrieme_emprunt_lève_trop_d_emprunts():
    media = Mediatheque("Test")
    for i in range(4):
        media.ajouter_document(Livre(f"Livre {i}", 2020, f"L{i:03d}"))
    adherent = media.inscrire("Awa")

    media.emprunter(adherent.numero, "L000")
    media.emprunter(adherent.numero, "L001")
    media.emprunter(adherent.numero, "L002")

    with pytest.raises(TropDEmprunts):
        media.emprunter(adherent.numero, "L003")


def test_rendre_document_le_remet_en_circulation():
    media = Mediatheque("Test")
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    media.ajouter_document(livre)
    adherent = media.inscrire("Awa")

    media.emprunter(adherent.numero, "L001")
    assert not livre.disponible

    media.rendre(adherent.numero, "L001")
    assert livre.disponible


def test_duree_pret_livre_et_dvd():
    livre = Livre("Titre", 2020, "L001", auteur="X", nb_pages=100)
    dvd = DVD("Film", 2020, "D001", realisateur="Y", duree_min=120)

    assert livre.duree_pret() == 21
    assert dvd.duree_pret() == 7


def test_rechercher_insensible_a_la_casse():
    media = Mediatheque("Test")
    media.ajouter_document(Livre("L'Aventure Ambiguë", 1961, "L001"))
    media.ajouter_document(DVD("Autre film", 2020, "D001"))

    resultats = media.rechercher("aventure")
    assert len(resultats) == 1
    assert resultats[0].code == "L001"

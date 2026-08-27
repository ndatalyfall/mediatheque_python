from mediatheque import Mediatheque, Livre, DVD, DocumentIndisponible, TropDEmprunts


def main():
    mediatheque = Mediatheque("Mediatheque de Dakar")

    mediatheque.ajouter_document(Livre("L'Aventure ambiguë", 1961, "L001",
                                       auteur="Cheikh Hamidou Kane", nb_pages=191))
    mediatheque.ajouter_document(DVD("Camp de Thiaroye", 1988, "D001",
                                     realisateur="Sembene Ousmane", duree_min=147))
    mediatheque.ajouter_document(Livre("Leikki", 2024, "L002",
                                       auteur="Boubacar Boris Diop", nb_pages=400))
    mediatheque.ajouter_document(DVD("Atlantiques", 2009, "D002",
                                     realisateur="Mati Diop", duree_min=15))

    awa = mediatheque.inscrire("Awa Diop")
    moussa = mediatheque.inscrire("Moussa Ndiaye")

    pret = mediatheque.emprunter(awa.numero, "L001")
    print(pret)

    mediatheque.emprunter(awa.numero, "D001")
    mediatheque.emprunter(awa.numero, "L002")

    print(f"Emprunts de {awa.nom} : {len(awa)}")

    try:
        mediatheque.emprunter(awa.numero, "D002")
    except TropDEmprunts as err:
        print(f"Impossible : {err}")

    try:
        mediatheque.emprunter(awa.numero, "L001")
    except DocumentIndisponible as err:
        print(f"Impossible : {err}")

    print("\n--- Documents disponibles ---")
    for doc in mediatheque.documents_disponibles():
        print(doc)

    print("\n--- Recherche 'aventure' ---")
    for doc in mediatheque.rechercher("aventure"):
        print(doc)

    print(f"\n--- Emprunts de {awa.nom} ---")
    for doc in mediatheque.emprunts_de(awa.numero):
        print(doc)

    mediatheque.rendre(awa.numero, "L001")
    print(f"\nAprès retour de L001, emprunts de {awa.nom} : {len(awa)}")
    print(f"L001 disponible ? {mediatheque._documents['L001'].disponible}")

    pret2 = mediatheque.emprunter(moussa.numero, "L001")
    print(f"\n{pret2}")

    print("\n--- Tous les documents disponibles ---")
    for doc in mediatheque.documents_disponibles():
        print(doc)

    print(f"\nNombre total de documents dans la mediatheque : {len(mediatheque)}")

    print("\n--- Tous les documents (via __iter__) ---")
    for doc in mediatheque:
        print(doc)


if __name__ == "__main__":
    main()
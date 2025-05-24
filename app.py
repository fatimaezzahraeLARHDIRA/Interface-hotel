import streamlit as st
import sqlite3

def connect_db():
    return sqlite3.connect("hotel.db")

st.title("Test Streamlit + SQLite")

menu = st.sidebar.selectbox("Menu", ["Voir clients", "Voir réservations"])

conn = connect_db()
cursor = conn.cursor()

if menu == "Voir clients":
    st.subheader("Liste des clients")
    cursor.execute("SELECT * FROM Client")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)

elif menu == "Voir réservations":
    st.subheader("Liste des réservations")
    cursor.execute("SELECT * FROM Reservation")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)

menu = st.sidebar.selectbox("Menu", [
    "Liste des réservations",
    "Liste des clients",
    "Ajouter un client",
    "Ajouter une réservation"
])
if menu == "Ajouter un client":
    st.subheader("Ajouter un nouveau client")

    nom = st.text_input("Nom complet")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.number_input("Code postal", step=1)
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")

    if st.button("Ajouter le client"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Client (nom_complet, adresse, ville, code_postal, email, telephone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, adresse, ville, code_postal, email, telephone))
        conn.commit()
        conn.close()
        st.success("Client ajouté avec succès ✅")
if menu == "Ajouter une réservation":
	st.subheader("Ajouter une réservation")

id_client = st.number_input("ID du client", step=1)
id_chambre = st.number_input("ID de la chambre", step=1)
date_debut = st.date_input("Date de début")
date_fin = st.date_input("Date de fin")

if st.button("Ajouter la réservation"):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Reservation (date_debut, date_fin, id_client, id_chambre)
        VALUES (?, ?, ?, ?)
    """, (date_debut, date_fin, id_client, id_chambre))
    conn.commit()
    conn.close()
    st.success("Réservation ajoutée avec succès ✅")
menu = st.sidebar.selectbox("Menu", [
    "Liste des réservations",
    "Liste des clients",
    "Ajouter un client",
    "Ajouter une réservation",
    "Chambres disponibles"
])
if menu == "Chambres disponibles":
    st.subheader("Rechercher les chambres disponibles")

    date_debut = st.date_input("Date de début", key="debut_chambre")
    date_fin = st.date_input("Date de fin", key="fin_chambre")

    if st.button("Rechercher"):
        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT * FROM Chambre
        WHERE id NOT IN (
            SELECT id_chambre FROM Reservation
            WHERE (? BETWEEN date_debut AND date_fin)
            OR (? BETWEEN date_debut AND date_fin)
            OR (date_debut BETWEEN ? AND ?)
        );
        """

        cursor.execute(query, (date_debut, date_fin, date_debut, date_fin))
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                st.write(row)
        else:
            st.info("Aucune chambre disponible pour cette période.")

        conn.close()


conn.close()

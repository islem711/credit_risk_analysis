import streamlit as st
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# Charger le modèle entraîné
model = joblib.load('./models/best_model.pkl')
preprocessing_pipeline = joblib.load('./models/preprocessing_pipeline.pkl')

# Créer une fonction pour faire des prédictions
def make_prediction(age, income, employment_length, loan_amount, loan_percent_income,
                    credit_hist_length, home_ownership, loan_intent, loan_grade, default_on_file):
    input_data = pd.DataFrame({
        'person_age': [age],
        'person_income': [income],
        'person_emp_length': [employment_length],
        'loan_amnt': [loan_amount],
        'loan_percent_income': [loan_percent_income],
        'cb_person_cred_hist_length': [credit_hist_length],
        'person_home_ownership': [home_ownership],
        'loan_intent': [loan_intent],
        'loan_grade': [loan_grade],
        'cb_person_default_on_file': [default_on_file]
    })
    
    preprocessed_input = preprocessing_pipeline.transform(input_data)
    prediction = model.predict(preprocessed_input)
    return prediction[0]

st.set_page_config(page_title="Simulateur de Prêt", layout="wide")
# Interface utilisateur avec Streamlit
background = Image.open('./img/heading.jpg')
good = Image.open('./img/good.png')
bad = Image.open('./img/bad.png')
nouvelle_largeur = 300
nouvelle_hauteur = 300

# Redimensionner l'image
good = good.resize((nouvelle_largeur, nouvelle_hauteur))
bad = bad.resize((nouvelle_largeur, nouvelle_hauteur))

# Exécuter l'application avec Streamlit
if __name__ == '__main__':
    st.sidebar.title("Menu")
    st.sidebar.subheader("Que voulez-vous faire ?")
    selected_option = st.sidebar.selectbox("Choisissez une option", ["Prédire un emprunteur", "À propos"])

    if selected_option == "Prédire un emprunteur":
        st.sidebar.success("Entrez les détails de l'emprunteur dans le formulaire ci-dessus.")
        st.sidebar.warning("Les résultats de prédiction apparaîtront en bas du formulaire.")
        # Define your custom CSS style for the div
        custom_style = """
            <style>
            .custom-div {
                background-color: #4169E1;
                padding: 20px;
                border-radius: 10px;
                border: 3px solid black;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
                text-align: center;
                color: white;
                
            }
            </style>
        """
        # Render the custom CSS style
        st.markdown(custom_style, unsafe_allow_html=True)

        # Use the custom class "custom-div" in your div
        st.markdown('<div class="custom-div"><h1 style ="color: white;">Simulateur de Prêt </h1><h2 style ="color: white">Entrez les détails du futur emprunteur :</h2></div>', unsafe_allow_html=True)        
        age = st.slider("Age", 18, 100, 30)
        income = st.number_input("Revenu annuel", 0, 1000000, 50000)
        employment_length = st.slider("Durée d'emploi en années", 0, 50, 5)
        loan_amount = st.number_input("Montant du prêt", 0, 1000000, 10000)
        loan_percent_income = st.slider("Pourcentage du revenu à utiliser pour le remboursement", 0, 100, 20)
        credit_hist_length = st.slider("Ancienneté du crédit en mois", 0, 1000, 200)
        home_ownership = st.selectbox("Type de propriété", ["RENT", "OWN", "MORTGAGE", "OTHER"])
        loan_intent = st.selectbox("Raison du prêt", ['EDUCATION', 'MEDICAL', 'VENTURE', 'PERSONAL', 'DEBTCONSOLIDATION', 'HOMEIMPROVEMENT'])
        loan_grade = st.selectbox("Grade du prêt", ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        default_on_file = st.selectbox("A-t-il déjà fait défaut ?", ["Y", "N"])
        if st.button("Prédire"):
            prediction = make_prediction(age, income, employment_length, loan_amount, loan_percent_income,
                                        credit_hist_length, home_ownership, loan_intent, loan_grade, default_on_file)
            if prediction == 1:
                # Centrer l'image dans Streamlit en utilisant des colonnes
                col1, col2, col3 = st.columns([1, 2, 1])  # Trois colonnes pour centrer l'image

                # Colonne vide pour centrer l'image horizontalement
                col1.write("")

                # Colonne du milieu pour afficher l'image redimensionnée
                col2.image(bad)

                # Colonne vide pour centrer l'image horizontalement
                col3.write("")
                st.error("Le futur emprunteur est considéré comme risqué pour le prêt.")

            else:
                # Centrer l'image dans Streamlit en utilisant des colonnes
                col1, col2, col3 = st.columns([1, 2, 1])  # Trois colonnes pour centrer l'image

                # Colonne vide pour centrer l'image horizontalement
                col1.write("")

                # Colonne du milieu pour afficher l'image redimensionnée
                col2.image(good)

                # Colonne vide pour centrer l'image horizontalement
                col3.write("")
                st.success("Le futur emprunteur est considéré comme éligible pour le prêt.")


        st.markdown('</div>', unsafe_allow_html=True)
    else:
        ## Displaying the image:
        st.image(background,use_column_width=True)
        st.sidebar.info("Ce simulateur est créé avec Streamlit.")
        st.sidebar.info("Auteur : BEGGARI MOHAMED ISLEM")
        st.sidebar.info("Contact : mohamed.islem.beggari@etu.univ-st-etienne.fr")
from datetime import timedelta
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy.sql import text


# Title of the app
title_template="""
    <div style="background-color:rgb(235, 238, 245);border-radius:12px; padding:8px;">
    <h1 style="color:rgb(3, 24, 66)"> Cambio de unidades volumen</h1>
    </div> """

# st.title('title_template')
st.markdown(title_template, unsafe_allow_html=True)
    
subheader_template="""
    <div style="background-color: white; padding:8px;">
    <h3 style="color:rgb(202, 240, 248)"> By Valtic</h3>
    </div> """
    
st.markdown(subheader_template, unsafe_allow_html=True)

opciones_menu=["Home", "Litros -> galones (us)",
                     "Galones -> litros",
                      "gpm (us) -> litros/hora",
                       "litros/h -> gpm(us)"]

# Sidebar menu for navigation
menu = st.sidebar.selectbox("Selecciona una opción", opciones_menu)

# Home
if menu == opciones_menu[0]: #HOME
    st.header("Conversion unidades de Volumen")
    st.write("Usa el menu lateral para seleccionar una calculadora")

    conn = st.connection('pets_db', type='sql')

    with conn.session as s:
        st.markdown(f"Note that `s` is a `{type(s)}`")
        s.execute(text('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);'))
        s.execute(text('DELETE FROM pet_owners;'))
        pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
        for k in pet_owners:
            s.execute(text(
                'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);'),
                params=dict(owner=k, pet=pet_owners[k])
            )
        s.commit()

    pet_owners = conn.query('select * from pet_owners', ttl=timedelta(minutes=10))
    st.dataframe(pet_owners)

# gal to l.
elif menu == opciones_menu[1] or menu == opciones_menu[2]: #"Galones -> litros"
    st.header("Galones (us) a Litros")
    galones = st.number_input("Escribe volumen en galones para calcular en litros",step=1.0)
    if galones:
        litros = galones * 3.785412
        st.write(f"Resultado: {galones:.2f} gal son {litros:.2f} litros.")

    # L to gal.
    st.header("Litros a Galones(us)")
    litros_2 = st.number_input("Escribe volumen en litros para calcular en galones(us)",step=1.0)
    if litros_2:
        galones_2 = litros_2 / 3.785412
        st.write(f"Resultado: {litros_2:.2f} litros son {galones_2:.2f} galones.")


# gmp to l/h.
elif menu == opciones_menu[3] or menu == opciones_menu[4]: 
    #"Galones por minuto -> litros/hora"
    st.header("Galones por minuto (us) a Litros/hora")
    gpm = st.number_input("Escribe volumen en galones para calcular en litros",step=1.0)
    if gpm:
        litros_hora = ( gpm * 3.785412 ) * 60
        st.write(f"Resultado: {gpm:.2f} gpm (us) son {litros_hora:.2f} litros/hora.")

# l/h to gpm.
#elif menu == opciones_menu[4]: #"Litros/hora -> Galones por minuto"
    st.header("Litros/hora a Galones por minuto (us)")
    litros_hora_ = st.number_input("Escribe volumen en litros para calcular en galones(us)",step=1.0)
    if litros_hora_:
        galones_pmim = ( litros_hora_ / 3.785412) / 60
        st.write(f"Resultado: {litros_hora_:.2f} litros/hora son {galones_pmim:.2f} gpm (us).")



# Plot Sine Wave
elif menu == "Plot Sine Wave":
    st.header("Plot Sine Wave")
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    st.pyplot(plt)

# Plot CSV Data
elif menu == "Plot CSV Data":
    st.header("Plot CSV Data")
    uploaded_file = st.file_uploader("Choose a CSV file")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)
        st.line_chart(data)


import streamlit as st
import pandas as pd
import numpy as np
import requests

#url = 'http://127.0.0.1:8000/predictions'  # URL del endpoint de la API FastAPI
url = 'http://backend:8000/predictions'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def execute_prediction(datos: pd.DataFrame):
    """
    Función para enviar datos a la API y recibir una predicción.
    """
    payload = datos.to_json(orient='records')       

    print('datos en execute_prediction ',payload)

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        # Si la respuesta es exitosa, devuelve el diagnóstico
        result = response.json()
        print('resultado en execute_prediction',result)
        return result['diagnostico']
    else:
        # Si hay un error, devuelve None
        print('Error en la predicción:', response.status_code)
        return None

st.set_page_config(
    page_title="App para detección de enfermedades",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="auto")

header_container = st.container()

# Set the page configuration


with header_container:
    # Set the title of the app
    st.title("App para detección de enfermedades")
    st.subheader("Esta app es un prototipo para detectar enfermedades a partir de sintomas, no es un diagnóstico médico.")
    st.write("¿Cómo funciona?, digita los sintomas y el sistema te dará un diagnóstico. ")
    st.subheader("Datos del paciente : ")

with st.form(key='my_form'):
    # Create a form for user input
    politica = st.checkbox('Acepto el uso de mis datos para fines de investigación ')
    nm_paciente = st.text_input('Digite el nombre del paciente :')
    sintomas = st.text_area('Digite algunos sintomas :')
    edad = st.select_slider('Edad del paciente :', options=[i for i in range(0,120)])
    genero = st.radio('Genero del paciente :',['Masculino','Femenino','Otro'])
    genero = 1 if genero == 'Masculino' else (2 if genero == 'Femenino' else 0)    
    temperatura = st.number_input('Temperatura del paciente ('+chr(176)+'C) :', min_value=30, max_value=45, step=1)
    glucosa = st.number_input('Nivel de glucosa en sangre (mg/dL) :', min_value=0, max_value=500, step=1)
    presion = st.number_input('Presión arterial (mmHg) :', min_value=0, max_value=300, step=1)
    urgencia = st.select_slider('Severidad de la condición del paciente (siento 1 no tan critico y 10 estado muy critico) :', options=[i for i in range(1,11)])
    btn = st.form_submit_button('Enviar')

# Check if the button was clicked
if btn == False:
    st.write("Por favor, acepte el uso de sus datos para fines de investigación y complete todos los campos.")

if btn == True:
    try:    
    # Check if the user has accepted the policy
     if politica:
            # Create a DataFrame with the input data
            data = {
                'Nombre': [nm_paciente],
                'Sintomas': [sintomas],
                'Temperatura': [temperatura],
                'Genero': [genero],
                'Edad': [edad],
                'Glucosa': [glucosa],
                'Presion': [presion],
                'Urgencia': [urgencia]
            }
            df = pd.DataFrame(data)
            
            # Display the DataFrame
            st.write("Datos del paciente:")
            st.dataframe(df)
            
            diagnostico = execute_prediction(df)

            # Call the get_diagnostico function to get a random diagnosis
            st.write("El diagnóstico de su paciente es:", diagnostico)
     else:
            st.write("Por favor, acepte el uso de sus datos para fines de investigación.")
    except Exception as e:
        st.write("Ocurrió un error al procesar los datos. Por favor, inténtelo de nuevo.")
        st.error(f"Error: {e}")
 
 
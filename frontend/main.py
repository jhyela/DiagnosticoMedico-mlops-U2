import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import logging
import socket

#url = 'http://127.0.0.1:8000/predictions'  # URL del endpoint de la API FastAPI
url = 'http://backend:8000/predictions'

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def es_host_activo(host, puerto):
    try:
        # Crea un socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Establece un tiempo de espera de 2 segundos
            s.connect((host, puerto))
        return True
    except socket.timeout:
        return False
    except Exception:
        return False
    
def execute_prediction(datos: dict):
    """
    Función para enviar datos a la API y recibir una predicción.
    """    
    try:
        # Realiza la solicitud POST a la API
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
    except requests.exceptions.HTTPError as http_err:   
        if response.status_code == 422:
            print('Error en la predicción: Datos no válidos 422')
        else:
            print(f'Error en la predicción: {http_err}')
        return None
    except requests.exceptions.Timeout:
        print('Error en la predicción: Tiempo de espera agotado')
        return None
    except requests.exceptions.TooManyRedirects:
        print('Error en la predicción: Demasiadas redirecciones')
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud a la API: {e}")
        print('Error en la predicción: No se pudo conectar a la API')
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

    if response.status_code == 200:
        # Si la respuesta es exitosa, devuelve el diagnóstico
        result = response.json()
        print('resultado en execute_prediction',result)
        return result['diagnostico'] + " con probabilidad de " + str(result['probabilidad']) + "%"
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
    genero = st.radio('Género del paciente :',['Masculino','Femenino'])
    genero = 1 if genero == 'Masculino' else (2 if genero == 'Femenino' else 0)    
    temperatura = st.number_input('Temperatura del paciente ('+chr(176)+'C) :', min_value=30, max_value=45, step=1)
    glucosa = st.number_input('Nivel de glucosa en sangre (mg/dL) :', min_value=0, max_value=500, step=1)
    presion = st.number_input('Presión arterial (mmHg) :', min_value=0, max_value=300, step=1)
    urgencia = st.select_slider('Severidad de la condición del paciente (siento 1 no tan crítico y 10 estado muy crítico) :', options=[i for i in range(1,11)])
    btn = st.form_submit_button('Enviar')

st.divider()
url2 = "http://127.0.0.1:8000/reportes"
st.markdown(f'<a href="{url2}" target="_blank" style="text-decoration: none;">Ver datos históricos</button></a>',unsafe_allow_html=True)
st.divider()

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
            
            try:
               diagnostico = execute_prediction(data)
            except Exception as e:
                st.write("Ocurrió un error al procesar los datos. Por favor, inténtelo de nuevo.")
                st.error(f"Error: {e}")                

            # Call the get_diagnostico function to get a random diagnosis
            st.write("El diagnóstico de su paciente es:", diagnostico)
     else:
            st.write("Por favor, acepte el uso de sus datos para fines de investigación.")
    except Exception as e:
        st.write("Ocurrió un error al procesar los datos. Por favor, inténtelo de nuevo.")
        st.error(f"Error: {e}")
 
 
from model.modelo_ML import get_diagnostico

import pandas as pd 
from fastapi import FastAPI
import uvicorn
import logging
import os
import datetime
import re


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)
logger.log(logging.INFO, "Iniciando la aplicación FastAPI")

app = FastAPI()

@app.get('/')
async def root():  
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la API de predicción de diagnóstico "+__name__+"."}


@app.get('/reportes')
async def get_datos_historicos():  
    
    print("Dentro de reportes")

    filename = "/storage/historicos.csv"
    sano = 0
    leve = 0
    aguda = 0
    cronica = 0
    terminal = 0
    num_lineas = 0
    fecha = None
    lineas_5 = ""

    if os.path.isfile(filename):
     try:
      with open(filename, "r",encoding="utf-8") as archivo:
       lineas = archivo.readlines()
       num_lineas  = len(lineas)
      for linea in lineas:
        fecha = (linea.split(';')[2]).strip()       
        if linea.find("NO ENFERMO") != -1:
            sano += 1
        elif linea.find("ENFERMEDAD LEVE") != -1:        
            leve += 1            
        elif linea.find("ENFERMEDAD AGUDA") != -1:
            aguda += 1    
        elif linea.find("ENFERMEDAD CRÓNICA") != -1:
            cronica += 1       
        else :
            terminal += 1                          
        
        if num_lineas > 5:
          last_5_lines = lineas[-5:]
          lineas_5 = ""
          for line in last_5_lines:
           lineas_5 = lineas_5 + line.split(';')[0].strip() + ","
    
     except FileNotFoundError:
      print("El archivo de datos históricos no fue encontrado.")     
      return {"message": "El archivo de datos históricos no fue encontrado."}

    return {"NO ENFERMO": sano,
            "ENFERMEDAD LEVE": leve,
            "ENFERMEDAD AGUDA": aguda,
            "ENFERMEDAD CRÓNICA": cronica,
            "ENFERMEDAD TERMINAL": terminal,
            "FECHA ÚLTIMA PREDICCIÓN": fecha,
            "ÚLTIMAS 5 PREDICCIONES": lineas_5 [:-1]
        }   


@app.post('/predictions')
async def procesar_diagnostico(data: dict):
    """
    Endpoint para recibir datos y devolver una predicción.
    """
    separador = ";"
    filename = "/storage/historicos.csv"
    
    try:
        datos = pd.DataFrame.from_dict({k: [v] for k, v in data.items()})

    except Exception as e:
        print(f"Error al convertir los datos a DataFrame: {e}")
        logger.error(f"Error al convertir los datos a DataFrame: {e}")
        return {"error": "Error al procesar los datos"}
    
    print("Datos recibidos (backend):", datos,str(type(datos)))
    #print("Datos recibidos (backend):", datos.to_dict(orient='records')[0])

    logger.info("Recibiendo datos para predicción")
   
    now = datetime.datetime.now()

    df_diagnostico = {}
    df_diagnostico['Nombre'] = datos['Nombre'].values[0]
    df_diagnostico['Sintomas'] = datos['Sintomas'].values[0]
    df_diagnostico['Sexo'] = datos['Sexo'].values[0]
    df_diagnostico['Urgencia'] = datos['Urgencia'].values[0]
    df_diagnostico['Edad'] = datos['Edad'].values[0]
    df_diagnostico['Glucosa'] = datos['Glucosa'].values[0]
    df_diagnostico['Presion'] = datos['Presion'].values[0]
    df_diagnostico['Temperatura'] = datos['Temperatura'].values[0]
    
    df_diagnostico = pd.DataFrame(df_diagnostico, index=[0])

    print("Datos para el modelo (backend):", df_diagnostico)
    
    try :
        prediction,probabilidad = get_diagnostico(df_diagnostico)
               
        print("Predicción en backend:", prediction,probabilidad)  
        
    except Exception as e:
        logger.error(f"Error en la predicción: {e}")
        print(f"Error en la predicción: {e}")    
        return {"error": "Error en la predicción"}
    
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    if os.path.isfile(filename):
        try:

          with open(filename, "a+") as f:
           f.write(prediction + separador + str(probabilidad) + separador + date_string + "\n")  
        except Exception as e:
           logger.error(f"Error al escribir en el histórico de datos: {e}")
    else:
        try:
          with open(filename, "w") as f:
              f.write(prediction + separador + str(probabilidad) + separador + date_string + "\n")  
        except Exception as e:
           logger.error(f"Error al escribir en el histórico de datos: {e}")
           
    return {'diagnostico': prediction, 'probabilidad': str(probabilidad)}


if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000, reload=True)
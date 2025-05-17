import numpy as np
import pandas as pd
import joblib
import os
import imblearn
import logging

df_diagnostico = {
                  'diagnostico' : ['NO ENFERMO', 'ENFERMEDAD LEVE','ENFERMEDAD AGUDA','ENFERMEDAD CRÓNICA','ENFERMEDAD TERMINAL']
                  }
df_diagnostico = pd.DataFrame(df_diagnostico, index=[0,1,2,3,4])

df_diagnostico

logger = logging.getLogger(__name__)

def get_diagnostico(datos):
    """
    Esta función genera un diagnóstico aleatorio a partir de una lista de diagnósticos predefinidos.
    """
    
    print("En ML datos :" + str(type(datos)))

    columnas = ['Glucosa','Presion','Edad','Sexo','Temperatura','Urgencia']
 

    datos_pre = pd.DataFrame(datos[columnas])

    print("En ML datos_pre :" + str(type(datos_pre)))

    input_array = datos_pre[columnas].to_numpy()

    dir_path = os.path.dirname(__file__)
    filemodel = 'modelo_entrenado.pkl'
    file_path = os.path.join(dir_path, filemodel)
    

    print("********************************************")

    print("Datos para el modelo numpy:", input_array)
    logger.info("DataFrame final con columnas ordenadas:\n%s", input_array)

    print("********************************************")
    try:
        if os.path.exists(file_path):
        #if os.path.isfile(filemodel):
            # Cargar el modelo entrenado
            try:                
                modelo = joblib.load("/app/model/modelo_entrenado.pkl")
                
                print("Modelo cargado exitosamente.")
                logger.info("Modelo cargado exitosamente.")
                
                new_pred = modelo.predict(input_array)
                new_pred_proba = modelo.predict_proba(input_array)
                
                print("En modelo prediccion : --> ", new_pred,new_pred[0])
                print("En modelo probabilidad : --> ", new_pred_proba,new_pred_proba[0][0])

                return df_diagnostico.loc[new_pred[0], 'diagnostico'],np.round(new_pred_proba[0][0],3)

                #return "ENFERMEDAD AGUDA", 0.85
            
            except Exception as e:
                print("Error al cargar el modelo:", e)
                logger.error(f"Error cargando modelo: {str(e)}")
                return "Error al cargar el modelo " + str(e), -9
            
        else:
            print("El modelo no se encuentra disponible :",file_path)
            return None, None

    except Exception as e:
        print("Error al cargar el modelo:", e)
        return None, None
   
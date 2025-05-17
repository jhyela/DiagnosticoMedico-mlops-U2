import numpy as np
import pandas as pd
import joblib
import os
import imblearn

df_diagnostico = {
                  'diagnostico' : ['NO ENFERMO', 'ENFERMEDAD LEVE','ENFERMEDAD AGUDA','ENFERMEDAD CRÓNICA','ENFERMEDAD TERMINAL']
                  }
df_diagnostico = pd.DataFrame(df_diagnostico, index=[0,1,2,3,4])

df_diagnostico

def get_diagnostico(datos):
    """
    Esta función genera un diagnóstico aleatorio a partir de una lista de diagnósticos predefinidos.
    """
    
    datos_pre = datos[['Glucosa','Presion','Edad','Sexo','Temperatura','Urgencia']] 
   
    dir_path = os.path.dirname(__file__)
    filemodel = 'modelo_entrenado.pkl'

    file_path = os.path.join(dir_path, filemodel)

    print('directorio actual :',dir_path)
    contenido = os.listdir(dir_path)
    print("Contenido del directorio:", contenido)
    print("********************************************")
    
    print("Datos para el modelo:", datos_pre)
    
    print("********************************************")
    try:
        if os.path.exists(file_path):
            # Cargar el modelo entrenado
            try:
                modelo = joblib.load(file_path)
                
                print("Modelo cargado exitosamente.")
                
                new_pred = modelo.predict(datos_pre)
                new_pred_proba = modelo.predict_proba(datos_pre)
                

                print("En modelo prediccion : --> ", new_pred,new_pred[0])
                print("En modelo probabilidad : --> ", new_pred_proba,new_pred_proba[0][0])

                return df_diagnostico.loc[new_pred[0], 'diagnostico'],np.round(new_pred_proba[0][0],3)
            
            except Exception as e:
                print("Error al cargar el modelo:", e)
                return "Error" , -1
            
        else:
            print("El modelo no se encuentra disponible. ",file_path)
            return None, None

    except Exception as e:
        print("Error al cargar el modelo:", e)
        return None, None
   
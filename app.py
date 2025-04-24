from model.modelo_ML import get_diagnostico
import pandas as pd 
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)


app = FastAPI()

@app.post('/predictions')
async def procesar_diagnostico():
    """
    Endpoint para recibir datos y devolver una predicción.
    """
    logger.info("Recibiendo datos para predicción")
    try :
        prediction = get_diagnostico()
        print("Predicción en appp.py:", prediction)  
    except Exception as e:
        #logger.error(f"Error en la predicción: {e}")
        print(f"Error en la predicción: {e}")    
        return {"error": "Error en la predicción"}
    return {'diagnostico': prediction[0]}
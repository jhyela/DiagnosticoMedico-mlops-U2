import numpy as np

diagnosticos = ['NO ENFERMO', 'ENFERMEDAD LEVE','ENFERMEDAD AGUDA','ENFERMEDAD CRÓNICA','ENFERMEDAD TERMINAL']

def get_diagnostico():
    """
    Esta función genera un diagnóstico aleatorio a partir de una lista de diagnósticos predefinidos.
    """
    # Genera un diagnóstico aleatorio
    # Se elige un diagnóstico aleatorio de la lista de diagnósticos
    # y se devuelve como resultado.
    return np.random.choice(diagnosticos,1) , np.round(np.random.rand(), 3)

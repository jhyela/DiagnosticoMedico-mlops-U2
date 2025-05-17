import pandas as pd
import os
from backend.model.modelo_ML import get_diagnostico


d_test1 = {
        "Nombre":"Carlos Perez",
        "Sintomas":"tos",
        "Temperatura":38,
        "Sexo":1,
        "Edad":30,
        "Glucosa":30,
        "Presion":260,
        "Urgencia":3
}

d_test1 = pd.DataFrame(d_test1,
                       columns=['Glucosa','Presion','Edad','Sexo','Temperatura','Urgencia'],
                       index=[0])

d_test2 = {
        "Nombre":"Ana Garcia",
        "Sintomas":"daño de estomago",
        "Temperatura":40,
        "Sexo":2,
        "Edad":55,
        "Glucosa":90,
        "Presion":150,
        "Urgencia":9
}

d_test2 = pd.DataFrame(d_test2,
                       columns=['Glucosa','Presion','Edad','Sexo','Temperatura','Urgencia'],
                       index=[0])       

def test_diagnostico1():   
   a,b = get_diagnostico(d_test1)
   assert 'ENFERMEDAD LEVE' == 'ENFERMEDAD LEVE'

def test_diagnostico2():   
   a,b =  get_diagnostico(d_test2)
   assert 'ENFERMEDAD TERMINAL' == 'ENFERMEDAD TERMINAL'

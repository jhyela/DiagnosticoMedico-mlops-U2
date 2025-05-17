# Objetivo de este Repositorio Git
Repositorio para entregar las actividades de la materia Machine Learning Operations(MLOps) de la Maestria en IA - Universidad Icesi.

# Descripción del Problema
Dados los avances tecnológicos, en el campo de la medicina la cantidad de información que existe de los pacientes es muy abundante. Sin embargo, para algunas enfermedades no tan comunes, llamadas huérfanas, los datos que existen escasean. Se requiere construir un modelo que sea capaz de predecir, dados los datos de síntomas de un paciente, si es posible o no que este sufra de alguna enfermedad. Esto se requiere tanto para enfermedades comunes (muchos datos) como para enfermedades huérfanas (pocos datos).

# Diseño de Pipeline de ML
El siguiente modelo de pipeline de ML pretende dar solución a los requerimientos planteados en la descripción del problema anterior; el pipeline propuesto consiste en desplegar en producción un modelo de Machine Learning, que, según los datos de entrada, que en este caso serán datos relacionados con la salud y los síntomas de cada paciente, el modelo sea capaz de predecir el diagnostico de alguna de las siguientes categorías de enfermedades:

 - NO ENFERMO
 - ENFERMEDAD LEVE
 - ENFERMEDAD AGUDA
 - ENFERMEDAD CRÓNICA
 - ENFERMEDAD TERMINAL

![Pipeline Propuesto](./images/pipeline_ML-2025-04-23-2130.png)

# Fuente de Datos
Para solventar esta problemática, tenemos como input de datos las historias clínicas de cada paciente, adicionalmente esperamos contar con el resultado de las pruebas de laboratorio, los examenes previamente realizados a igual que cualquier diagnóstico médico que se le haya realizado al paciente y que no esté en su historia clínica. Por otro lado, esperamos tener acceso a bases de datos especializadas donde se encuentren diagnósticos de enfermedades raras al igual que enfermedades comunes que nos ayuden a poder clasificar los pacientes según sus síntomas.
Como base de datos de enfermedades raras se deberia tener acceso a base de datos como Orphanet o OMIM.

# Almacenamiento de Datos
Debido los diversos formatos que se podrían tener como datos estructurados y no estructurados, lo más recomendable es almacenar esta información en un data lake.

# Preparación de los Datos
En la etapa de preparación de datos esperamos hacer ingeniería de características (featuring engineering) y selección de características (feature selection) usando algoritmos tradicionales para esta tarea como PCA y LDA (análisis de discriminante lineal).

 Para balancear los datos principalmente por las enfermedades huérfanas, podemos usar técnicas como:
 - Oversampling: SMOTE o ADASYN para enfermedades huérfanas.
 - Undersampling: Si los datos comunes son abundantes.
 - Pesos en el modelo: Asignar mayor peso a la clase minoritaria.

# Selección y Evaluación de Modelos de ML
Para encontrar la mejor solución para el problema planteado, se propone utilizar algoritmos como Regresión logística múltiple, Random Forest, XGBoost, redes neuronales (MLP o Transformers) y ensambles como máquinas de soporte vectorial y GBM.

# Entrenamiento, Evaluación y Pruebas del Modelo
En esta parte de pipeline dividimos de forma aleatoria los datos de entrada en 3 partes para realizar entrenamiento, evaluación y pruebas, generalmente la división de datos se realiza en porcentaje de 70%, 20% y 10% respectivamente.
Para medir el desempeño de los modelos seleccionados se realizará una comparación en métricas como :

 - Accuracy (Presión): Proporción de predicciones correctas sobre el total.
 - Recall (Sensibilidad): Proporción de casos positivos reales detectados.
 - F1-score: Media armónica entre precisión y recall. Ideal para equilibrar ambas métricas.
 - MSE (Error Cuadrático Medio): Estimador mide el promedio de los errores al cuadrado.

 Para clases desbalanceadas debido principalmente a las enfermedades raras se podria utilizar:
 - Recall por clase (Sensibilidad por enfermedad): Asegurar que las enfermedades raras no se pasen por alto.
 - Precisión por clase: Evitar sobrediagnóstico de enfermedades raras.
 - Average Precision (AP): Versión ponderada del recall, útil para desbalance.

# Evaluación de Requerimientos del Negocio
En esta parte del pipeline evaluaremos si el modelo de Machine Learning seleccionado satisface las necesidades del negocio, si la clasificación de la gravedad de las enfermedades satisface los requerimientos de los interesados en el modelo de clasificación; si se concluye que el modelo no satisface las necesidades del negocio nos devolveremos hasta la fase de preparación de los datos y evalución de características y volveremos a iniciar el proceso.
Por otro lado, de ser satisfactoria la solución brindada por el modelo de ML, seguiremos adelante con el pipeline.

# Registro del Modelo de ML
Se realiza en el registro del modelo de ML para su posterior versionamiento, administración y seguimiento.
Este registro se podría realizar en herramientas como MLflow, Snowflake, Azure ML, Amazon SageMaker, GitLab o alguna otra herramienta que permita el registro del modelo de ML.

# Despliegue en Producción
Una vez el modelo de Machine Learning este entrenado, evaluado y validado, ya se encuentra listo para ser desplegado en producción. Para esta tarea generalmente se usa uno o varios contenedores Docker y opcionalmente se puede utilizar Kubernetes en caso de tener varios contenedores Docker.
Algunos de los servicios de infraetructura más usados en la nube utilizados para desplegar modelos de ML en producción son: Amazon web Services, Microsotf Azure y Google Cloud Platform.

Otra forma de desplegar este modelo de ML es exponiendo una API Rest para enviar datos al modelo y asi poder obtener la predicción de la posible enfermedad del paciente.

# Monitoreo
Esta tarea se realiza una vez la modelo esta desplegado en producción y el objetivo de esta es poder monitorear si el desempeño del modelo de ML sigue cumpliendo con las expectativas de los interesados o del negocio.
El desempeño del ML se puede degradar principalmente por cambios en los datos de entrada al mismo, o por cambios en los requerimientos por parte de los interesados o en algunos casos por la actualización de dependencias de alguno de los componentes del modelo.


# Aplicación para Detección de Enfermedades

El archivo principal de esta aplicación es docker-compose up -d --build.
La estructura de directorios del proyecto es: 


![Estructura de directorios](./images/directorios.JPG)

1. Correr en Docker el comando : 
        
        docker-compose up -d --build
   
    ![Contenedores Docker](./images/contenedores.JPG)
        
        Esto creara dos contenedores Backend y Frontend

2. En un browser ingresar al front mediante la URL: http://localhost:8501 , esto levantara una página de captura de datos en Stremalit como se ve en la siguiente imagen.
   
   ![Página de captura de datos](./images/Front_Streamlit.JPG)

3. Después de aceptar la política de uso de los datos y llenar los campos, el resultado del diagnóstico médico se visualizara en la parte inferior.

    ![Diagnóstico](./images/Front_Streamlit_diagnostico.JPG)

# Workshop_03 - Prediction and streaming data 
Autor: [@Johan901](https://github.com/Johan901)

---

## Bienvenidos
Dados los 5 archivos CSV que tienen información sobre el puntaje de felicidad en diferentes países, entrene un modelo de aprendizaje automático de regresión para predecir el puntaje de felicidad.


## ¿Qué verás en este proyecto?

1. Análisis y Preparación de Datos (EDA y ETL)
Revisar la calidad de los datos, limpiarlos y transformarlos.
Realizar análisis exploratorio para identificar patrones y correlaciones relevantes.
2. Desarrollo de Modelos de Regresión
Seleccionar variables y dividir los datos en entrenamiento y prueba.
Entrenar y evaluar varios modelos de regresión, seleccionando el mejor en base a métricas de rendimiento.
3. Implementación de Transmisión de Datos con Kafka
Configurar Kafka y crear productores y consumidores para transmitir datos en tiempo real.
Probar el flujo de datos para asegurar una comunicación efectiva entre los componentes.
4. Predicción y Almacenamiento de Resultados
Integrar el modelo de predicción en el consumidor de Kafka para hacer predicciones en tiempo real.
Guardar los resultados en una base de datos y automatizar el proceso para un flujo continuo de predicciones.



## Corre este proyecto


1. clona mi repositorio:
```bash
   git clone https://github.com/Johan901/Wokshop3.git
 ```

2. Go to the project directory  
```bash
   cd WORKSHOP3
```


- Corre el producer y el consumer:

  - **producer**
    
    ```bash
    python producer.py
    ```
    
  - **consumer**
    
    ```bash
    python consumer.py
    ```


## Thank you for visiting this repository.
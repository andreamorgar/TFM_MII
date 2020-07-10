**Trabajo Fin de Máster del Máster Profesional en Ingeniería Informática**

Autora: Andrea Morales Garzón

Curso 2019-2020

Universidad de Granada

# Aprendizaje predictivo en Nutrición

La integración de datos heterogéneos es una tarea indispensable en múltiples dominios y, en especial, en el área de Food Computing. Los grandes volúmenes de datos que intervienen, el vocabulario hiperespecializado, los factores multiculturales y las asunciones en el lenguaje alimenticio la convierten en una tarea difícil de abordar. En este trabajo se propone un método general basado en modelos predictivos del lenguaje para alinear fuentes de datos a partir de las descripciones textuales de sus elementos. En concreto, se ha desarrollado un sistema que combina un modelo predictivo de tipo *Word Embedding* para representar los datos textuales y un procedimiento de mapeo entre ítems basado en medidas de distancia sintácticas y semánticas, tanto clásicas y difusas. Con el fin de reflejar sus capacidades y su versatilidad, el sistema se ha aplicado para resolver un problema de interés actual: la adaptación automatizada de recetas a restricciones alimenticias. Las pruebas empíricas realizadas muestran que esta aproximación es apropiada para resolver el problema, especialmente cuando se combinan modelos semánticos específicos con medidas de distancia difusas.


## Estructura de ficheros

- [data](https://github.com/andreamorgar/TFM_MII/tree/master/data): directorio que contiene archivos con datos externos, pero utilizados dentro del proyecto.
- [docs](https://github.com/andreamorgar/TFM_MII/tree/master/docs): directorio que contiene los ficheros latex para el desarrollo de la memoria.
- [excels](https://github.com/andreamorgar/TFM_MII/tree/master/excels): directorio en el que se almacenan los resultados del módulo de mapeo.
    - [Mapeos (experimentación)](https://github.com/andreamorgar/TFM_MII/tree/master/excels/idiet-mapping): mapeos resultantes en función de las medidas utilizadas.
    - [Resultados en la precisión de los mapeos](https://github.com/andreamorgar/TFM_MII/tree/master/excels/accuracy): precisión en los mapeos en función de las medidas utilizadas.
- [files](https://github.com/andreamorgar/TFM_MII/tree/master/files): directorio con los códigos implementados en el TFM.
    
    Código relevante:
    - [Implementación del modelo de Word Embedding](https://github.com/andreamorgar/TFM_MII/tree/master/files/word-embedding.py)
    - [Implementación de las medidas de distancia difusas](https://github.com/andreamorgar/TFM_MII/tree/master/files/fjaccard.py)
    - [Mapeo entre bases de datos](https://github.com/andreamorgar/TFM_MII/tree/master/files/usda-correspondences-and-accuracy.py)
    - [Adaptación de recetas a restricciones alimenticias](https://github.com/andreamorgar/TFM_MII/tree/master/files/adapt-ingredients.py)
    - [Back-end de la aplicación](https://github.com/andreamorgar/TFM_MII/tree/master/files/app): código de la implementación de la aplicación móvil
        - [Implementación de la API](https://github.com/andreamorgar/TFM_MII/tree/master/files/app/api_flask.py)
        - [Utilidades para la API](https://github.com/andreamorgar/TFM_MII/tree/master/files/app/utils.py)
        - [Modelo de datos de receta](https://github.com/andreamorgar/TFM_MII/tree/master/files/app/recipe_class.py)
        - [Conexión con la base de datos](https://github.com/andreamorgar/TFM_MII/tree/master/files/app/recipesdb.py)

    Ficheros auxiliares:
    - [Script para generar gráficas para la memoria](https://github.com/andreamorgar/TFM_MII/tree/master/files/grafica_mapeo_parametro.py)
    - [Script utilizado para obtener los textos del dataset de archives.org](https://github.com/andreamorgar/TFM_MII/tree/master/files/crear-ficheros-texto-plano.py)
    - [Pruebas preliminares con n-gramas](https://github.com/andreamorgar/TFM_MII/tree/master/files/n-gramas.py)
    - [Código para visualizaciones de Word Embedding](https://github.com/andreamorgar/TFM_MII/tree/master/files/vocabulary_model_info.py)
  
- [memoria_latex](https://github.com/andreamorgar/TFM_MII/tree/master/memoria_latex): ficheros latex para la memoria del trabajo.
- [memoria](https://github.com/andreamorgar/TFM_MII/blob/master/memoria.pdf): memoria del trabajo en formato PDF.
- [models](https://github.com/andreamorgar/TFM_MII/tree/master/models): modelos guardados, generados y entrenados en el proyecto.
- [recipes](https://github.com/andreamorgar/TFM_MII/tree/master/recipes): directorio con los textos de las recetas, clasificados en subdirectorios según de donde provenga la receta. Estos ficheros son los que se utilizan como corpus de entreamiento del modelo de Word Embedding.
- [Vídeo con la demostración del funcionamiento de la aplicación](https://github.com/andreamorgar/TFM_MII/tree/master/videos)


## Manual de uso de la aplicación

### Dependencias
- Python 3.7.3
  - Gensim 3.8.3 
- Mongo 4.2.7
- Flask 1.1.1
- Ionic 5.2.3
  - Utility:
    - cordova-res : not installed
    - native-run  : 0.2.9 (update available: 1.0.0)



  - System:
    - NodeJS : v10.16.0
    - npm    : 6.13.3
    - OS     : Linux 5.0 

### Ejecución de la aplicación

Primero hay que asegurar que el servicio de la base de datos esté funcionando. Para iniciarlo:
~~~
$ systemctl start mongod
~~~

Inicialmente, esta base de datos está vacía, por lo que hay que llenarla con recetas. Entramos a la base de datos:
~~~
$ mongo
~~~

Dentro de la base de datos podemos cargar unas recetas de prueba. Para ello necesitamos crear una base de datos llamada *recipesdb* con tres colecciones: *recipesdb*, *tags* y *adaptedrecipes*. Para cargar contenido dentro de las colecciones de *recipesdb* y *tags* se proporcionan dos ficheros: [recipes.csv](https://github.com/andreamorgar/TFM_MII/tree/master/data/recipes.csv) y [tags.csv](https://github.com/andreamorgar/TFM_MII/tree/master/data/tags.csv)



Para poner la API en funcionamiento:
~~~
$ cd files/database
$ python3 api_flask.py
~~~

Para levantar la aplicación, nos situamos en el directorio de la aplicación e iniciamos la ejecución.
~~~
$ cd app
$ ionic serve
~~~

### Anotaciones

Con los pasos anteriores, la aplicación estaría en marcha, pero no podría obtener adaptaciones de recetas. Esto se debe a que la base de datos de composición nutricional utilizada no es pública y tiene licencia copyright. Para subsanar este inconveniente, se adjunta un [vídeo](https://github.com/andreamorgar/TFM_MII/tree/master/videos) con una demostración de la ejecución de la aplicación móvil.

No obstante en el directorio [data](https://github.com/andreamorgar/TFM_MII/tree/master/data), se proporcionan los archivos (vacíos) con la estructura requerida por el código para funcionar correctamente. Una vez rellenados, el sistema de adaptación funcionará con normalidad.


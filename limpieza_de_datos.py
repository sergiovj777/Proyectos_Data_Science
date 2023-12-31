# -*- coding: utf-8 -*-
"""limpieza_de_datos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xzg2bZg7Cti4JTrHjMC1t5zYeYckfGGX
"""

from IPython.display import Image
Image(filename='imagen.png')



"""## Importar librerías"""

#Procesamiento
import pandas as pd
import numpy as np
import datetime as dt
import missingno as msno
 
#Visualización
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

"""## Cargar datos


"""

android_games = pd.read_csv('android-games.csv')

"""### Visualizar datos del dataframe


Primeras 5 líneas:
"""

android_games.head()

"""Últimas 5 líneas:"""

android_games.tail()

"""Muestra aleatoria:"""

android_games.sample(4)

"""Tamaño del dataframe:"""

android_games.shape

"""## Análisis exploratorio de datos

### General
"""

android_games.info()

"""- Podemos observar valores nulos en las variables *paid* y *average rating*.
- El tipo de dato de la fecha es *Object* así como el de la variable *installs*.
"""

android_games.describe().T

"""- En las variables *growth (30 days)* y *growth (60 days)* se observa el valor máximo en una escala superior a los demás valores.

### Visualizaciones

Distribución del promedio de calificaciones:
"""

#Matplotlib
plt.hist(android_games['average rating']);

"""- La mayoría de los juegos que entran en el top 100 por categoría reciben una calificación promedio de 4 estrellas.

Cantidad de videojuegos pagos y gratis:
"""

#Seaborn
sns.countplot(x='paid',data=android_games);

plot = (100 * android_games['paid'].value_counts() / len(android_games['paid'])).plot(
kind='bar', title='% de videojuegos gratis y pagos')

"""- Más del 90% de los videojuegos que están dentro del top 100 son gratis."""

# Plotly
fig = go.Figure()
fig.add_trace(go.Box(y=android_games['growth (30 days)']))
fig.add_trace(go.Box(y=android_games['growth (60 days)']))

fig.show()

"""### Descriptivas

Descripción de variables categóricas:
"""

android_games.describe(include='O')

"""- Para la fecha podemos observar 121 datos únicos, pero si cada puesto se registró en un día del año este valor debería ser 100.
- El videojuego que aparece más veces en el top es Solitaire.
- La variable *installs* es categórica.

Valores únicos de las Categorías:
"""

android_games['category'].unique()

"""- Observamos las siguientes categorías: 
  - *game action*
  - *game card*
  - *FICTION BOOK*
  - *BIOGRAPHY BOOK*

Valores únicos de Fecha:
"""

android_games['Date'].unique()

"""- Observamos dos formatos para la columna *Date*

Valores únicos de la columna *installs*
"""

android_games['installs'].unique()

"""- Los valores contienen letras que indican:

  *   M: *1000000
  *   k: *1000

## Insights
- Valores nulos en las variables *paid* y *average rating*.
- Tipo de dato de la fecha es *Object*. 
- Fecha con formatos distintos.
- Variable *installs* es categórica.
- Variables *growth (30 days)* y *growth (60 days)* con datos atípicos.
"""

from IPython.display import Image
Image(filename='level-up.png', width=300, height=300,)

"""## Limpieza de datos

### Valores nulos

Validemos cuántos datos nulos existen:
"""

#Valores nulos por columna
missing_values_count  = android_games.isna().sum()
missing_values_count

# Porcentaje de datos nulos
total_cells = np.product(android_games.shape)
total_missing = missing_values_count.sum()

(total_missing/total_cells) * 100

#Visualizar cantidad de datos por columna
msno.bar(android_games);

"""- En la gráfica anterior no se logra observar cuáles columnas tienen datos nulos."""

msno.matrix(android_games);

"""Podemos eliminar estos valores porque representan el 5% del total de los datos:



"""

# android_games.dropna()

"""**Advertencia!**

Esta opción no debe ser la primera a considerar. Podemos mirar cuáles son esos valores nulos y qué caracteristicas tienen las columnas y los datos:
"""

android_games[android_games.isna().any(1)]

"""Vemos que falta muy poca información y esta podemos completarla para no perder los datos:

- Para la columna *average rating* podemos llenar los valores con 4, ya que como vimos en el análisis de datos la mayoría de los videojuegos en el top 100 tienen ese puntaje.

- Para la columna *paid* podemos hacer una validación ya que tenemos el precio:
  - Si el precio es 0, paid=False
  - Si el precio es >0, paid=True

Reemplacemos los valores Nan de *average rating* por 4:
"""

values = {"average rating": 4}
android_games.fillna(value=values, inplace=True)

"""Validemos los valores de la columna paid con los valores en la columna precio:"""

for i in range(len(android_games['price'])):
  if android_games['price'][i] != 0:
    android_games['paid'][i]=True
  else:
    android_games['paid'][i]=False

android_games[android_games['price']>0]

android_games.isna().sum()

"""**Misión completada!**

Tenemos el dataset sin valores nulos.

### Datos duplicados

Verificar si existen datos duplicados:
"""

android_games[android_games.duplicated()]

android_games[android_games.duplicated(subset=['Date',	'rank',	'title',	'total ratings', 'category'], keep = False)]

"""- Podemos observar que la diferencia entre los datos duplicados se encuentra en las variables: 
  - 5 star ratings	
  - 4 star ratings	
  - 3 star ratings	
  - 2 star ratings	
  - 1 star ratings

Para eliminarlos y quedar con uno de los datos podemos tomar el promedio de las variables mencionadas.
"""

#android_games.drop_duplicates(subset=['Date',	'rank',	'title',	'total ratings', 'category'], inplace = True)

top_games = android_games.groupby(['Date','rank','title','total ratings','installs','average rating',
                                   'growth (30 days)','growth (60 days)','price','category','paid'])['5 star ratings','4 star ratings',
                                   '3 star ratings','2 star ratings','1 star ratings'].mean()
top_games.reset_index(inplace=True)

top_games[top_games.duplicated(subset=['Date',	'rank',	'title',	'total ratings', 'category'], keep = False)]

top_games.sample(5)

"""**Misión completada!**

Creamos un nuevo dataframe para eliminar los datos duplicados y obtener el valor promedio de esos datos.

### Uniformidad de datos categóricos

En las categorías vemos algunas repetidas que aparacen como únicas porque están escritas en mayúscula y otras en minúscula. Para que exista uniformidad entre los datos cambiaremos todo a mayúsculas:
"""

top_games['category'] = top_games['category'].str.upper()

top_games['category'].unique()

"""**Pausa!** 

Podemos observar categorías que no corresponden a videojuegos, esas categorías corresponden a libros. 

En este caso podemos eliminarlos.
"""

top_games = top_games[~top_games['category'].isin(['FICTION BOOK', 'BIOGRAPHY BOOK'])]

top_games['category'].unique()

"""**Misión completada!**

Tenemos la columna de categorías limpia.

### Tipo de datos

La columna de precio es de tipo object, esta columna nos será más útil si lo pasamos a tipo int o float para futuros calculos y gráficas:
"""

def installs(x):
    if x[-1] == 'M':
        return(float(x[:-2])*1000000)
    else:
        return(float(x[:-2])*1000)

top_games['installs'] = top_games['installs'].apply(installs)

display(top_games['installs'].unique())
display(top_games['installs'].dtype)

top_games['installs'].astype('int')

"""**Misión completada!**

Tenemos la columna de instalaciones con tipo de dato *int*.

### Reemplazar valores de variables

Vamos a cambiar los valores de la columna que indica si el videojuegos es pago o gratis:

*   Pago (True) = 1
*   Gratis (False) = 0
"""

top_games['paid'].unique()

top_games['paid'] = top_games['paid'].replace({True:1, False:0})

top_games['paid'].unique()

"""**Misión completada!**

La columna paid tiene valores de 0 y 1.

### Formato de fechas

Validar el formato de la fecha y convertirlo a datetime:
"""

top_games['Date'].unique()

#Unificar formato
top_games['Date'] = pd.to_datetime(top_games['Date']).dt.strftime('%m/%d/%Y')

#Validar
display(top_games['Date'].unique())
display(top_games['Date'].nunique())

"""**Misión completada!**

Ahora tenemos la fecha en el mismo formato.

**Para finalizar** guardamos el dataframe para su posterior uso:
"""

top_games.to_csv("android_games_limpio.csv")

"""## **Ta dá!**

Tienes tu dataset limpio y listo para visualizaciones e implementación de modelos.

**Nivel Avanzado**

Si te interesa la limpieza de datos y quieres profundizar te recomiendo que busques:
- Expresiones regulares
- Librerías fuzzywuzzy y recordlinkage
"""

from IPython.display import Image
Image(filename='imagen_end.png')
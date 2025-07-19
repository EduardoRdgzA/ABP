import matplotlib.pyplot as plt
import numpy as np 
from functools import reduce

# Datos ejemlo 
categorias = ["O&P","C&P", "A&H", "R&M","C&M"]
N = len(categorias)  # Número de variables


data_bf1 = {
    "investigacion": [1, 2, 4, 5, 5],
    "producto" : [4, 3, 5, 3, 2],
    "presentacion" : [3, 2, 3, 3, 4]
}

data_bf2 = {
    "investigacion": [3, 3, 4, 5, 5],
    "producto" : [4, 3, 5, 5, 5],
    "presentacion" : [3, 2, 3, 3, 5]
}

data_bf3 = {
    "investigacion": [5, 4, 4, 5, 5],
    "producto" : [4, 5, 5, 5, 4],
    "presentacion" : [5, 5, 5, 5, 4]
}

# Calcular los ángulos para cada eje
# angulos_grados = [n/float(N) * 360 for n in range(N)]
angulos_raw = [n/float(N) * 2 * np.pi for n in range(N)]
# Agregar el primer valor al final de la lista para cerrar el pentágono
angulos = angulos_raw + angulos_raw[:1] # 6 elementos

def loop_data(data:dict) -> dict:
    """
    Añade el primer valor de cada lista de datos al final de la misma para cerrar el polígono en una gráfica radar.

    Esta función toma un diccionario donde cada clave corresponde a una categoría y su valor es una lista de números (valores para cada vértice del radar). Para cada lista, agrega su primer elemento al final, permitiendo que la gráfica radar se cierre correctamente formando un polígono.

    Args:
        data (dict): Diccionario con los datos de cada categoría. Cada valor debe ser una lista de números.

    Returns:
        dict: El mismo diccionario de entrada, pero con el primer valor de cada lista añadido al final.
    """
    data_copy = {}
    for key in data:
        data_copy[key] = data[key] + data[key][:1]
    return data_copy

def list_comprehension(datos:dict) -> list:
    lista = [datos[key] for key in datos]
    return lista

def generar_vectores_por_categoria(datos:dict, angulos:list) -> dict:
    """
    Genera los vectores (radio, ángulo) para cada categoría a partir de los datos y los ángulos dados.

    Esta función toma un diccionario de datos donde cada clave es una categoría y su valor es una lista de números (radios para cada vértice del radar), junto con una lista de ángulos. Devuelve un nuevo diccionario donde cada categoría está asociada a una lista de tuplas (radio, ángulo), facilitando la conversión a coordenadas polares para graficar.

    Args:
        datos (dict): Diccionario con los datos de cada categoría. Cada valor debe ser una lista de números (radios).
        angulos (list): Lista de ángulos (en radianes) correspondientes a cada vértice del radar.

    Returns:
        dict: Diccionario donde cada clave es una categoría y su valor es una lista de tuplas (radio, ángulo).
    """
    valores_por_categoria = list_comprehension(datos) # Extrae las listas de valores por categoría

    # Combina cada valor con su ángulo correspondiente
    vectores_por_categoria = []
    for valores in valores_por_categoria:
        vector = list(zip(valores, angulos))
        vectores_por_categoria.append(vector)

    # Asigna cada vector a su categoría correspondiente
    nuevos_datos = {}
    for indice, categoria in enumerate(datos):
        nuevos_datos[categoria] = vectores_por_categoria[indice]

    return nuevos_datos

def vector_resultante_por_categoria(datos:dict) -> dict:
    """
    Calcula el vector resultante en coordenadas cartesianas para cada categoría a partir de sus vectores polares.

    Esta función toma un diccionario donde cada clave es una categoría y su valor es una lista de tuplas (radio, ángulo) que representan los vectores en coordenadas polares. Para cada categoría, convierte estos vectores a coordenadas cartesianas (x, y), suma todas las componentes y devuelve el vector resultante total para cada categoría.

    Args:
        datos (dict): Diccionario donde cada clave es una categoría y su valor es una lista de tuplas (radio, ángulo) en coordenadas polares.

    Returns:
        dict: Diccionario donde cada clave es una categoría y su valor es una tupla (x, y) que representa el vector resultante en coordenadas cartesianas.
    """
    vectores_resultantes_por_categoria = []
    for categoria in datos:
        lista_vectores_por_categoria = datos[categoria]
        abscisas = []
        ordenadas = []
        for radio, theta in lista_vectores_por_categoria:
            x = radio * np.cos(theta)
            y = radio * np.sin(theta)
            abscisas.append(x)
            ordenadas.append(y)

        total_abscisas = reduce(lambda a,b :a+b, abscisas)
        total_ordenadas = reduce(lambda a,b:a+b, ordenadas)

        vector_resultante = (total_abscisas, total_ordenadas)
        vectores_resultantes_por_categoria.append(vector_resultante)
    nuevos_datos = {}
    for indice, categoria in enumerate(datos):
        nuevos_datos[categoria] = vectores_resultantes_por_categoria[indice]
    return nuevos_datos

# Crear la figura
"""
Matriz del layout
bf1 bf2 bf3 : boleta-fase-#
cf1 cf2 cf3 : cohesion-fase-#
if1 if2 if3 : integración-fase-#
"""
fig, ((bf1,bf2,bf3),(cf1,cf2,cf3),(if1,if2,if3)) = plt.subplots(
    3,3,
    figsize=(8,8),
    subplot_kw=dict(projection='polar'),
)

def radar(subgrafica:str = None, datos:dict = None, vectores_resultantes_xy:dict = None, color:list = None, titulo:str= None
)-> None:
    """
    Dibuja una gráfica radar (o de telaraña) con varias categorías y añade los vectores resultantes para cada una.

    Esta función grafica los datos de varias categorías en una gráfica radar, rellenando cada área con un color distinto y añadiendo flechas que representan los vectores resultantes en coordenadas polares. Permite personalizar los colores y la estilización de la gráfica.

    Args:
        subgrafica (matplotlib.axes._subplots.PolarAxesSubplot): Subgráfica polar donde se dibujará el radar, de acuerdo al layout de la figura.
        datos (dict): Diccionario con los datos de cada categoría. Cada valor debe ser una lista de números (radios para cada vértice del radar, ya con el primer valor repetido al final para cerrar el polígono).
        vectores_resultantes_xy (dict): Diccionario con los vectores resultantes por categoría. Cada valor debe ser una tupla (x, y) en coordenadas cartesianas.
        color (list): Lista de colores para cada categoría.

    Returns:
        None: Esta función solo dibuja sobre la subgráfica proporcionada.
    """
    vectores_por_categoria =list_comprehension(vectores_resultantes_xy)

    for indice, categoria in enumerate(datos):
        subgrafica.plot(angulos, datos[categoria], color=color[indice])
        subgrafica.fill(angulos, datos[categoria], color=color[indice], alpha=0.1)

        # Añadir los vectores resultantes a la gráfica
        # Convertir los vectores cartesianas a polares y graficar flechas
        for i, vec in enumerate(vectores_por_categoria):
            x, y = vec
            radio = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            subgrafica.annotate(
                '',
                xy=(theta, radio),
                xytext=(0, 0),
                arrowprops=dict(facecolor=color[i], edgecolor=color[i], shrink=0, width=1, headwidth=6, alpha=0.7)
            )

    # Estilización de las gráficas    
    subgrafica.set_xticks(angulos) # vértices marcados
    subgrafica.set_theta_direction(-1) # dirección horaria del ángulo 
    subgrafica.set_xticklabels(categorias + ["O&P"] ,fontsize=8) # Etiquetas de los vértices
    subgrafica.set_theta_offset(np.pi/2) # rotación de la gráfica a 90 grados
    subgrafica.set_yticks([1, 2, 3, 4, 5]) # etiquetas del eje radial
    subgrafica.spines['polar'].set_visible(False) # eliminar el eje polar
    subgrafica.set_ylim(0, 6) 
    subgrafica.set_title(titulo)

def vectores_cohesion(datos:dict) -> dict:
    """
    Calcula la cohesión entre las diferentes categorías tomando el valor mínimo de cada vértice.
    
    Esta función toma un diccionario donde cada clave es una categoría y su valor es una lista de números. 
    Calcula el valor mínimo para cada posición (vértice) entre todas las categorías.
    
    Args:
        datos (dict): Diccionario con las categorías y sus valores.
        
    Returns:
        dict: Diccionario con una sola clave "cohesion" y una lista con los valores mínimos por vértice.
    """
    dat = list_comprehension(datos)
    vertices = list(zip(*dat))  # Convertir a lista para poder iterar múltiples veces
    minimos = [min(u) for u in vertices]
    cohesion = {
        'cohesion': minimos,
    }
    return cohesion

def vectores_integracion(datos:dict) -> dict:
    """
    Calcula la integracion entre las diferentes categorías tomando el valor máximo de cada vértice.
    
    Esta función toma un diccionario donde cada clave es una categoría y su valor es una lista de números. 
    Calcula el valor máximo para cada posición (vértice) entre todas las categorías.
    
    Args:
        datos (dict): Diccionario con las categorías y sus valores.
        
    Returns:
        dict: Diccionario con una sola clave "integración" y una lista con los valores máximos por vértice.
    """
    dat = list_comprehension(datos)
    vertices = list(zip(*dat))  # Convertir a lista para poder iterar múltiples veces
    maximos = [max(u) for u in vertices]
    integracion = {
        'integracions': maximos,
    }
    return integracion



def graficar_radar(subgrafica:str ,data:dict, color:list,titulo:str) -> None:
    data_loop = loop_data(data)
    datos_vectores = generar_vectores_por_categoria(data, angulos_raw)
    vectores_resultantes = vector_resultante_por_categoria(datos_vectores)
    radar(subgrafica, datos= data_loop, vectores_resultantes_xy=vectores_resultantes, color= color,titulo=titulo)


# Gráficar
color= ['#38761d', '#bf9133', "#351e75"]
graficar_radar(bf1,data_bf1,color,"Fase 1")
graficar_radar(bf2,data_bf2,color,"Fase 2")
graficar_radar(bf3,data_bf3,color,"Fase 3")

cohesion_cf1 = vectores_cohesion(data_bf1)
cohesion_cf2 = vectores_cohesion(data_bf2)
cohesion_cf3 = vectores_cohesion(data_bf3)
graficar_radar(cf1,cohesion_cf1,["#bf2525"],"Cohesion 1")
graficar_radar(cf2,cohesion_cf2,["#bf2525"],"Coheison 2")
graficar_radar(cf3,cohesion_cf3,["#bf2525"],"Cohesion 3")

integracion_if1 = vectores_integracion(data_bf1)
integracion_if2 = vectores_integracion(data_bf2)
integracion_if3 = vectores_integracion(data_bf3)
graficar_radar(if1,integracion_if1,["#bf2525"],"Integración 1")
graficar_radar(if2,integracion_if2,["#bf2525"],"Integración 2")
graficar_radar(if3,integracion_if3,["#bf2525"],"Integración 3")


fig.suptitle(
    "Innovarte\nDesarrollo Anual del Proyecto",
    fontsize=20,
    fontname='Arial',
    fontweight='bold'
)
fig.text(
    0.5, 0.00, 
    "Fuente: Datos obtenidos a través de las evaluaciones medidas con rúbricas. 2024-2025.",
    ha='center', 
    fontsize=10,
    fontname='Arial'
)
plt.tight_layout()
plt.show()


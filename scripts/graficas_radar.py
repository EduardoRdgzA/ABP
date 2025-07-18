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
    """Funcion que añade el primer varo al final para cerrar el pentágono

    Args:
        data (dict): data del pentágono

    Returns:
        dict: data con el valor final añadido
    """
    for key in data:
        data[key] += data[key][:1]
    return data

def list_comprehension(datos:dict) -> list:
    lista = [datos[key] for key in datos]
    return lista


def generar_vectores_por_categoria(datos:dict, angulos:list) -> dict:
    # Extrae las listas de valores por categoría
    valores_por_categoria = list_comprehension(datos)

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

datos_vectores_bf1 = generar_vectores_por_categoria(data_bf1, angulos_raw)
datos_vectores_bf2 = generar_vectores_por_categoria(data_bf2, angulos_raw)
datos_vectores_bf3 = generar_vectores_por_categoria(data_bf3, angulos_raw)

vec = list_comprehension(datos_vectores_bf1)

def vector_resultante_por_categoria(datos:dict) -> dict:
    """Extrae un diccionario con los vectores resultantes en coordenadas cartesianas

    Args:
        datos (dict): datos de las categorias con los valores

    Returns:
        dict: Devuelve un diccionario con los vectores resultantes en coordenadas polares 
    """
    # Extre la lista de  vectores por categoria
    vectores_resultantes_por_categoria = []
    for categoria in datos:
        lista_vectores_por_categoria = datos[categoria]
        # Extre las coordenadas de cada vector por categoria
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
    # Asigna cada vector a su categoría correspondiente
    nuevos_datos = {}
    for indice, categoria in enumerate(datos):
        nuevos_datos[categoria] = vectores_resultantes_por_categoria[indice]
    return nuevos_datos

vectores_resultantes_bf1 = vector_resultante_por_categoria(datos_vectores_bf1)
vectores_resultantes_bf2 = vector_resultante_por_categoria(datos_vectores_bf2)
vectores_resultantes_bf3 = vector_resultante_por_categoria(datos_vectores_bf3)
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

def radar(
        grafica:str = None, 
        datos:dict = None, 
        vectores_resultantes:dict = None, 
        color:list = None, 
        estilizar:bool = True
)-> None:
    """Funcion que gráfica un radar con tres telarañas

    Args:
        grafica (str): Nombre de la gráfica de acuerdo al layout
        datos (dict): Datos a por radar. En orden: Investigacion, Producto y Presentación
        vectores_resultantes(dict): Vectores resultantes por radar (Tambien son 3)
        color (list): Colores de la las telarañas
    """
    vectores_por_categoria =list_comprehension(vectores_resultantes)

    for indice, categoria in enumerate(datos):
        grafica.plot(angulos, datos[categoria], color=color[indice])
        grafica.fill(angulos, datos[categoria], color=color[indice], alpha=0.1)

        # Añadir los vectores resultantes a la gráfica
        # Convertir los vectores cartesianas a polares y graficar flechas
        for i, vec in enumerate(vectores_por_categoria):
            x, y = vec
            radio = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            grafica.annotate(
                '',
                xy=(theta, radio),
                xytext=(0, 0),
                arrowprops=dict(facecolor=color[i], edgecolor=color[i], shrink=0, width=1, headwidth=6, alpha=0.7)
            )

    # Estilización de las gráficas    
    while estilizar:
        grafica.set_xticks(angulos) # vértices marcados
        grafica.set_theta_direction(-1) # dirección horaria del ángulo 
        grafica.set_xticklabels(["O&P","C&P", "A&H", "R&M","C&M","O&P"]) # Etiquetas de los vértices
        grafica.set_theta_offset(np.pi/2) # rotación de la gráfica a 90 grados
        grafica.set_yticks([1, 2, 3, 4, 5]) # etiquetas del eje radial
        grafica.spines['polar'].set_visible(False) # eliminar el eje polar
        grafica.set_ylim(0, 6) 
        break



# Gráficar
color= ['#38761d', '#bf9133', "#351e75"]

estilizar = True

data_bf1 = loop_data(data_bf1)
radar(bf1, datos= data_bf1, vectores_resultantes=vectores_resultantes_bf1, color= color, estilizar=estilizar)
print("")

data_bf2 = loop_data(data_bf2)
radar(bf2, datos= data_bf2, vectores_resultantes=vectores_resultantes_bf2, color= color, estilizar=estilizar)
print("")

data_bf3 = loop_data(data_bf3)
radar(bf3, datos= data_bf3, vectores_resultantes=vectores_resultantes_bf3,color= color, estilizar=estilizar)
print("")

plt.tight_layout()
plt.show()


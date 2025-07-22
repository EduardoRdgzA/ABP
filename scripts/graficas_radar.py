import matplotlib.pyplot as plt
import numpy as np 
from functools import reduce
import pandas as pd
from rich import print

#########################     EXTRACIÓN DE DATOS     #########################


def data2list(path:str = "") -> list:
    """
    Lee un archivo CSV y organiza los datos de equipos por grupo y fase.

    Esta función carga un archivo CSV con datos de equipos, filtra los registros con correo, y extrae los valores de cada fase (investigación, producto, presentación) para cada equipo.
    Devuelve una lista de diccionarios, donde cada diccionario representa un equipo y contiene los datos organizados por fase y categoría.

    Args:
        path (str): Ruta al archivo CSV que contiene los datos.

    Returns:
        list: Lista de diccionarios, cada uno con la estructura de datos por equipo y fase.
    """
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    df_lideres_equipo = df.dropna(subset=['Correo'])
    df_todas_las_categorias = df_lideres_equipo.iloc[:, 3:]         
    lista_de_filas = df_todas_las_categorias.values.tolist()

    equipos_por_grupo = []
    for supervector in lista_de_filas:
        id_abp = supervector[:1][0]
        fase1 = supervector[1:15+1]
        fase2 = supervector[16:30+1]
        fase3 = supervector[31:]
            
        
        data_equipo = {
            'id':id_abp,
            'fase 1':{
                'investigación' : fase1[:4+1],
                'producto' : fase1[5:9+1],
                'presentación': fase1[10:14+1]
            },
            'fase 2':{
                'investigación' : fase2[:4+1],
                'producto' : fase2[5:9+1],
                'presentación': fase2[10:14+1]
            },
            'fase 3':{
                'investigación' : fase3[:4+1],
                'producto' : fase3[5:9+1],
                'presentación': fase3[10:14+1]
            }
        }
        
        equipos_por_grupo.append(data_equipo)

    return equipos_por_grupo
    

#########################    PROCESO DE GRAFICAR     #########################
# Categorias
categorias = ["O&P","C&P", "A&H", "R&M","C&M"]
N = len(categorias)  # Número de variables

####    Ejemplo de datos     ####
data_bf1_Test = {
    "investigacion": [1, 2, 4, 5, 5],
    "producto" : [4, 3, 5, 3, 2],
    "presentacion" : [3, 2, 3, 3, 4]
}

data_bf2_Test = {
    "investigacion": [3, 3, 4, 5, 5],
    "producto" : [4, 3, 5, 5, 5],
    "presentacion" : [3, 2, 3, 3, 5]
}

data_bf3_Test = {
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

def vectores_por_categoria_radianes(datos:dict, angulos:list) -> dict:
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

def vector_resultante_por_categoria_xy(datos:dict) -> dict:
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
        'cohesión': minimos,
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
        'integración': maximos,
    }
    return integracion

def area_por_categoria(data:dict) -> dict:
    """
    Calcula el área normalizada de los polígonos para cada categoría en una gráfica radar.

    Esta función toma un diccionario donde cada clave es una categoría y su valor es una lista de tuplas (radio, ángulo) que representan los vértices del polígono en coordenadas polares. Calcula el área de cada polígono usando la fórmula para polígonos regulares y la normaliza respecto al área máxima posible, devolviendo un valor entre 0 y 5 para cada categoría.

    Args:
        data (dict): Diccionario con los datos de cada categoría. Cada valor debe ser una lista de tuplas (radio, ángulo) para los vértices del polígono.

    Returns:
        dict: Diccionario donde cada clave es una categoría y su valor es el área normalizada del polígono correspondiente.
    """
    categorias = list_comprehension(data)
    
    area_maxima = 0.5 * np.sin(np.deg2rad(72)) *5 * 25
    areas_poligonos_por_categorias = []
    for vectores_i in categorias:
        vectores_imas1 = []
        vectores_imas1 = vectores_i[1:] + vectores_i[:1]

        radios_i = np.array( [componente[0] for componente in vectores_i] )
        radios_imas1 = np.array( [componente[0] for componente in vectores_imas1] )

        sumaproducto_radios =  np.sum(radios_i * radios_imas1)
        area_poligono = 0.5 * np.sin(np.deg2rad(72)) * sumaproducto_radios

        areas_poligonos_por_categorias.append( (area_poligono / area_maxima) * 5)
    
    nuevos_datos = {}
    for indice, categoria in enumerate(data):
        nuevos_datos[categoria] = areas_poligonos_por_categorias[indice]

    return nuevos_datos

def radar(subgrafica:str = None, datos:dict = None, vectores_resultantes_xy:dict = None, color:list = None, title_props:dict = None, leyend_props:dict = None,label:list = None
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
        subgrafica.fill(angulos, datos[categoria], color=color[indice], alpha=0.1,label=label[indice])

        # Añadir los vectores resultantes a la gráfica
        # Convertir los vectores cartesianas a polares y graficar flechas
        for i, vec in enumerate(vectores_por_categoria):
            x, y = vec
            radio = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x)
            subgrafica.annotate(
                '',
                xy=(theta, radio), # Orden del vector necesairio para matplotlib en gráficas polares
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
    subgrafica.set_title(**title_props)
    subgrafica.legend(**leyend_props)

def graficar_radar(subgrafica:str=None ,data:dict=None, color:list=[], title_props:dict=None, leyend_props:dict=None, semaforo:bool=False) -> None:
    data_loop = loop_data(data)
    datos_vectores = vectores_por_categoria_radianes(data, angulos_raw)
    vectores_resultantes = vector_resultante_por_categoria_xy(datos_vectores)
    areas_por_categoria = area_por_categoria(datos_vectores)
    area = list_comprehension(areas_por_categoria)    
    label= [f"Éxito: {item:.1f}" for item in area]
    label_float = [item for item in area]
    color_semaforo = color
    while semaforo:
        color_semaforo.clear()
        for valor in label_float:
            if valor < 3.0000:
                color_semaforo.append("#C0392B") # Rojo
            elif 3.0000 <= valor <= 3.4999:
                color_semaforo.append("#E67E22") # Naranja
            elif 3.5000 <= valor <= 3.9999:
                color_semaforo.append("#F1C40F") # Amarillo
            elif 4.000 <= valor <= 4.4999:
                color_semaforo.append("#27AE60") # Verde
            else:
                color_semaforo.append("#2980B9") # Azul (all blue)
        break

    radar(
        subgrafica, 
        datos= data_loop, 
        vectores_resultantes_xy=vectores_resultantes, 
        color= color_semaforo,
        title_props=title_props, 
        leyend_props=leyend_props,
        label=label
    )

def imprimir(save:str,id_equipo:str,data_bf1:dict, data_bf2:dict ,data_bf3:dict)-> None:
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
    # Gráficar
    color= ['#38761d', '#bf9133', "#351e75"]

    #########################     BOLETA     #########################
    leyend_props_b = dict(
        title_fontsize=8,
        loc='upper left',
        fontsize=6,
    )
    leyend_props_bf1 = dict(leyend_props_b)
    leyend_props_bf2 = dict(leyend_props_b)
    leyend_props_bf3 = dict(leyend_props_b)
    leyend_props_bf1.update(title="Boleta 1")
    leyend_props_bf2.update(title="Boleta 2")
    leyend_props_bf3.update(title="Boleta 3")
    graficar_radar(bf1, data_bf1, color, dict(label='Fase 1:\nPregunta Detonadora',fontweight='bold'),leyend_props_bf1)
    graficar_radar(bf2, data_bf2, color, dict(label='Fase 2:\nConstruir Conocimientos',fontweight='bold'), leyend_props_bf2)
    graficar_radar(bf3, data_bf3, color, dict(label='Fase 3:\nProducto',fontweight='bold'), leyend_props_bf3)

    #########################     COHESIÓN     #########################
    cohesion_cf1 = vectores_cohesion(data_bf1)
    cohesion_cf2 = vectores_cohesion(data_bf2)
    cohesion_cf3 = vectores_cohesion(data_bf3)
    leyend_props_c = dict(
        title_fontsize=8,
        loc='upper left',
        fontsize=7,
    )
    leyend_props_cf1 = dict(leyend_props_c)
    leyend_props_cf2 = dict(leyend_props_c)
    leyend_props_cf3 = dict(leyend_props_c)
    leyend_props_cf1.update(title="Cohesión 1")
    leyend_props_cf2.update(title="Cohesión 2")
    leyend_props_cf3.update(title="Cohesión 3")
    graficar_radar(cf1,cohesion_cf1,["#bf2525"],dict(label=''), leyend_props_cf1, semaforo=True)
    graficar_radar(cf2,cohesion_cf2,["#bf2525"],dict(label=''), leyend_props_cf2, semaforo=True)
    graficar_radar(cf3,cohesion_cf3,["#bf2525"],dict(label=''), leyend_props_cf3, semaforo=True)

    #########################     INTEGRACIÓN     #########################
    leyend_props_i = dict(
        title_fontsize=8,
        loc='upper left',
        fontsize=7,
    )
    leyend_props_if1 = dict(leyend_props_i)
    leyend_props_if2 = dict(leyend_props_i)
    leyend_props_if3 = dict(leyend_props_i)
    leyend_props_if1.update(title="Integración 1")
    leyend_props_if2.update(title="Integración 2")
    leyend_props_if3.update(title="Integración 3")
    integracion_if1 = vectores_integracion(data_bf1)
    integracion_if2 = vectores_integracion(data_bf2)
    integracion_if3 = vectores_integracion(data_bf3)
    graficar_radar(if1,integracion_if1,["#bf2525"],dict(label=''), leyend_props_if1,semaforo=True)
    graficar_radar(if2,integracion_if2,["#bf2525"],dict(label=''), leyend_props_if2,semaforo=True)
    graficar_radar(if3,integracion_if3,["#bf2525"],dict(label=''), leyend_props_if3,semaforo=True)


    fig.suptitle(
        f"Innovarte: Desarrollo Anual del Proyecto\nEquipo: {id_equipo}",
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
    #plt.show()
    plt.savefig(save)
    plt.close(fig)

def generar_radares(data_list:list=None)-> None:
    for equipo in data_list:
        id_equipo = equipo['id']
        data_bf1 = equipo['fase 1']
        data_bf2 = equipo['fase 2']
        data_bf3 = equipo['fase 3']
        imprimir(
            save=f"/Users/eduardo/Documents/ABP/scripts/data/{id_equipo}.png",
            id_equipo=id_equipo,
            data_bf1=data_bf1,
            data_bf2=data_bf2,
            data_bf3=data_bf3,
        )
        print(f"Radar del equipo {id_equipo} generado")


if __name__ == '__main__':
    from pathlib import Path
    carpeta = Path("/Users/eduardo/Documents/ABP/scripts/data")
    for f in carpeta.glob("*.csv"):
        print(f)
        data = data2list(f)
        generar_radares(data)
    
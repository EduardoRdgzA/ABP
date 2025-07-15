import matplotlib.pyplot as plt
import numpy as np 

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

print(data_bf1)
print(angulos_raw)

def vectores(data_dict:dict, angulos_raw:list):
    datos_categorias = [ data_dict[key] for key in data_dict ]
    vectores = []
    for data_categoria in datos_categorias:
        vector = list(zip(data_categoria, angulos_raw))
        vectores.append(vector)
    count = 0
    for categoria in data_dict:
        data_dict[categoria] = vectores[count]
        count += 1
    print(data_dict)
vectores(data_bf1, angulos_raw)


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

def radar(grafica:str, data:dict, color:list)-> None:
    """Funcion que gráfica un radar con tres telarañas

    Args:
        grafica (str): Nombre de la gráfica de acuerdo al layout
        data (dict): Datos a graficar
        color (list): Colores de la las telarañas
    """
    count = 0
    for key in data:
        grafica.plot(angulos, data[key],color=color[count])
        grafica.fill(angulos, data[key], color=color[count], alpha=0.1)
        count += 1 

    grafica.set_xticks(angulos)
    grafica.set_theta_direction(-1)
    grafica.set_xticklabels(["O&P","C&P", "A&H", "R&M","C&M","O&P"])
    grafica.set_theta_offset(np.pi/2)
    grafica.set_yticks([1, 2, 3, 4, 5])
    grafica.spines['polar'].set_visible(False)

# Gráficar
color= ['#38761d', '#bf9133', "#351e75"]

data_bf1 = loop_data(data_bf1)
radar(bf1, data= data_bf1, color= color)

data_bf2 = loop_data(data_bf2)
radar(bf2, data= data_bf2, color= color)

data_bf3 = loop_data(data_bf3)
radar(bf3, data= data_bf3, color= color)

plt.tight_layout()
plt.show()


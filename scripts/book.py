from rich import print

import matplotlib.pyplot as plt

#################
from pydantic import BaseModel 
from typing import List, Dict, Any, Union
from pathlib import Path
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from functools import reduce

def printc(*context:Any,text:str=None,color:str="yellow") -> None:
    print(f"[{color}]# Start: '{text}'")
    print(*context)
    print(f"[{color}]### End: '{text}'")
    print("")

class AbstractUtilities(ABC):
    @abstractmethod
    def angles(self, angles_raw:bool) -> list:
        pass

class Utilities(AbstractUtilities):
    def angles(self, angles_raw:bool) -> list:
        angulos_crudos:list = [n/int(5) * 2 * np.pi for n in range(5)] # Poligono de 5 vértices: pentágono
        if angles_raw:
            return angulos_crudos
        
        else:
            angles_loop:list = angulos_crudos + angulos_crudos[:1] # Completar el pentágono en la gráfica polar
            return angles_loop


class AbstractLoadData(ABC):
    @abstractmethod
    def csv2list(self) -> list:
        pass
class LoadData(AbstractLoadData, BaseModel):
    path_data: Path
    category_labels : List[str]

    def csv2list(self) -> list:
        try:
            data_raw = pd.read_csv(self.path_data)
            data_frame = pd.DataFrame(data_raw)
            df_dropna = data_frame.dropna(subset=['Correo']) # print(df_dropna)
            df = df_dropna.iloc[:, 3:]   
            equipos:list = df.values.tolist()

            equipos_por_csv: List[dict]  = []

            id_min, id_max = (0,0)
            fase1_min, fase1_max  = (1, 15)
            fase2_min, fase2_max = (16, 30)
            fase3_min, fase3_max = (31, 45)

            investigacion_min, investigacion_max = (0, 4)
            producto_min, producto_max = (5, 9)
            presentacion_min, presentacion_max = (10, 14)

            for equipo in equipos:
                id_abp:str = equipo[ : id_max + 1][0]
                fase1:list = equipo[fase1_min : fase1_max + 1]
                fase2:list = equipo[fase2_min : fase2_max + 1]
                fase3:list = equipo[fase3_min : ]
                    
                equipo_data:dict = {
                    'id':id_abp,
                    'fase 1':{
                        self.category_labels[0] : fase1[ : investigacion_max + 1],
                        self.category_labels[1] : fase1[producto_min : producto_max + 1],
                        self.category_labels[2] : fase1[presentacion_min : presentacion_max + 1],
                    },
                    'fase 2':{
                        self.category_labels[0] : fase2[ : investigacion_max + 1],
                        self.category_labels[1] : fase2[producto_min : producto_max + 1],
                        self.category_labels[2] : fase2[presentacion_min : presentacion_max + 1],
                    },
                    'fase 3':{
                        self.category_labels[0] : fase3[ : investigacion_max + 1],
                        self.category_labels[1] : fase3[producto_min : producto_max + 1],
                        self.category_labels[2] : fase3[presentacion_min : presentacion_max + 1],
                    }
                }
                equipos_por_csv.append(equipo_data)
            return equipos_por_csv
        
        except Exception as e:
            print("Error al cargar los datos:", e)

class AbstractGetVectors(ABC):
    @abstractmethod
    def vectors_rubric_radians(self) -> List[dict]:
        pass

    @abstractmethod
    def vectors_resultant_radians(self) -> List[dict]:
        pass

    @abstractmethod
    def vectors_cohesion_integration_radians(self, labels:List[str]) -> List[dict]:
        pass

class GetVectors(AbstractGetVectors, BaseModel):
    data: List[dict]
    utilities : AbstractUtilities

    model_config = {
        'arbitrary_types_allowed': True
    } #Esto permite que Pydantic acepte tipos personalizados (como tu clase abstracta) como campos del modelo, evitando el error y manteniendo la flexibilidad de tu diseño.

    def vectors_rubric_radians(self) -> List[dict]:
        angles_loop = self.utilities.angles(angles_raw=False)
        phases_labels : bool| list = True
        new_team_dict:list = []
        
        for team_dict in self.data:  # dict
            while phases_labels:
                phases_labels = list(team_dict.keys())
                break

            team_vectors:list = []
            for categories_for_team in team_dict.values(): # dict 
                if isinstance(categories_for_team, dict):
                    
                    # Bloque para obtener los vectores (radio, ángulo)
                    # Este bloque es el Kernel del la función
                    vectores_radians:list = []
                    for vector in categories_for_team.values():
                        vector_radian = list(zip(vector, angles_loop))
                        vectores_radians.append(vector_radian)
                    
                    # Bloque para reconstrir el diccionario de las categorias y sus vectores en radianes: "investigación", "producto", "presentación"
                    phases_vectors:dict = {}
                    for index, phase in enumerate(categories_for_team):
                        phases_vectors[phase] = vectores_radians[index]
                        team_vectors.append(phases_vectors)
                    
            # Bloque para reconstir el diccionario completo.
            category_vectors : dict = {}
            for index, categoria in enumerate(team_dict):
                category_vectors[phases_labels[0]] = team_dict[phases_labels[0]]
                category_vectors[categoria] = team_vectors[index]
            new_team_dict.append(category_vectors)

        return new_team_dict

    def vectors_resultant_radians(self) -> List[dict]:
        angles_loop = self.utilities.angles(angles_raw=False)
        phases_labels : bool| list = True
        new_team_dict:list = []
        
        for team_dict in self.data:  # dict
            while phases_labels:
                phases_labels = list(team_dict.keys())
                break
            
            team_vectors:list = []
            for categories_for_team in team_dict.values(): # dict 
                if isinstance(categories_for_team, dict):
                    
                    # Bloque para obtener los vectores resultantes (radio, ángulo)
                    # Este bloque es el Kernel del la función
                    resultant_vectors_radians:list = []
                    for rubric_vector_for_category in categories_for_team.values():
                        vectors_radians_for_category:list = list(zip(rubric_vector_for_category, angles_loop))
                        
                        # Bloque para obtener vectores en coordenadas cartesianas
                        abscissas:list = []
                        ordinates:list = []
                        for vector in vectors_radians_for_category: 
                            radius, angle = vector
                            x = radius * np.cos(angle)
                            y = radius * np.sin(angle)
                            abscissas.append(x)
                            ordinates.append(y)

                        # Bloque para obtener el vector resultante en coordenadas cartesianas
                        resultant_abscissas:float = reduce(lambda a,b : a+b, abscissas)
                        resultant_ordenadas:float = reduce(lambda a,b : a+b, ordinates)
                        resultant_cartesian:tuple = (resultant_abscissas, resultant_ordenadas)
                        
                        # Bloque para obtener el vector resultante en coordenadas polares
                        x, y = resultant_cartesian
                        radius = np.sqrt(x**2 + y**2)
                        theta = np.arctan2(y, x)
                        resultant_radian = (radius, theta)
                        resultant_vectors_radians.append(resultant_radian)

                    # Bloque para reconstrir el diccionario de las categorias y sus vectores en radianes: "investigación", "producto", "presentación"
                    phases_vectors:dict = {}
                    for index, phase in enumerate(categories_for_team):
                        phases_vectors[phase] = resultant_vectors_radians[index]
                        team_vectors.append(phases_vectors) ##### RECORRER SANGRIA
            
            # Bloque para reconstir el diccionario completo.
            category_vectors : dict = {}
            for index, categoria in enumerate(team_dict): ##### phases_labels[1:]
                category_vectors[phases_labels[0]] = team_dict[phases_labels[0]]
                category_vectors[categoria] = team_vectors[index]  
            new_team_dict.append(category_vectors)
            
        return new_team_dict

    def vectors_cohesion_integration_radians(self, labels:List[str]) -> List[dict]:
        phases_labels : bool| list = True
        new_team_dict:list = []
        
        for team_dict in self.data:  # dict
            while phases_labels:
                phases_labels = list(team_dict.keys())
                break

            team_vectors:list = []
            for categories_for_team in team_dict.values(): # dict 
                if isinstance(categories_for_team, dict):
                    
                    # Bloque para obtener los vectores (radio, ángulo)
                    # Este bloque es el Kernel del la función
                    vectors_for_category = list(categories_for_team.values())
                    vertices = list(zip(*vectors_for_category))
                    minimos = [min(u) for u in vertices]
                    maximos = [max(u) for u in vertices]
                    

                    # Bloque para reconstrir el diccionario de las categorias y sus vectores en radianes: "investigación", "producto", "presentación"
                    phases_vectors:dict = {}
                    for index, phase in enumerate(categories_for_team):
                        phases_vectors[phase] = categories_for_team[phase]
                        phases_vectors[labels[0]] = minimos
                        phases_vectors[labels[1]] = maximos #ESTE BLOQUE SE ALIMENTA DE:  'vectores_radians: list'
                        team_vectors.append(phases_vectors)
                    
                    
            # Bloque para reconstir el diccionario completo.
            category_vectors : dict = {}
            for index, categoria in enumerate(team_dict):
                category_vectors[phases_labels[0]] = team_dict[phases_labels[0]]
                category_vectors[categoria] = team_vectors[index]
            new_team_dict.append(category_vectors)


        return new_team_dict


class AbstractGraficar(ABC):
    @abstractmethod
    def funcion(self):
        pass

class AbstractOrquestador(ABC):
    @abstractmethod
    def funcion(self):
        pass


if __name__ == '__main__':
    file = Path("/Users/eduardo/Documents/ABP/scripts/data/1_morado.csv")
    # csv = [files.as_posix() for files in  carpeta.glob("*csv")]
    print(file)

    loaddata_props = dict(
        path_data=file,
        category_labels=["investigación","producto","presentación"],
    )

    data = LoadData(**loaddata_props)
    data_list = data.csv2list()

    getvector_props = dict(
        data=data_list,
        utilities = Utilities(),
    )
    get_vector = GetVectors(**getvector_props)
    vectors_cohesion_integration = get_vector.vectors_cohesion_integration_radians(labels=["cohesión","integración"])
    #printc(vectors_cohesion_integration,color="cyan")
    ##############################         VECTOR 2 ###############
    getvector_props_2 = dict(
        data=vectors_cohesion_integration,
        utilities = Utilities(),
    )
    get_vector_2 = GetVectors(**getvector_props_2)

    vectors_2 = get_vector_2.vectors_rubric_radians()
    #printc(vectors_2,text="vectors_rubric_radians", color="yellow")

    resultend_vectors_2 = get_vector_2.vectors_resultant_radians()
    printc(resultend_vectors_2, color="red")


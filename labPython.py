"""
Desafío 3: Sistema de Gestión de Tareas
Objetivo: Desarrollar un sistema para organizar y administrar tareas personales o de equipo.

Requisitos:
- Crear una clase base Tarea con atributos como descripción, fecha de vencimiento, estado (pendiente, en progreso, completada), etc.
- Definir al menos 2 clases derivadas para diferentes tipos de tareas (por ejemplo, TareaSimple, TareaRecurrente) con atributos y métodos específicos.
- Implementar operaciones CRUD para gestionar las tareas.
- Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
- Persistir los datos en archivo JSON.
"""
import json

class Tarea:
    def _init_(self, número_de_tarea, descripción, fecha_de_vencimiento, estado):
        self.__número_de_tarea = número_de_tarea.validar_num_tarea(número_de_tarea)
        self.__descripción = descripción
        self.__fecha_de_vencimiento = fecha_de_vencimiento
        self.__estado = self.estado_valido(estado)
    
    @property
    def número_de_tarea(self):
        return self.__número_de_tarea
    @property
    def descripción(self):
        return self.__descripción
    @property
    def fecha_de_vencimiento(self):
        return self.__fecha_de_vencimiento
    @property
    def estado(self):
        return self.__estado.uppercase()
    
    @número_de_tarea.setter
    def número_de_tarea(self, nuevo_num):
        self.__número_de_tarea = self.validar_num_tarea(nuevo_num)

    @estado.setter
    def estado(self, nuevo_estado):
        self.__estado = self.actualizar_estado(nuevo_estado)
    
    def validar_num_tarea(self, número_de_tarea):
        try:
            num_tarea = int(número_de_tarea)
            if num_tarea < 1:
                raise ValueError("El número de tarea debe ser mayor a 0")
            return num_tarea
        except ValueError:
            raise ValueError("El número de tarea debe ser un número entero")

    def estado_valido(self, estado):
        try:
            if estado not in ["PENDIENTE", "EN PROGRESO", "COMPLETADA"]:
                raise ValueError("Estado inválido")
            return estado
        except ValueError:
            raise ValueError("Estado inválido")
    

    def to_dict(self):
        return {
            "Número de tarea": self.número_de_tarea,
            "Descripción": self.descripción,
            "Fecha de vencimiento": self.fecha_de_vencimiento,
            "Estado": self.estado
        }

    def __str__(self):
        return f"Tarea {self.número_de_tarea}: {self.descripción}"
    
class TareaSimple(Tarea):
    def init_(self, número_de_tarea, descripción, fecha_de_vencimiento, estado, dificultad):
        super().__init__(número_de_tarea ,descripción, fecha_de_vencimiento, estado)
        self.__dificultad = dificultad.validar_dificultad()

    @property
    def dificultad(self):
        return self.__dificultad
        
    def to_dict(self):
        datos = super().to_dict()
        datos["Dificultad"] = self.dificultad
        return datos

    def __str__(self):
        return f"{super().__str__()} - Dificultad: {self.dificultad}"
       
    def validar_dificultad(self, dificultad):
        try:
            dificultad_num = int(dificultad)
            if dificultad_num < 1 or dificultad_num > 5:
                raise ValueError("Dificultad inválida, ingrese un número entre 1 y 5")
            return dificultad
        except ValueError:
            raise ValueError("Dificultad inválida")
       
class TareaRecurrente(Tarea):
    def init_(self, número_de_tarea, descripción, fecha_de_vencimiento, estado, frecuencia):
        super().__init__(número_de_tarea ,descripción, fecha_de_vencimiento, estado)
        self.__frecuencia = frecuencia.validar_frecuencia()

    @property
    def frecuencia(self):
        return self.__frecuencia

    def to_dict(self):
        datos = super().to_dict()
        datos["Frecuencia"] = self.frecuencia
        return datos

    def __str__(self): 
        return f"{super().__str__()} - Frecuencia: {self.frecuencia}"

    def validar_frecuencia(self, frecuencia):
        try:
            frecuencia_num = int(frecuencia)
            if frecuencia_num < 1 or frecuencia_num > 3:
                raise ValueError("Frecuencia inválida, ingrese un número entre 1 y 3")
            return frecuencia
        except ValueError:
            raise ValueError("Frecuencia inválida")
        
class GestionTareas:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as error:
            raise Exception(f'Error al leer datos del archivo: {error}')
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except IOError as error:
            print(f'Error al intentar guardar los datos en {self.archivo}: {error}')
        except Exception as error:
            print(f'Error inesperado: {error}')
    
    def añadir_tarea(self, tarea):
        try:
            datos = self.leer_datos()
            número_de_tarea = tarea.número_de_tarea
            if not número_de_tarea in datos.keys():
                datos[número_de_tarea] = tarea.to_dict()
                self.guardar_datos(datos)
                print(f'Tarea {tarea.número_de_tarea}: "{tarea.descripción}" anadida.')
            else:
                print(f"Ya existe una tarea con el número de tarea '{tarea.número_de_tarea}'.")
        except Exception as error:
            print(f'Error inesperado al crear la tarea: {error}')
        
    def leer_tarea(self, número_de_tarea):
        try:
            datos = self.leer_datos()
            if número_de_tarea in datos:
                tarea_data = datos[número_de_tarea]
                if 'Dificultad' in tarea_data:
                    tarea = TareaSimple(**tarea_data)
                else:
                    tarea = TareaRecurrente(**tarea_data)
                print(f"Tarea con el número de tarea '{tarea.número_de_tarea}'.")
                print(tarea)
            else:
                print(f"No existe una tarea con el número de tarea '{tarea.número_de_tarea}'.")
        except Exception as error:
            print(f'Error inesperado al leer la tarea: {error}')

    def actualizar_tarea(self, número_de_tarea, fecha_de_vencimiento, estado):
        try:
            datos = self.leer_datos()
            if número_de_tarea in datos.keys():
                datos[número_de_tarea]['Fecha de vencimiento'] = fecha_de_vencimiento
                datos[número_de_tarea]['Estado'] = estado
                self.guardar_datos(datos)
                print(f"Tarea '{número_de_tarea}' actualizada.")
            else:
                print(f"No existe una tarea con el número de tarea '{número_de_tarea}'.")
        except Exception as error:
            print(f'Error inesperado al actualizar la tarea: {error}')

    def borrar_tarea(self, número_de_tarea):
        try:
            datos = self.leer_datos()
            if número_de_tarea in datos.keys():
                del datos[número_de_tarea]
                self.guardar_datos(datos)
                print(f"Tarea '{número_de_tarea}' borrada.")
            else:
                print(f"No existe una tarea con el número de tarea '{número_de_tarea}'.")
        except Exception as error:
            print(f'Error inesperado al borrar la tarea: {error}')
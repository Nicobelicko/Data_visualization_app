#Detecta el tipo de archivo y utiliza el loader adecuado
#Almacena y gestiona los dataframes cargados
#Proporciona métodos para acceder a los datos

import pandas as pd
import streamlit as st
from typing import Dict, Union, List, Optional, BinaryIO, Tuple
import io

from .data_loader import DataLoaderFactory


class DataManager:
    """Clase para gestionar la carga y almacenamiento de datos"""

    def __init__(self):
        """Inicializa el gestor de datos"""
        # Diccionario para almacenar los dataframes cargados
        #La clave es el nombre del archivo

        if 'loaded_data' not in st.session_state:
            st.session_state.loaded_data = {}

        #Dataframe actualmente seleccionado
        if 'current_df' not in st.session_state:
            st.session_state.current_df = None

        #Nombre del archivo actualmente seleccionado
        if 'current_file' not in st.session_state:
            st.session_state.current_file = None

    def load_file(self,file,**kwargs) -> Tuple[bool,str]:
        """
        Carga un archivo y almacena los datos.
        
        Args:
            file: Objeto de archivo de Streamlit
            **kwargs: Argumentos específicos para cada tipo de cargador
            
        Returns:
            Tupla (éxito, mensaje)
        """

        try:
            if file is None:
                return False, "No se ha seleccionado ningún archivo"
            
            #Obtenemos el loader adecuado
            loader = DataLoaderFactory.get_loader(file.name)

            #Validamos el archivo
            if not loader.validate_file(file):
                return False, f"El archivo {file.name} no es válido para el formato seleccionado"
            
            df = loader.load_data(file,**kwargs)

            # Guardamos los datos en la sesión

            if isinstance(df,dict): #Para excel de múltiples hojas
                for sheet_name, sheet_df in df.items():
                    file_key = f"{file.name} - {sheet_name}"
                    st.session_state.loaded_data[file_key] = sheet_df
                
                #seleccionamos la primera hoja como dataframe actual
                first_sheet = list(df.keys())[0]
                st.session_state.current_df = df[first_sheet]
                st.session_state.current_file = f"{file.name} - {first_sheet}"

                return True, f"Se cargaron {len(df)} hojas del archivo {file.name}"
            
            else:
                #Para archivos con una sola hoja o csv
                st.session_state.loaded_data[file.name] = df
                st.session_state.current_df = df
                st.session_state.current_file = file.name

                return True, f"Archivo {file.name} cargado correctamente"
            
        except Exception as e:
            return False, f"Error al cargar el archivo: {str(e)}"
        
    
    def get_loaded_files(self) -> List[str]:
        """
        Retorna la lista de archivos cargados.
        
        Returns:
            Lista con los nombres de los archivos cargados
        """
        return list(st.session_state.loaded_data.keys())
    
    def select_file(self,file_name: str) -> Tuple[bool,str]:
        """
        Selecciona un archivo como el actual.
        
        Args:
            file_name: Nombre del archivo a seleccionar
            
        Returns:
            Tupla (éxito, mensaje)
        """

        if file_name in st.session_state.loaded_data:
            st.session_state.current_df = st.session_state.loaded_data[file_name]
            st.session_state.current_file = file_name
            return True,f"Archivo {file_name} seleccionado"
        else:
            return False,f"El archivo {file_name} no está cargado"
        
    def get_current_df(self) -> Optional[pd.DataFrame]:

         """
        Retorna el dataframe actualmente seleccionado.
        
        Returns:
            DataFrame actual o None si no hay ninguno seleccionado
        """
         return st.session_state.current_df
    
    def get_current_file(self) -> Optional[str]:

        """
        Retorna el nombre del archivo actualmente seleccionado.
        
        Returns:
            Nombre del archivo actual o None si no hay ninguno seleccionado
        """
        return st.session_state.current_file
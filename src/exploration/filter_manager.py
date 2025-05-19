import pandas as pd
import streamlit as st
from typing import Dict, List, Union, Optional, Tuple, Any
import datetime

class FilterManager:
    """Clase para gestionar múltiples filtros de datos"""

    def __init__(self):
        """Inicializa el gestor de filtros"""
        if 'active_filters' not in st.session_state:
            st.session_state.active_filters = {}

    def add_filter(self, column: str, filter_value: Any) -> None:
        """
        Añade o actualiza un filtro
        
        Args:
            column: Nombre de la columna
            filter_value: Valor del filtro (depende del tipo de columna)
        """
        st.session_state.active_filters[column] = filter_value

    def remove_filter(self, column: str) -> None:
        """
        Elimina un filtro
        
        Args:
            column: Nombre de la columna
        """
        if column in st.session_state.active_filters:
            del st.session_state.active_filters[column]

    def clear_filters(self) -> None:
        """Elimina todos los filtros"""
        st.session_state.active_filters = {}
    
    def get_active_filters(self) -> Dict[str, Any]:
        """
        Retorna los filtros activos
        
        Returns:
            Diccionario con los filtros activos
        """
        return st.session_state.active_filters
    
    def create_filter_widget(self, df: pd.DataFrame, column: str) -> Optional[Tuple[str, Any]]:
        """
        Crea un widget de filtro apropiado para una columna
        
        Args:
            df: DataFrame a filtrar
            column: Nombre de la columna
            
        Returns:
            Tupla (nombre_columna, valor_filtro) o None si no se aplicó filtro
        """

        if column not in df.columns:
            return None
        
        col_dtype = df[column].dtype
        col_data = df[column]

        # Widget para numéricos
        if pd.api.types.is_numeric_dtype(col_dtype):
            min_val = float(col_data.min())
            max_val = float(col_data.max())

            #En caso de valores iguales
            if min_val == max_val:
                min_val -= 1
                max_val += 1

            #Determinar el paso según el rango
            range_val = max_val - min_val
            step = range_val / 100.0 if range_val > 0 else 0.1 #Para la escala del slider

            # Valores por defecto del slider
            default_min = min_val
            default_max = max_val

            # Si hay un filtro activo, usarlo como valor por defecto
            if column in st.session_state.active_filters:
                saved_min, saved_max = st.session_state.active_filters[column]
                default_min = saved_min
                default_max = saved_max
            
            st.write(f"**Filtrar por {column}**")
            filter_value = st.slider(
                f"Rango para {column}",
                min_value=min_val,
                max_value=max_val,
                value=(default_min, default_max),
                step=step
            )

            # Solo retornar si el rango ha cambiado
            if filter_value[0] > min_val or filter_value[1] < max_val:
                return column, filter_value
            
        # Widget para categorías/texto con pocos valores únicos
        elif (pd.api.types.is_categorical_dtype(col_dtype) or pd.api.types.is_object_dtype(col_dtype)) and col_data.nunique() < 50:
            unique_values = sorted(col_data.dropna().unique())

            #valores por defecto
            default_values = []

            #Si hay un filtro activo, usarlo como valor por defecto
            if column in st.session_state.active_filters:
                default_values = st.session_state.active_filters[column]

            st.write(f"**Filtrar por {column}**")
            filter_value = st.multiselect(
                 f"Seleccionar valores para {column}",
                options=unique_values,
                default=default_values
            )

            if filter_value:
                return column, filter_value
        
        # Widget para búsqueda de texto
        elif pd.api.types.is_string_dtype(col_dtype):
            # Valor por defecto
            default_value = ""

            # Si hay un filtro activo, usarlo como valor por defecto
            if column in st.session_state.active_filters:
                default_value = st.session_state.active_filters[column]

            st.write(f"**Buscar en {column}**")
            filter_value = st.text_input(
                f"Texto a buscar en {column}",
                value=default_value
            )

            # Solo retornar si hay texto ingresado
            if filter_value:
                return column, filter_value
            
        # Widget para fechas
        elif pd.api.types.is_datetime64_dtype(col_dtype):
            min_date = col_data.min().to_pydatetime().date()
            max_date = col_data.max().to_pydatetime().date()
            
            # Valores por defecto
            default_start = min_date
            default_end = max_date

            # Si hay un filtro activo, usarlo como valor por defecto
            if column in st.session_state.active_filters:
                saved_start, saved_end = st.session_state.active_filters[column]
                default_start = saved_start
                default_end = saved_end

            st.write(f"**Filtrar por {column}**")
            start_date = st.date_input(
                f"Fecha inicial para {column}",
                value=default_start,
                min_value=min_date,
                max_value=max_date
            )

            end_date = st.date_input(
                f"Fecha final para {column}",
                value=default_end,
                min_value=min_date,
                max_value=max_date
            )

            # Convertir a datetime para comparar con la columna
            start_datetime = pd.Timestamp(start_date)
            end_datetime = pd.Timestamp(end_date)

             
            # Solo retornar si el rango ha cambiado
            if start_datetime > col_data.min() or end_datetime < col_data.max():
                return column, (start_datetime, end_datetime)
            
        return None
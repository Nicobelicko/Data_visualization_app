#Para la expliración, filtrado y manipulación básica de datos
#Funcionalidades principales:

#Selección de columnas específicas
#Filtrado por valores (texto, rango numérico, categorías)
#Ordenamiento por columnas
#Agrupación básica
#Resumen estadístico

import pandas as pd
import streamlit as st
from typing import Dict, List, Union, Optional, Tuple, Any
import numpy as np


class DataExplorer:
    """Clase para explorar y filtrar datos"""

    def __init__(self, df:Optional[pd.DataFrame] = None):
        """
        Inicializa el explorador de datos
        
        Args:
            df: DataFrame opcional para inicializar
        """
        self.original_df = df
        self.filtered_df = df

    def set_data(self, df: pd.DataFrame) -> None:

        """
        Establece el DataFrame a explorar
        
        Args:
            df: DataFrame a explorar
        """
        self.original_df = df.copy()
        self.filtered_df = df.copy()

    def get_column_types(self) -> Dict[str, List[str]]:
        """
        Clasifica las columnas por tipo de datos
        
        Returns:
            Diccionario con las columnas clasificadas por tipo
        """
         
        if self.original_df is None:
            return {}
        
        column_types = {
            'numeric' : [],
            'categorical': [],
            'datetime': [],
            'text': [],
            'boolean': [],
            'other': []
        }

        for column in self.original_df.columns:
            dtype = self.original_df[column].dtype

            if pd.api.types.is_numeric_dtype(dtype):
                if set(self.original_df[column].dropna().unique()).issubset({0,1,True,False}):
                    column_types['boolean'].append(column)
                else:
                    column_types['numeric'].append(column)
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                column_types['datetime'].append(column)
            elif pd.api.types.is_categorical_dtype(dtype) or (self.original_df[column].nunique() < min(20, len(self.original_df) * 0.1)): #valores originalmente categóricos o con 20 o menos del 10% del total de filas son valores únicos
                column_types['categorical'].append(column)
            elif pd.api.types.is_string_dtype(dtype):
                if self.original_df[column].str.len().mean() > 50:
                    column_types['text'].append(column)
                else:
                    column_types['categorical'].append(column)
            else:
                column_types['other'].append(column)
        
        return column_types
    
    def get_column_stats(self, column_name: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de una columna
        
        Args:
            column_name: Nombre de la columna
            
        Returns:
            Diccionario con estadísticas de la columna
        """
         
        if self.original_df is None or column_name not in self.original_df.columns:
            return {}
        
        col_data = self.original_df[column_name]
        stats = {
            'name': column_name,
            'dtype': str(col_data.dtype),
            'count': len(col_data),
            'null_count': col_data.isna().sum(),
            'unique_count': col_data.nunique()
        }

        #Estadísticas específicas por tipo
        if pd.api.types.is_numeric_dtype(col_data.dtype):
            stats.update({
                'min': col_data.min(),
                'max': col_data.max(),
                'mean': col_data.mean(),
                'median': col_data.median(),
                'std': col_data.std()
            })
        elif pd.api.types.is_datetime64_dtype(col_data.dtype):
            stats.update({
                'min': col_data.min(),
                'max': col_data.max(),
                'range_days': (col_data.max() - col_data.min()).days if not pd.isna(col_data.min()) and not pd.isna(col_data.max()) else None
            })
        elif pd.api.types.is_string_dtype(col_data.dtype) or pd.api.types.is_categorical_dtype(col_data.dtype):
             # Para cadenas y categorías, mostrar valores más frecuentes
             value_counts = col_data.value_counts().head(5).to_dict()
             stats['top_values'] = value_counts

             if pd.api.types.is_string_dtype(col_data.dtype):
                # Estadísticas de longitud para cadenas
                stats['mean_length'] = col_data.str.len().mean()
                stats['max_length'] = col_data.str.len().max()
        
        return stats
    
    def filter_by_column_values(self,filters: Dict[str,Any]) -> None:
        """
        Filtra el DataFrame basado en valores de columnas
        
        Args:
            filters: Diccionario con filtros {column_name: filter_value}
                Para numéricos: (min_val, max_val)
                Para categorías: [val1, val2, ...]
                Para texto: string a buscar
                Para fechas: (start_date, end_date)
        """
        if self.original_df is None:
            return
        
        #Partimos del dataframe original
        df = self.original_df.copy()

        #Aplicamos los filtros
        for column,filter_value in filters.items():
            if column not in df.columns:
                continue

            col_dtype = df[column].dtype

            # Filtro para numéricos
            if pd.api.types.is_numeric_dtype(col_dtype) and isinstance(filter_value, tuple) and len(filter_value) == 2:
                min_val, max_val = filter_value
                df = df[(df[column] >= min_val) & (df[column] <= max_val)]

            #Filtro para categorías
            elif (pd.api.types.is_categorical_dtype(col_dtype) or pd.api.types.is_object_dtype(col_dtype)) and isinstance(filter_value, list):
                if filter_value: #Solo si hay valores seleccionados para el filtro
                    df = df[df[column].isin(filter_value)]

            #Filtro para texto
            elif pd.api.types.is_string_dtype(col_dtype) and isinstance(filter_value, str):
                if filter_value: #Solo aplicar si hay texto
                    df = df[df[column].str.contains(filter_value,case=False, na=False)]

            elif pd.api.types.is_datetime64_dtype(col_dtype) and isinstance(filter_value, tuple) and len(filter_value) == 2:
                start_date, end_date = filter_value
                df = df[(df[column] >= start_date) & (df[column] <= end_date)]

        #Guardamos el resultado filtrado
        self.filtered_df = df

    def sort_by_column(self, column: str, ascending: bool = True) -> None:
        """
        Ordena el DataFrame por una columna
        
        Args:
            column: Nombre de la columna
            ascending: True para orden ascendente, False para descendente
        """
        if self.filtered_df is not None and column in self.filtered_df.columns:
            self.filtered_df = self.filtered_df.sort_values(by=column, ascending=ascending)

    def get_filtered_data(self) -> Optional[pd.DataFrame]:
        """
        Retorna el DataFrame filtrado
        
        Returns:
            DataFrame filtrado
        """
        return self.filtered_df
    
    def get_summary_stats(self) -> Optional[pd.DataFrame]:
        """
        Retorna un resumen estadístico del DataFrame
        
        Returns:
            DataFrame con estadísticas resumidas
        """
        if self.filtered_df is None:
            return None
        
        #Crear un resumen personalizado
        numeric_cols = self.filtered_df.select_dtypes(include=['number']).columns

        if len(numeric_cols) > 0:
            summary = self.filtered_df[numeric_cols].describe().T
            #Agregar conteo de nulos
            summary['null_count'] = self.filtered_df[numeric_cols].isna().sum()
            summary['null_percent'] = (self.filtered_df[numeric_cols].isna().sum() / len(self.filtered_df)) * 100
            return summary
        else:
            return pd.DataFrame()
        
    def select_columns(self, columns: List[str]) -> None:
        """
        Selecciona un subconjunto de columnas
        
        Args:
            columns: Lista de nombres de columnas a seleccionar
        """
        if self.filtered_df is not None:
            #Filtramos solo las columnas que existen
            valid_columns = [col for col in columns if col in self.filtered_df.columns] #filtra solo las columnas que esxisten en el dataframe
            if valid_columns:
                self.filtered_df = self.filtered_df[valid_columns]

    def reset_filters(self) -> None:
        """Restablece todos los filtros al DataFrame original"""
        if self.original_df is not None:
            self.filtered_df = self.original_df.copy()

 

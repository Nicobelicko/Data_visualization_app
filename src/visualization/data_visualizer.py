#Clase principal para la visualización de datos
#Crea y gestiona visualizaciones de los datos (originales o filtrados)

#Detección de tipos de datos para sugerir gráficos adecuados
#Creación de gráficos básicos (barras, líneas, dispersión, pastel)
#Personalización de gráficos (títulos, ejes, colores)
#Exportación de gráficos

import pandas as pd
import streamlit as st
from typing import Dict, List, Union, Optional, Any, Type
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import base64

from .chart_base import ChartBase
from .bar_chart import BarChart
from .line_chart import LineChart
from .scatter_chart import ScatterChart

class DataVisualizer:
    """Clase principal para la visualización de datos"""

    def __init__(self):
        """Inicializa el visualizador de datos"""
        self.chart_types = {
            'bar': BarChart(),
            'line': LineChart(),
            'scatter': ScatterChart(),
        }

         # Estado actual del gráfico
        if 'current_chart' not in st.session_state:
            st.session_state.current_chart = None
        
        # Configuración del gráfico actual
        if 'chart_config' not in st.session_state:
            st.session_state.chart_config = {}

    def get_compatible_charts(self, df: pd.DataFrame) -> Dict[str, ChartBase]:
        """
        Determina qué tipos de gráficos son compatibles con el DataFrame actual.
        
        Args:
            df: DataFrame a analizar
            
        Returns:
            Diccionario con los tipos de gráficos compatibles
        """

        if df is None or df.empty:
            return {}
        
        # Clasificamos las columnas por tipo
        column_types = self._classify_columns(df)

        # Verificamos la compatibilidad de cada tipo de gráfico
        compatible_charts = {}
        for chart_name, chart in self.chart_types.items():
            if chart.is_compatible(column_types):
                compatible_charts[chart_name] = chart
        
        return compatible_charts
    
    def _classify_columns(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Clasifica las columnas del DataFrame por tipo de datos.
        
        Args:
            df: DataFrame a clasificar
            
        Returns:
            Diccionario con las columnas clasificadas por tipo
        """
        column_types = {
            'numeric': [],
            'categorical': [],
            'datetime': [],
            'text': [],
            'boolean': [],
            'other': []
        }

        for column in df.columns:
            dtype = df[column].dtype

            if pd.api.types.is_numeric_dtype(dtype):
                # Detectar booleanos codificados como números
                if set(df[column].dropna().unique()).issubset({0, 1, True, False}):
                    column_types['boolean'].append(column)
                else:
                    column_types['numeric'].append(column)
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                column_types['datetime'].append(column)
            elif pd.api.types.is_categorical_dtype(dtype) or (df[column].nunique() < min(20, len(df) * 0.1)):
                column_types['categorical'].append(column)
            elif pd.api.types.is_string_dtype(dtype):
                if df[column].str.len().mean() > 50:
                    column_types['text'].append(column)
                else:
                    column_types['categorical'].append(column)
            else:
                column_types['other'].append(column)
        
        return column_types
    
    def create_chart(self, df: pd.DataFrame, chart_type: str, chart_params: Dict[str, Any]) -> Optional[Any]:
        """
        Crea un gráfico del tipo especificado.
        
        Args:
            df: DataFrame con los datos
            chart_type: Tipo de gráfico a crear
            chart_params: Parámetros para la configuración del gráfico
            
        Returns:
            Figura de Plotly o None si hay un error
        """

        if df is None or df.empty:
            return None
        
        if chart_type not in self.chart_types:
            raise ValueError(f"Tipo de gráfico no soportado: {chart_type}")
        
        chart = self.chart_types[chart_type]

        try:
            # Guardar la configuración actual
            st.session_state.chart_config = {
                'type': chart_type,
                'params': chart_params
            }
            
            # Crear el gráfico
            fig = chart.create_chart(df, **chart_params)
            st.session_state.current_chart = fig
            
            return fig
        except Exception as e:
            st.error(f"Error al crear el gráfico: {str(e)}")
            return None
        
    def update_chart(self, df: pd.DataFrame, update_params: Dict[str, Any]) -> Optional[Any]:
        """
        Actualiza el gráfico actual con nuevos parámetros.
        
        Args:
            df: DataFrame con los datos
            update_params: Parámetros a actualizar
            
        Returns:
            Figura de Plotly actualizada o None si hay un error
        """

        if 'chart_config' not in st.session_state or not st.session_state.chart_config:
            return None
        
        # Obtener la configuración actual
        chart_type = st.session_state.chart_config['type']
        chart_params = st.session_state.chart_config['params'].copy()
        
        # Actualizar los parámetros
        chart_params.update(update_params)
        
        # Crear el gráfico con los parámetros actualizados
        return self.create_chart(df, chart_type, chart_params)
    
    
    
    def get_chart_requirements(self, chart_type: str) -> Dict[str, Dict[str, str]]:
        """
        Obtiene los requisitos para un tipo de gráfico.
        
        Args:
            chart_type: Tipo de gráfico
            
        Returns:
            Diccionario con los parámetros requeridos y opcionales
        """
        if chart_type not in self.chart_types:
            raise ValueError(f"Tipo de gráfico no soportado: {chart_type}")
        
        chart = self.chart_types[chart_type]

        return {
            'required': chart.get_required_parameters(),
            'optional': chart.get_optional_parameters() or {}
        }
    
    def export_chart(self, fig: Any, format: str = 'png') -> Optional[str]:
        """
        Exporta un gráfico en el formato especificado.
        
        Args:
            fig: Figura de Plotly a exportar
            format: Formato de exportación ('png', 'jpg', 'svg', 'html')
            
        Returns:
            URL base64 para descarga o None si hay un error
        """

        if fig is None:
            return None
        
        try:
            if format == 'html':
                buffer = BytesIO()
                fig.write_html(buffer)
                buffer.seek(0)
                b64 = base64.b64encode(buffer.read()).decode()
                return f"data:text/html;base64,{b64}"
            else:
                buffer = BytesIO()
                if format == 'svg':
                    fig.write_image(buffer, format=format)
                else:  # png o jpg
                    fig.write_image(buffer, format=format, engine="kaleido")
                buffer.seek(0)
                b64 = base64.b64encode(buffer.read()).decode()
                return f"data:image/{format};base64,{b64}"
        except Exception as e:
            st.error(f"Error al exportar el gráfico: {str(e)}")
            return None
        
    def get_chart_suggestions(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Genera sugerencias automáticas de gráficos para el DataFrame.
        
        Args:
            df: DataFrame a analizar
            
        Returns:
            Lista de diccionarios con sugerencias de gráficos
        """

        if df is None or df.empty:
            return []
        
        suggestions = []
        column_types = self._classify_columns(df)

        if len(column_types['numeric']) > 0 and len(column_types['categorical']) > 0:
            num_col = column_types['numeric'][0]
            cat_col = column_types['categorical'][0]

            suggestions.append({
                'type': 'bar',
                'title': f"Distribución de {num_col} por {cat_col}",
                'params': {
                    'x': cat_col,
                    'y': num_col
                }
            })

        # Si hay una segunda columna categórica, sugerir gráfico con color
            if len(column_types['categorical']) > 1:
                color_col = column_types['categorical'][1]
                suggestions.append({
                    'type': 'bar',
                    'title': f"Distribución de {num_col} por {cat_col} (agrupado por {color_col})",
                    'params': {
                        'x': cat_col,
                        'y': num_col,
                        'color': color_col,
                        'aggregation': 'sum'
                    }
                })

        # Sugerencias para gráficos de líneas
        if len(column_types['datetime']) > 0 and len(column_types['numeric']) > 0:
            date_col = column_types['datetime'][0]
            num_col = column_types['numeric'][0]
            
            suggestions.append({
                'type': 'line',
                'title': f"Tendencia de {num_col} en el tiempo",
                'params': {
                    'x': date_col,
                    'y': num_col
                }
            })

        # Sugerencias para gráficos de dispersión
        if len(column_types['numeric']) >= 2:
            x_col = column_types['numeric'][0]
            y_col = column_types['numeric'][1]
            
            suggestions.append({
                'type': 'scatter',
                'title': f"Relación entre {x_col} y {y_col}",
                'params': {
                    'x': x_col,
                    'y': y_col
                }
            })

            # Si hay una columna categórica, sugerir gráfico con color
            if len(column_types['categorical']) > 0:
                color_col = column_types['categorical'][0]
                suggestions.append({
                    'type': 'scatter',
                    'title': f"Relación entre {x_col} y {y_col} (agrupado por {color_col})",
                    'params': {
                        'x': x_col,
                        'y': y_col,
                        'color': color_col
                    }
                })
        
        return suggestions
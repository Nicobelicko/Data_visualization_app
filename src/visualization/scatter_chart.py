import pandas as pd
from typing import Dict, List, Union, Optional, Any
import plotly.express as px

from .chart_base import ChartBase

class ScatterChart(ChartBase):
    """Implementación para gráficos de dispersión"""
    
    def create_chart(self, df: pd.DataFrame, **kwargs) -> Any:
        """
        Crea un gráfico de dispersión.
        
        Args:
            df: DataFrame con los datos
            **kwargs: Argumentos para la configuración del gráfico
                - x: Nombre de la columna para el eje X
                - y: Nombre de la columna para el eje Y
                - color: Nombre de la columna para color (opcional)
                - size: Nombre de la columna para tamaño de puntos (opcional)
                - title: Título del gráfico (opcional)
                - opacity: Opacidad de los puntos (opcional)
            
        Returns:
            Figura de Plotly
        """

        # Validamos parámetros requeridos
        if 'x' not in kwargs or 'y' not in kwargs:
            raise ValueError("Los parámetros 'x' y 'y' son requeridos para un gráfico de dispersión")
        
        x = kwargs['x']
        y = kwargs['y']
        title = kwargs.get('title', f'Gráfico de dispersión de {y} vs {x}')
        color = kwargs.get('color')
        size = kwargs.get('size')
        opacity = kwargs.get('opacity', 0.7)

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size=size,
            title=title,
            opacity=opacity,
            labels={x: x, y: y}
        )

         # Configuración adicional
        fig.update_layout(
            xaxis_title=x,
            yaxis_title=y,
            height=600
        )

        return fig
    
    def get_required_parameters(self) -> Dict[str, str]:
        """
        Retorna los parámetros requeridos para un gráfico de dispersión.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        return {
            'x': 'Columna para el eje X',
            'y': 'Columna para el eje Y'
        }
    
    def get_optional_parameters(self) -> Dict[str, str]:
        """
        Retorna los parámetros opcionales para un gráfico de dispersión.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        return {
            'color': 'Columna para asignar colores a los puntos',
            'size': 'Columna para determinar el tamaño de los puntos',
            'title': 'Título del gráfico',
            'opacity': 'Opacidad de los puntos (0-1)'
        }
    
    def is_compatible(self, column_types: Dict[str, List[str]]) -> bool:
        """
        Determina si un gráfico de dispersión es compatible con los tipos de columnas disponibles.
        
        Args:
            column_types: Diccionario con clasificación de columnas por tipo
            
        Returns:
            True si es compatible, False en caso contrario
        """
        # Necesitamos al menos dos columnas numéricas
        numeric_cols = len(column_types.get('numeric', []))
        return numeric_cols >= 2
         

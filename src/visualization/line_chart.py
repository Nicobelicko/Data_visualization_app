import pandas as pd
from typing import Dict, List, Union, Optional, Any
import plotly.express as px

from .chart_base import ChartBase

class LineChart(ChartBase):
    """Implementación para gráficos de líneas"""
    
    def create_chart(self, df: pd.DataFrame, **kwargs) -> Any:
        """
        Crea un gráfico de líneas.
        
        Args:
            df: DataFrame con los datos
            **kwargs: Argumentos para la configuración del gráfico
                - x: Nombre de la columna para el eje X
                - y: Nombre de la columna para el eje Y
                - color: Nombre de la columna para color (opcional)
                - title: Título del gráfico (opcional)
                - markers: True para mostrar marcadores, False para ocultarlos (opcional)
                - aggregation: Función de agregación a aplicar ('sum', 'mean', etc.) (opcional)
            
        Returns:
            Figura de Plotly
        """

        # Validamos parámetros requeridos
        if 'x' not in kwargs or 'y' not in kwargs:
            raise ValueError("Los parámetros 'x' y 'y' son requeridos para un gráfico de líneas")
        
        x = kwargs['x']
        y = kwargs['y']
        title = kwargs.get('title', f'Gráfico de líneas de {y} por {x}')
        color = kwargs.get('color')
        markers = kwargs.get('markers', True)
        aggregation = kwargs.get('aggregation')

        if aggregation:
            # Si hay una columna color, agrupamos por x y color
            if color:
                agg_df = df.groupby([x, color])[y].agg(aggregation).reset_index()
            else:
                agg_df = df.groupby(x)[y].agg(aggregation).reset_index()
            plot_df = agg_df
        else:
            plot_df = df

        # Creamos el gráfico
        fig = px.line(
            plot_df,
            x=x,
            y=y,
            color=color,
            title=title,
            labels={x: x, y: y},
            markers=markers
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
        Retorna los parámetros requeridos para un gráfico de líneas.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        return {
            'x': 'Columna para el eje X (generalmente tiempo o secuencia)',
            'y': 'Columna para el eje Y (valores)'
        }
    
    def get_optional_parameters(self) -> Dict[str, str]:
        """
        Retorna los parámetros opcionales para un gráfico de líneas.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        return {
            'color': 'Columna para asignar colores a múltiples líneas',
            'title': 'Título del gráfico',
            'markers': 'True para mostrar marcadores, False para ocultarlos',
            'aggregation': 'Función de agregación: "sum", "mean", "count", etc.'
        }
    
    def is_compatible(self, column_types: Dict[str, List[str]]) -> bool:
        """
        Determina si un gráfico de líneas es compatible con los tipos de columnas disponibles.
        
        Args:
            column_types: Diccionario con clasificación de columnas por tipo
            
        Returns:
            True si es compatible, False en caso contrario
        """
        # Necesitamos al menos una columna numérica y una de tipo fecha o numérica para el eje X
        has_numeric = len(column_types.get('numeric', [])) > 0
        has_datetime = len(column_types.get('datetime', [])) > 0
        
        # Un gráfico de líneas funciona mejor con fechas, números o categorías ordenadas en el eje X
        has_valid_x = has_datetime or has_numeric or len(column_types.get('categorical', [])) > 0
        
        return has_numeric and has_valid_x
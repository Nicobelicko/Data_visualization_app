import pandas as pd
from typing import Dict, List, Union, Optional, Any
import plotly.express as px


from .chart_base import ChartBase

class BarChart(ChartBase):

    """Implementación para gráficos de barras"""
    
    def create_chart(self, df: pd.DataFrame, **kwargs) -> Any:
        """
        Crea un gráfico de barras.
        
        Args:
            df: DataFrame con los datos
            **kwargs: Argumentos para la configuración del gráfico
                - x: Nombre de la columna para el eje X
                - y: Nombre de la columna para el eje Y
                - color: Nombre de la columna para color (opcional)
                - title: Título del gráfico (opcional)
                - orientation: 'v' para vertical, 'h' para horizontal (opcional)
                - aggregation: Función de agregación a aplicar ('sum', 'mean', etc.) (opcional)
            
        Returns:
            Figura de Plotly
        """

        #Validamos los parámetros requeridos
        if 'x' not in kwargs or 'y' not in kwargs:
            raise ValueError("Los parámetros 'x' y 'y' son requeridos para un gráfico de barras")
        
        x =kwargs['x']
        y =kwargs['y']
        title = kwargs.get('title', f'Gráfico de barras de {y} por {x}')
        color = kwargs.get('color')
        orientation = kwargs.get('orientation', 'v')
        aggregation = kwargs.get('aggregation')

        #Aplicamos agregación si es necesario

        if aggregation:
            #Si hay una columna color, agrupamos por x y color
            if color:
                agg_df = df.groupby([x, color])[y].agg(aggregation).reset_index()
            else:
                agg_df = df.groupby(x)[y].agg(aggregation).reset_index()
            
            plot_df = agg_df
        else:
            plot_df = df

        
        # Creamos el gráfico
        if orientation == 'h':
            fig = px.bar(
                plot_df,
                y=x,
                x=y,
                color=color,
                title=title,
                orientation='h',
                labels={x: x, y: y}
            )
        else:
            fig = px.bar(
                plot_df,
                x=x,
                y=y,
                color=color,
                title=title,
                labels={x: x, y: y}
            )

        # Configuración adicional
        fig.update_layout(
            xaxis_title=x if orientation == 'v' else y,
            yaxis_title=y if orientation == 'v' else x,
            height=600
        )

        return fig
    
    def get_required_parameters(self) -> Dict[str,str]:
        """
        Retorna los parámetros requeridos para un gráfico de barras.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        return {
            'x': 'Columna para el eje X (categorías)',
            'y': 'Columna para el eje Y (valores)'
        }
    
    def get_optional_parameters(self) -> Dict[str, str]:
        """
        Retorna los parámetros opcionales para un gráfico de barras.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        return {
            'color': 'Columna para asignar colores',
            'title': 'Título del gráfico',
            'orientation': 'Orientación: "v" (vertical) o "h" (horizontal)',
            'aggregation': 'Función de agregación: "sum", "mean", "count", etc.'
        }
    
    def is_compatible(self, column_types: Dict[str, List[str]]) -> bool:
        """
        Determina si un gráfico de barras es compatible con los tipos de columnas disponibles.
        
        Args:
            column_types: Diccionario con clasificación de columnas por tipo
            
        Returns:
            True si es compatible, False en caso contrario
        """

        # Necesitamos al menos una columna numérica y una categórica o de texto
        has_numeric = len(column_types.get('numeric', [])) > 0
        has_categories = len(column_types.get('categorical', [])) > 0

        return has_numeric and has_categories
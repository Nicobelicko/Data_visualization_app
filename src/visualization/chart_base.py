from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List, Union, Optional, Any
import plotly.graph_objects as go
import plotly.express as px

class ChartBase(ABC):
    """Clase base abstracta para todos los tipos de gráficos"""

    @abstractmethod
    def create_chart(self, df: pd.DataFrame, **kwargs) -> Any:

        """
        Crea un gráfico a partir de los datos.
        
        Args:
            df: DataFrame con los datos
            **kwargs: Argumentos específicos para cada tipo de gráfico
            
        Returns:
            Objeto de gráfico
        """
        pass

    @abstractmethod
    def get_required_parameters(self) -> Dict[str, str]:
        """
        Retorna los parámetros requeridos para este tipo de gráfico.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        pass

    def get_optional_parameters(self) -> Dict[str, str]:
        """
        Retorna los parámetros opcionales para este tipo de gráfico.
        
        Returns:
            Diccionario con nombres de parámetros y descripciones
        """
        pass

    @abstractmethod
    def is_compatible(self, column_types: Dict[str, List[str]]) -> bool:
        """
        Determina si este tipo de gráfico es compatible con los tipos de columnas disponibles.
        
        Args:
            column_types: Diccionario con clasificación de columnas por tipo
            
        Returns:
            True si es compatible, False en caso contrario
        """
        pass
#clase abstracta
#Defino los metodos para cargar datos e implementa validaciones

from abc import ABC, abstractmethod
import pandas as pd
from typing import Union, List, Dict, Optional, BinaryIO, Tuple
import io

class DataLoader(ABC):
    """Clase base abstracta para todos los cargadores de datos"""
    @abstractmethod
    def load_data(self,file_obj: BinaryIO, **kwargs) -> pd.DataFrame:
        """
        Carga datos desde un archivo y retorna un DataFrame.
    
        Args:
            file_obj: Objeto de archivo a cargar
            **kwargs: Argumentos específicos para cada tipo de cargador
            
        Returns:
            DataFrame con los datos cargados
        """
        pass

    @abstractmethod
    def validate_file(self,file_obj: BinaryIO) -> bool:
        """
        Valida si el archivo es del formato correcto para este cargador.
        
        Args:
            file_obj: Objeto de archivo a validar
            
        Returns:
            True si el archivo es válido, False en caso contrario
        """
        pass
    
    def get_preview(self, df: pd.DataFrame, rows: int = 5) -> pd.DataFrame:
        """
        Obtiene una vista previa de los datos.
        
        Args:
            df: DataFrame con los datos
            rows: Número de filas a mostrar
            
        Returns:
            DataFrame con la vista previa
        """
        return df.head(rows)
    
class DataLoaderFactory:
    """Factory para crear el cargador apropiado según el tipo de archivo"""

    @staticmethod
    def get_loader(file_name: str):
        """
        Retorna el cargador adecuado según la extensión del archivo

        Args:
            file_name: Nombre del archivo

        Returns:
            Instancia del cargador adecuado
        """

        from .csv_loader import CSVLoader
        from .excel_loader import ExcelLoader

        if file_name.lower().endswith('.csv'):
            return CSVLoader()
        elif file_name.lower().endswith(('.xlsx','.xls')):
            return ExcelLoader()
        else: 
            raise ValueError(f"Formato de archivo no soportado: {file_name}")
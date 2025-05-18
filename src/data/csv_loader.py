#Especializada en cargar archivos CSV
#Manejo de delimitadores, codificación, etc.
#Soporte para múltiples archivos CSV

import pandas as pd
from typing import BinaryIO, Dict, Any
import io
from .data_loader import DataLoader

class CSVLoader(DataLoader):
    """Cargador específico para archivos csv"""

    def validate_file(self, file_obj: BinaryIO) -> bool:
         """
        Valida si el archivo es un CSV válido.
        
        Args:
            file_obj: Objeto de archivo a validar
            
        Returns:
            True si el archivo es un CSV válido, False en caso contrario
        """
         try:
              #Guardamos la posición actual en el archivo
              pos = file_obj.tell()

              #Intentamos ller las primeras líneas
              sample = file_obj.read(1024).decode('utf-8')

              #Restauramos la posición
              file_obj.seek(pos)

              #Verificamos si hay almenos una coma o punto y coma
              return ',' in sample or ';' in sample
         except Exception:
              return False
         
    def load_data(self, file_obj: BinaryIO, **kwargs) -> pd.DataFrame:
        """
        Carga datos desde un archivo CSV.
        
        Args:
            file_obj: Objeto de archivo CSV
            **kwargs: Argumentos para pd.read_csv
                - delimiter: Delimitador a usar (por defecto ',')
                - encoding: Codificación del archivo (por defecto 'utf-8')
                
        Returns:
            DataFrame con los datos del CSV
        """
        #Valores por defecto
        delimiter = kwargs.get('delimiter',',')
        encoding = kwargs.get('encoding','utf-8')

        try:
             #creamos una copia en memoria para evitar problemas de buffering
             file_content = io.BytesIO(file_obj.read())

             #Cargamos el csv
             df = pd.read_csv(file_content,delimiter=delimiter, encoding=encoding)

             return df
        except Exception as e:
             raise ValueError(f"Error al cargar el archivo CSV: {str(e)}")
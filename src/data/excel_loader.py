#Especializada en archivos Excel
#Manejo de múltiples hojas
#Opciones para seleccionar hojas específicas

import pandas as pd
from typing import BinaryIO, Dict, List, Union, Optional
import io
from .data_loader import DataLoader

class ExcelLoader(DataLoader):
    """Cargador específico para archivos excel"""

    def validate_file(self, file_obj: BinaryIO) -> bool:
        """
        Valida si el archivo es un Excel válido.
        
        Args:
            file_obj: Objeto de archivo a validar
            
        Returns:
            True si el archivo es un Excel válido, False en caso contrario
        """
        try:
             # Guardamos la posición actual en el archivo
            pos = file_obj.tell()
            
            # Intentamos leer el archivo como Excel
            pd.read_excel(file_obj, sheet_name=None, nrows=1)
            
            # Restauramos la posición
            file_obj.seek(pos)
            
            return True
        
        except Exception:
            # Restauramos la posición en caso de error
            file_obj.seek(pos)
            return False
        
    def load_data(self, file_obj: BinaryIO, **kwargs) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """
        Carga datos desde un archivo Excel.
        
        Args:
            file_obj: Objeto de archivo Excel
            **kwargs: Argumentos para pd.read_excel
                - sheet_name: Nombre o índice de la hoja a cargar (por defecto 0)
                - multi_sheet: Si es True, retorna un diccionario con todas las hojas
                
        Returns:
            DataFrame con los datos o diccionario de DataFrames si multi_sheet=True
        """

        # Valor por defecto
        sheet_name = kwargs.get('sheet_name', 0)
        multi_sheet = kwargs.get('multi_sheet', False)

        try:
            
            # Creamos una copia en memoria para evitar problemas de buffering
            file_content = io.BytesIO(file_obj.read())

            if multi_sheet:
                # Cargamos todas las hojas
                return pd.read_excel(file_content, sheet_name=None)
            else:
                #Cargamos solo la hoja especificada
                return pd.read_excel(file_content,sheet_name=sheet_name)
        except ExcelLoader as e:
            raise ValueError(f"Error al cargarl el archivo Excel: {str(e)}")
        
    def get_sheet_names(self,file_obj: BinaryIO) -> List[str]:
        """
        Obtiene la lista de nombres de hojas en el archivo Excel.
        
        Args:
            file_obj: Objeto de archivo Excel
            
        Returns:
            Lista con los nombres de las hojas
        """
        try:
             # Creamos una copia en memoria para evitar problemas de buffering
            file_content = io.BytesIO(file_obj.read())
            
            # Restauramos la posición
            file_obj.seek(0)
            
            # Obtenemos los nombres de las hojas
            xl = pd.ExcelFile(file_content)
            return xl.sheet_names
        
        except Exception as e:
            raise ValueError(f"Error al leer las hojas del archivo Excel: {str(e)}")
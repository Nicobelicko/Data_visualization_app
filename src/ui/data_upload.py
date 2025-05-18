import streamlit as st
from typing import Dict, Any, Optional
import pandas as pd

from src.data.data_manager import DataManager

def render_data_upload_ui():
    """Renderiza la interfaz de usuario para cargar datos"""

    st.header("📤 Carga de Datos")

    data_manager = DataManager()

    #Widget para subir archivos

    uploaded_file = st.file_uploader(
        "Selecciona un archivo para cargar",
        type=["csv","xlsx","xls"],
        help="Formatos soportados: CSV, Excel (.xlsx, .xls)"
    )

    #Opciones según el tipo de archivo

    if uploaded_file is not None:
        st.subheader("Opciones de carga")

        #Opciones específicas para cada tipo
        load_options = {}

        #Para CSV
        if uploaded_file.name.lower().endswith('csv'):
            delimiter = st.selectbox(
                "Delimitador",
                options=[",", ";", "\\t", "|"],
                index=0,
                help="Selecciona el delimitador usado en el archivo CSV"
            )

            encoding = st.selectbox(
                "Codificación",
                options=["utf-8", "latin-1", "ISO-8859-1"],
                index=0,
                help="Selecciona la codificación del archivo"
            )

            load_options = {
                "delimiter" : delimiter,
                "encoding" : encoding
            }

        elif uploaded_file.name.lower().endswith(('.xlsx','xls')):
            
            #Intentamos obtener los nombres de las hojas

            try:
                from src.data.excel_loader import ExcelLoader
                excel_loader = ExcelLoader()
                sheet_names = excel_loader.get_sheet_names(uploaded_file)

                 # Al obtener los nombres, necesitamos resetear el archivo
                uploaded_file.seek(0)

                sheet_option  = st.radio(
                    "Hojas a cargar",
                    options=["Primera hoja", "Seleccionar una hoja", "Todas las hojas"],
                    index=0,
                    help="Selecciona qué hojas del Excel quieres cargar"
                    )
                
                if sheet_option == "Seleccionar una hoja":
                    selected_sheet = st.selectbox(
                        "Selecciona una hoja",
                        options=sheet_names
                    )
                    load_options = {
                        "sheet_name": selected_sheet,
                        "multi_sheet": False
                    }
                elif sheet_option == "Todas las hojas":
                    load_options={
                        "multi_sheet": True
                    }
                else: #Primera hoja
                    load_options={
                        "sheet_name": 0,
                        "multi_sheet": False
                    }
            except Exception as e:
                st.warning(f"No se pudieron obtener las hojas del archivo: {str(e)}")
                load_options = {
                    "sheet_name":0,
                    "multi_sheet": False
                }
        
        if st.button("Cargar datos"):

            #Reseteamos la posición del archivo
            uploaded_file.seek(0)

            #Cargamos el archivo
            success, message = data_manager.load_file(uploaded_file, **load_options)

            if success:
                st.success(message)
            else:
                st.error(message)

    #Mostramos los archivos cargados
    loaded_files = data_manager.get_loaded_files()
    if loaded_files:
        st.subheader("Archivos cargados")
        selected_file = st.selectbox(
            "Selecciona un archivo",
            options= loaded_files,
            index= loaded_files.index(data_manager.get_current_file()) if data_manager.get_current_file() in loaded_files else 0
        )

        if st.button("Mostrar archivo seleccionado"):
            success, message = data_manager.select_file(selected_file)
            if success:
                st.success(message)
            else:
                st.error(message)

        #Mostramos una vista previa del Dataframe actual
        current_df = data_manager.get_current_df()
        if current_df is not None:
            st.subheader(f"Vista previa: {data_manager.get_current_file()}")
            st.dataframe(current_df.head(10))

            st.text(f"Dimensiones: {current_df.shape[0]} filas x {current_df.shape[1]} columnas")

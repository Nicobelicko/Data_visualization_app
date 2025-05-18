import streamlit as st
from src.ui.data_upload import render_data_upload_ui

def main():
    st.set_page_config(
            page_title="App analisis de datos",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    st.title("📊 Data Analytics Dashboard")

    menu = st.sidebar.selectbox(
        "Menú",
        options = ["Inicio", "Cargar Datos", "Visualizar"],
        index= 0
    )
    if menu == "Inicio":
            st.write("Bienvenido a tu plataforma de análisis de datos")
            st.write("Selecciona una opción del menú para comenzar")
            
            # Tarjetas de funcionalidades
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("📤 **Cargar Datos**\n\n"
                    "Sube tus archivos CSV o Excel")
            
            with col2:
                st.info("📊 **Visualizar**\n\n"
                    "Crea gráficos y tablas interactivas")
            
            with col3:
                st.info("🔍 **Analizar**\n\n"
                    "Realiza análisis automáticos de tus datos")
    
    
    elif menu == "Cargar Datos":
        render_data_upload_ui()

    else:
       st.info(f"La funcionalidad '{menu}' será implementada proximamente")
   
   

if __name__ == "__main__":
    main()
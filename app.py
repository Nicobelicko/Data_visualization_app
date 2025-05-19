import streamlit as st
from src.ui.data_upload import render_data_upload_ui
from src.ui.data_visualization import render_data_visualization_ui

def main():
    st.set_page_config(
            page_title="App analisis de datos",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    st.title("Aplicativo análisis de datos")

    if "funcionalidad_seleccionada" not in st.session_state:
        st.session_state.funcionalidad_seleccionada = "Inicio"

    menu = st.sidebar.selectbox(
        "Menú",
        options = ["Inicio", "Cargar Datos", "Visualizar", "IA"],
        index= 0
    )

    
    if menu == "Inicio":
            st.write("Bienvenido a tu plataforma de análisis de datos")
            st.write("Algunas de las funcionalidades que puedes usar:")
            
            # Tarjetas de funcionalidades
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("📤 **Cargar Datos**\n\n"
                    "Sube tus archivos CSV o Excel")
            
            with col2:
                st.info("📊 **Visualizar**\n\n"
                    "Crea gráficos y tablas interactivas")
                funcionalidad = "Visualizar"
            
            with col3:
                st.info("🤖 **IA**\n\n"
                    "Realiza análisis automáticos de tus datos (PROXIMAMENTE)")
                
    
    
    elif menu == "Cargar Datos":
        render_data_upload_ui()

    elif menu == "Visualizar":
        render_data_visualization_ui()

    else:
       st.info(f"La funcionalidad '{menu}' será implementada proximamente")
   
def change_menu_selection(funcionalidad):
    st.session_state.funcionalidad_seleccionada = funcionalidad

if __name__ == "__main__":
    main()
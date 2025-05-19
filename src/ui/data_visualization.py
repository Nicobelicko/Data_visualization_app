import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional

from src.data.data_manager import DataManager
from src.exploration.data_explorer import DataExplorer
from src.visualization.data_visualizer import DataVisualizer

def render_data_visualization_ui():
    """Renderiza la interfaz de usuario para visualizar datos"""

    st.header("📊 Visualización de Datos")

    # Inicializamos los objetos necesarios
    data_manager = DataManager()
    data_explorer = DataExplorer()
    data_visualizer = DataVisualizer()

    # Obtenemos el DataFrame actual
    current_df = data_manager.get_current_df()
    current_file = data_manager.get_current_file()

    if current_df is None:
        st.warning("📤 No hay datos cargados. Por favor, carga un archivo primero en la sección 'Cargar Datos'.")
        return
    
    # Establecemos los datos en el explorador
    data_explorer.set_data(current_df)

    # Mostramos información del dataset actual
    st.subheader(f"📄 Dataset actual: {current_file}")
    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Filas: {current_df.shape[0]} | Columnas: {current_df.shape[1]}")
    with col2:
        st.info(f"Memoria utilizada: {current_df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")


     # Panel de filtros
    with st.expander("🔍 Filtros de datos", expanded=False):
        render_filters_section(current_df, data_explorer)

    tab1, tab2, tab3 = st.tabs(["📈 Crear gráfico", "🧙‍♂️ Sugerencias automáticas", "📋 Vista de datos"])

    with tab1:
        render_chart_creation_section(current_df, data_visualizer)

    with tab2:
        render_chart_suggestions_section(current_df, data_visualizer)

    with tab3:
        render_data_view_section(data_explorer.get_filtered_data())

def render_filters_section(df: pd.DataFrame, data_explorer: DataExplorer):
    """Renderiza la sección de filtros"""
    
    st.subheader("Filtrar datos")

    # Obtenemos la clasificación de columnas
    column_types = data_explorer.get_column_types()

    # Selección de columnas
    st.write("**Selección de columnas**")
    all_columns = list(df.columns)
    selected_columns = st.multiselect(
        "Selecciona las columnas a mostrar",
        options=all_columns,
        default=all_columns
    )

    if st.button("Aplicar selección de columnas"):
        data_explorer.select_columns(selected_columns)
    
    st.divider()

    # Filtros para columnas numéricas
    if column_types.get('numeric'):
        st.write("**Filtros numéricos**")
        numeric_col = st.selectbox(
            "Selecciona una columna numérica",
            options=column_types['numeric']
        )
        
        min_val = float(df[numeric_col].min())
        max_val = float(df[numeric_col].max())
        
     # Ajustar para evitar valores iguales
        if min_val == max_val:
            min_val -= 1
            max_val += 1
        
        num_range = st.slider(
            f"Rango para {numeric_col}",
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val)
        )

        if st.button("Aplicar filtro numérico"):
            filters = {numeric_col: num_range}
            data_explorer.filter_by_column_values(filters)

    # Filtros para columnas categóricas
    if column_types.get('categorical'):
        st.write("**Filtros categóricos**")
        cat_col = st.selectbox(
            "Selecciona una columna categórica",
            options=column_types['categorical']
        )

        unique_values = sorted(df[cat_col].dropna().unique())
        selected_values = st.multiselect(
            f"Valores para {cat_col}",
            options=unique_values,
            default=[]
        )
        
        if st.button("Aplicar filtro categórico"):
            if selected_values:
                filters = {cat_col: selected_values}
                data_explorer.filter_by_column_values(filters)

    # Botón para ordenar
    st.write("**Ordenamiento**")
    sort_col = st.selectbox(
        "Ordenar por columna",
        options=all_columns
    )


    sort_order = st.radio(
        "Orden",
        options=["Ascendente", "Descendente"],
        horizontal=True
    )

    if st.button("Aplicar ordenamiento"):
        data_explorer.sort_by_column(sort_col, sort_order == "Ascendente")

    # Botón para reiniciar todos los filtros
    if st.button("🔄 Reiniciar todos los filtros"):
        data_explorer.reset_filters()

def render_chart_creation_section(df: pd.DataFrame, data_visualizer: DataVisualizer):
    """Renderiza la sección de creación de gráficos"""
    
    st.subheader("Crear gráfico personalizado")

    # Obtenemos los tipos de gráficos compatibles
    compatible_charts = data_visualizer.get_compatible_charts(df)
    
    if not compatible_charts:
        st.warning("No hay tipos de gráficos compatibles con los datos actuales.")
        return
    
    # Selección del tipo de gráfico
    chart_options = list(compatible_charts.keys())
    selected_chart = st.selectbox(
        "Selecciona el tipo de gráfico",
        options=chart_options,
        format_func=lambda x: x.capitalize()
    )

    # Obtenemos los requisitos del gráfico
    chart_reqs = data_visualizer.get_chart_requirements(selected_chart)
    
    # Parámetros para el gráfico
    st.write("**Parámetros del gráfico**")
    chart_params = {}

    # Parámetros requeridos
    for param, desc in chart_reqs['required'].items():
        param_value = st.selectbox(
            f"{param}: {desc}",
            options=df.columns,
            key=f"req_{param}"
        )
        chart_params[param] = param_value

    # Parámetros opcionales
    st.write("**Opciones adicionales**")
    
    # Título (común a todos los gráficos)
    chart_title = st.text_input(
        "Título del gráfico",
        value=f"Gráfico de {selected_chart.capitalize()}"
    )
    chart_params['title'] = chart_title

    # Otros parámetros opcionales específicos del tipo de gráfico
    for param, desc in chart_reqs['optional'].items():
        if param == 'color':
            param_value = st.selectbox(
                f"{param}: {desc}",
                options=['Ninguno'] + list(df.columns),
                key=f"opt_{param}"
            )
            if param_value != 'Ninguno':
                chart_params[param] = param_value

        elif param == 'aggregation':
            agg_options = ['Ninguna', 'sum', 'mean', 'count', 'min', 'max']
            param_value = st.selectbox(
                f"{param}: {desc}",
                options=agg_options,
                key=f"opt_{param}"
            )
            if param_value != 'Ninguna':
                chart_params[param] = param_value
        
        elif param == 'orientation':
            param_value = st.radio(
                f"{param}: {desc}",
                options=['v', 'h'],
                format_func=lambda x: 'Vertical' if x == 'v' else 'Horizontal',
                horizontal=True,
                key=f"opt_{param}"
            )
            chart_params[param] = param_value

        elif param == 'markers':
            param_value = st.checkbox(
                f"{param}: {desc}",
                value=True,
                key=f"opt_{param}"
            )
            chart_params[param] = param_value

        elif param == 'opacity':
            param_value = st.slider(
                f"{param}: {desc}",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                key=f"opt_{param}"
            )
            chart_params[param] = param_value
        
        elif param == 'size':
            param_value = st.selectbox(
                f"{param}: {desc}",
                options=['Ninguno'] + list(df.columns),
                key=f"opt_{param}"
            )
            if param_value != 'Ninguno':
                chart_params[param] = param_value
            
    # Botón para crear el gráfico
    if st.button("🎨 Generar gráfico"):
        fig = data_visualizer.create_chart(df, selected_chart, chart_params)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Opciones de exportación
            st.write("**Exportar gráfico**")
            export_format = st.radio(
                "Formato de exportación",
                options=["PNG", "SVG", "HTML"],
                horizontal=True
            )

            if st.button("📥 Descargar gráfico"):
                export_url = data_visualizer.export_chart(fig, export_format.lower())
                if export_url:
                    st.markdown(
                        f'<a href="{export_url}" download="grafico.{export_format.lower()}" target="_blank">'
                        f'Haz clic aquí para descargar el gráfico ({export_format})</a>',
                        unsafe_allow_html=True
                    )

def render_chart_suggestions_section(df: pd.DataFrame, data_visualizer: DataVisualizer):
    """Renderiza la sección de sugerencias de gráficos"""
    
    st.subheader("Sugerencias automáticas de gráficos")
    
    # Generamos las sugerencias
    suggestions = data_visualizer.get_chart_suggestions(df)
    
    if not suggestions:
        st.warning("No se han podido generar sugerencias de gráficos para los datos actuales.")
        return
    
    st.write("Hemos analizado tus datos y te sugerimos los siguientes gráficos:")

    for i, suggestion in enumerate(suggestions, 1):
        with st.expander(f"Sugerencia {i}: {suggestion['title']}"):
            st.write(f"**Tipo de gráfico:** {suggestion['type'].capitalize()}")
            st.write("**Parámetros:**")
            for key, value in suggestion['params'].items():
                st.write(f"- {key}: {value}")
            
            if st.button(f"📊 Mostrar gráfico", key=f"suggestion_{i}"):
                fig = data_visualizer.create_chart(df, suggestion['type'], suggestion['params'])
                if fig:
                    st.plotly_chart(fig, use_container_width=True)

def render_data_view_section(df: Optional[pd.DataFrame]):
    """Renderiza la sección de vista de datos"""
    
    st.subheader("Vista de datos filtrados")
    
    if df is None or df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return
    
    # Opciones de visualización
    view_options = st.radio(
        "Mostrar como",
        options=["Tabla", "Resumen estadístico"],
        horizontal=True
    )

    if view_options == "Tabla":
        # Mostrar los primeros n registros
        num_rows = st.slider("Número de filas a mostrar", 5, min(100, len(df)), 20)
        st.dataframe(df.head(num_rows), use_container_width=True)
        
        # Información adicional
        st.info(f"Mostrando {num_rows} de {len(df)} filas totales")

    else:
        # Resumen estadístico
        st.write("**Resumen estadístico de columnas numéricas**")
        
        # Seleccionamos solo columnas numéricas
        numeric_df = df.select_dtypes(include=['number'])

        if not numeric_df.empty:
            st.dataframe(numeric_df.describe(), use_container_width=True)
        else:
            st.warning("No hay columnas numéricas en los datos filtrados.")

        

    
    


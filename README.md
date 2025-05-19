# Data_visualization_app
El objetivo de este aplicativo es permitir a los usuarios cargar sus datos para poder visualizar y filtrar datos de forma que sirvan para tomar decisiones estratégicas del negocio

## Características

- Carga de archivos de datos en formato CSV.
- Visualización interactiva de datos mediante gráficos y tablas.
- Filtros personalizables para explorar subconjuntos específicos de datos.
- Consultas dinámicas para obtener insights clave.
- Interfaz intuitiva y fácil de usar.

## Tecnologías utilizadas

- Python 3
- Streamlit
- Pandas
- Plotly
- Altair
- Matplotlib
- openpyxl

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/Nicobelicko/Data_visualization_app.git
   cd Data_visualization_app
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv nombre_entorno
   En Windows: .\nombre_entorno\Scripts\activate
   ```

3. Instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
streamlit run app.py
```

Una vez en funcionamiento, podrás cargar tus archivos CSV y comenzar a explorar tus datos de manera interactiva.

## Estructura del proyecto

```plaintext
├── app.py                 # Archivo principal de la aplicación Streamlit
├── requirements.txt       # Lista de dependencias del proyecto
├── README.md              # Documentación del proyecto
├── .gitignore             # Archivos y carpetas ignorados por Git
└── src/                    # Código fuente principal
│   ├── __init__.py
│   ├── data/               # Clases para manejo de datos
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   └── data_processor.py
│   │
│   ├── visualization/      # Clases para visualización
│   │   ├── __init__.py
│   │   ├── charts.py
│   │   └── tables.py
│   │
│   └── ui/                 # Componentes de interfaz
│       ├── __init__.py
│       ├── login.py
│       ├── sidebar.py
│       └── pages.py
│
```

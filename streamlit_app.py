import streamlit as st
import requests
import random
import plotly.graph_objects as go



st.set_page_config(layout="wide")

# Título de la aplicación
st.title("Estadísticas de Etiquetadores ⚽ 🏃‍♂️💨")

# Crear un sidebar para seleccionar fechas
st.sidebar.title("Seleccionar Fechas")


# Calendario para la fecha inicial
start_date = st.sidebar.date_input("Fecha Inicial")

# Calendario para la fecha final
end_date = st.sidebar.date_input("Fecha Final")

# Lista de tuplas que contiene las URLs y las claves API correspondientes
urls = [(st.secrets["URLS"]["URL1"],st.secrets["KEYS"]["KEY1"]),
        (st.secrets["URLS"]["URL2"],st.secrets["KEYS"]["KEY2"]),
        (st.secrets["URLS"]["URL3"],st.secrets["KEYS"]["KEY3"])
]
# Definir una función para obtener los datos de la API y cachear los resultados
@st.cache_data
def get_labelers_data(start_date, end_date):
    labelers_data = {}
    for url, api_key in urls:
        params = {
            "api_key": api_key,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d")
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            labelers = data["labelers"]
            for labeler in labelers:
                labeler_id = labeler["id"]
                labeler_name = labeler["displayName"]
                images_labeled = sum(entry["imagesLabeled"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                boxes_labeled = sum(entry["boxesDrawn"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                if labeler_id not in labelers_data:
                    labelers_data[labeler_id] = {"name": labeler_name, "images": images_labeled, "boxes": boxes_labeled}
                else:
                    labelers_data[labeler_id]["images"] += images_labeled
                    labelers_data[labeler_id]["boxes"] += boxes_labeled
        else:
            st.error(f"Error al realizar la solicitud a la API: {url}")
    return labelers_data

# Obtener los datos de los etiquetadores
labelers_data = get_labelers_data(start_date, end_date)

# Guardar los checkbox de visibilidad para cada etiquetador
labelers_visibility = {}
color_options = ["blue", "green", "orange", "red", "violet","gray", "white"]
color_index = 0
for labeler_id, data in labelers_data.items():
    labeler_name = data["name"]
    random.seed(labeler_id)
    color = color_options[color_index % len(color_options)]
    color_index += 1
    colored_label = f":{color}[{labeler_name}]"
    labelers_visibility[labeler_id] = st.sidebar.checkbox(colored_label, value=True, key=labeler_id)



selected_labelers = {labeler_id: data for labeler_id, data in labelers_data.items() if labelers_visibility[labeler_id]}
if selected_labelers:
    # Dividir en dos columnas
    col1, col2 = st.columns(2)
    
    # Gráfico de "Imágenes Etiquetadas"
    with col1:
        fig1 = go.Figure()
        for labeler_id, data in selected_labelers.items():
            random.seed(labeler_id)
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            fig1.add_trace(go.Bar(
                x=[data['name']],
                y=[data['images']],
                name=data['name'],
                marker_color=color
            ))
        fig1.update_layout(title='Imágenes Etiquetadas por Etiquetador 🚀🚀🚀', xaxis_title='Etiquetador', yaxis_title='Imágenes Etiquetadas')
        st.plotly_chart(fig1)
    
    # Gráfico de "Cajas Etiquetadas"
    with col2:
        fig2 = go.Figure()
        for labeler_id, data in selected_labelers.items():
            random.seed(labeler_id)
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            fig2.add_trace(go.Bar(
                x=[data['name']],
                y=[data['boxes']],
                name=data['name'],
                marker_color=color
            ))
        fig2.update_layout(title='Cajas Etiquetadas por Etiquetador 🚀🚀🚀', xaxis_title='Etiquetador', yaxis_title='Cajas Etiquetadas')
        st.plotly_chart(fig2)
if selected_labelers:
    # Dividir en dos columnas
    col3, col4 = st.columns(2)
    
    # Gráfico de sector para el porcentaje de "Imágenes Etiquetadas"
    with col3:
        fig3 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['images'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig3.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig3.update_layout(title='Porcentaje de Imágenes Etiquetadas por Etiquetador')
        st.plotly_chart(fig3)
    
    # Gráfico de sector para el porcentaje de "Cajas Etiquetadas"
    with col4:
        fig4 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['boxes'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig4.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig4.update_layout(title='Porcentaje de Cajas Etiquetadas por Etiquetador')
        st.plotly_chart(fig4)
if selected_labelers:
    # Dividir en dos columnas
    col5, col6 = st.columns(2)
    
    # Barra de progreso para imágenes etiquetadas
    with col5:
        st.subheader('Progreso de Imágenes Etiquetadas')
        for labeler_id, data in selected_labelers.items():
            images_progress = min((data['images'] / 500), 1.0)  # Asegurar que esté dentro del rango [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(images_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["images"]} / 500')

    # Barra de progreso para cajas etiquetadas
    with col6:
        st.subheader('Progreso de Cajas Etiquetadas')
        for labeler_id, data in selected_labelers.items():
            boxes_progress = min((data['boxes'] / 8000), 1.0)  # Asegurar que esté dentro del rango [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(boxes_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["boxes"]} / 8000')

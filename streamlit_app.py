import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging
from functions import get_labelers_data
st.set_page_config(layout="wide")

# Configure logging to save to a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Application Title
st.title("Labelers Statistics ⚽ 🏃‍♂️💨")

# Create a sidebar to select dates
st.sidebar.title("Select Dates")

# Calendar for start date
start_date = st.sidebar.date_input("Start Date")

# Calendar for end date
end_date = st.sidebar.date_input("End Date")

# List of tuples containing URLs and corresponding API keys
urls = [
    (st.secrets["URLS"]["URL1"],st.secrets["KEYS"]["KEY1"]),
        (st.secrets["URLS"]["URL2"],st.secrets["KEYS"]["KEY2"]),
        (st.secrets["URLS"]["URL3"],st.secrets["KEYS"]["KEY3"])
]

# Define a function to get the API data and cache the results
@st.cache_data


# Get the labelers' data
labelers_data = get_labelers_data(start_date, end_date)

# Store visibility checkboxes for each labeler
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
    # Split into two columns
    col1, col2 = st.columns(2)
    
    # "Images Labeled" Chart
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
        fig1.update_layout(title='Images Labeled by Labeler 🚀🚀🚀', xaxis_title='Labeler', yaxis_title='Images Labeled')
        st.plotly_chart(fig1)
    
    # "Boxes Labeled" Chart
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
        fig2.update_layout(title='Boxes Labeled by Labeler 🚀🚀🚀', xaxis_title='Labeler', yaxis_title='Boxes Labeled')
        st.plotly_chart(fig2)

if selected_labelers:
    # Split into two columns
    col3, col4 = st.columns(2)
    
    # Pie chart for "Images Labeled" percentage
    with col3:
        fig3 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['images'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig3.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig3.update_layout(title='Percentage of Images Labeled by Labeler')
        st.plotly_chart(fig3)
    
    # Pie chart for "Boxes Labeled" percentage
    with col4:
        fig4 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['boxes'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig4.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig4.update_layout(title='Percentage of Boxes Labeled by Labeler')
        st.plotly_chart(fig4)

if selected_labelers:
    # Split into two columns
    col5, col6 = st.columns(2)
    
    # Progress bar for labeled images
    with col5:
        st.subheader('Progress of Images Labeled')
        for labeler_id, data in selected_labelers.items():
            images_progress = min((data['images'] / 500), 1.0)  # Ensure it is within [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(images_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["images"]} / 500')

    # Progress bar for labeled boxes
    with col6:
        st.subheader('Progress of Boxes Labeled')
        for labeler_id, data in selected_labelers.items():
            boxes_progress = min((data['boxes'] / 8000), 1.0)  # Ensure it is within [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(boxes_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["boxes"]} / 8000')

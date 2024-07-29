import streamlit as st
import requests
import random
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Application Title
st.title("Labelers Statistics ⚽ 🏃‍♂️💨")

# Create a sidebar to select dates
st.sidebar.title("Select Dates")

# Calendar for the start date
start_date = st.sidebar.date_input("Start Date")

# Calendar for the end date
end_date = st.sidebar.date_input("End Date")

# List of tuples containing URLs and corresponding API keys
urls = [(st.secrets["URLS"]["URL1"],st.secrets["KEYS"]["KEY1"]),
        (st.secrets["URLS"]["URL2"],st.secrets["KEYS"]["KEY2"]),
        (st.secrets["URLS"]["URL3"],st.secrets["KEYS"]["KEY3"])
]

# Define a function to get the data from the API and cache the results
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
            st.error(f"Error in API request: {url}")
    return labelers_data

# Get the labelers data
labelers_data = get_labelers_data(start_date, end_date)

# Save the visibility checkboxes for each labeler
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
    
    # "Labeled Images" Chart
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
        fig1.update_layout(title='Labeled Images by Labeler 🚀🚀🚀', xaxis_title='Labeler', yaxis_title='Labeled Images')
        st.plotly_chart(fig1)
    
    # "Labeled Boxes" Chart
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
        fig2.update_layout(title='Labeled Boxes by Labeler 🚀🚀🚀', xaxis_title='Labeler', yaxis_title='Labeled Boxes')
        st.plotly_chart(fig2)
if selected_labelers:
    # Split into two columns
    col3, col4 = st.columns(2)
    
    # Pie chart for the percentage of "Labeled Images"
    with col3:
        fig3 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['images'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig3.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig3.update_layout(title='Percentage of Labeled Images by Labeler')
        st.plotly_chart(fig3)
    
    # Pie chart for the percentage of "Labeled Boxes"
    with col4:
        fig4 = go.Figure()
        labels = [data['name'] for data in selected_labelers.values()]
        values = [data['boxes'] for data in selected_labelers.values()]
        colors = [color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)] for labeler_id in selected_labelers.keys()]
        fig4.add_trace(go.Pie(labels=labels, values=values, marker=dict(colors=colors)))
        fig4.update_layout(title='Percentage of Labeled Boxes by Labeler')
        st.plotly_chart(fig4)
if selected_labelers:
    # Split into two columns
    col5, col6 = st.columns(2)
    
    # Progress bar for labeled images
    with col5:
        st.subheader('Labeled Images Progress')
        for labeler_id, data in selected_labelers.items():
            images_progress = min((data['images'] / 500), 1.0)  # Ensure it's within the range [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(images_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["images"]} / 500')

    # Progress bar for labeled boxes
    with col6:
        st.subheader('Labeled Boxes Progress')
        for labeler_id, data in selected_labelers.items():
            boxes_progress = min((data['boxes'] / 8000), 1.0)  # Ensure it's within the range [0.0, 1.0]
            color = color_options[list(labelers_visibility.keys()).index(labeler_id) % len(color_options)]
            st.progress(boxes_progress)
            st.subheader(f':{color}[{data["name"]}]: {data["boxes"]} / 8000')

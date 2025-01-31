import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging
#function
@st.cache_data
def get_labelers_data(start_date, end_date, urls):
    labelers_data = {}
    logging.info(f"Fetching data from {start_date} to {end_date}")
    for url, api_key, _ in urls:
        params = {
            "api_key": api_key,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d")
        }
        logging.info(f"Making request to {url} with params {params}")
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            logging.info(f"Data received from {url}: {data}")
            labelers = data["labelers"]
            for labeler in labelers:
                labeler_id = labeler["id"]
                labeler_name = labeler["displayName"]
                images_labeled = sum(entry["imagesLabeled"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                boxes_labeled = sum(entry["boxesDrawn"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                boxes_added = sum(entry["boxesAdded"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                boxes_removed = sum(entry["boxesRemoved"] for entry in data["data"] if entry["labelerId"] == labeler_id)
                boxes_updated = sum(entry["boxesUpdated"] for entry in data["data"] if entry["labelerId"] == labeler_id)

                
                # Save Data for each URL separately
                if labeler_id not in labelers_data:
                    labelers_data[labeler_id] = {
                        "name": labeler_name,
                        "urls": {}
                    }
                
                labelers_data[labeler_id]["urls"][url] = {
                    "images": images_labeled,
                    "boxes": boxes_labeled,
                    "boxesAdded": boxes_added,    # <-- Añadimos el valor de boxesAdded
                    "boxesRemoved": boxes_removed, # <-- Añadimos el valor de boxesRemoved
                    "boxesUpdated": boxes_updated
                }
        else:
            st.error(f"Error making API request: {url}")
            logging.error(f"Request error to {url}: {response.status_code}")
    logging.info(f"Accumulated data: {labelers_data}")
    return labelers_data

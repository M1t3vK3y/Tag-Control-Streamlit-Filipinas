import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging

#secrets
urls = [
    (st.secrets["URLS"]["URL1"],st.secrets["KEYS"]["KEY1"],st.secrets["NAMES"]["NAME1"]),
        (st.secrets["URLS"]["URL2"],st.secrets["KEYS"]["KEY2"],st.secrets["NAMES"]["NAME2"]),
        (st.secrets["URLS"]["URL3"],st.secrets["KEYS"]["KEY3"],st.secrets["NAMES"]["NAME3"]),
        (st.secrets["URLS"]["URL4"],st.secrets["KEYS"]["KEY4"],st.secrets["NAMES"]["NAME4"]),
        (st.secrets["URLS"]["URL5"],st.secrets["KEYS"]["KEY5"],st.secrets["NAMES"]["NAME5"]),
        (st.secrets["URLS"]["URL6"],st.secrets["KEYS"]["KEY6"],st.secrets["NAMES"]["NAME6"])
]
# Store visibility checkboxes for each labeler
labelers_visibility = {}
labeler_color_map = {}
color_options = ["blue", "green", "orange", "red", "violet","gray"]
color_index = 0

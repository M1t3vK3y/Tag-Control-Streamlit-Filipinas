import streamlit as st
import requests
import random
import plotly.graph_objects as go
import logging

urls = [
    (st.secrets["URLS"]["URL1"],st.secrets["KEYS"]["KEY1"]),
        (st.secrets["URLS"]["URL2"],st.secrets["KEYS"]["KEY2"]),
        (st.secrets["URLS"]["URL3"],st.secrets["KEYS"]["KEY3"])
]
labelers_visibility = {}
color_options = ["blue", "green", "orange", "red", "violet","gray", "white"]
color_index = 0

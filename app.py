import os
import datetime
import numpy as np
import pandas as pd
import streamlit as st
import earthaccess as ea
import cartopy.crs as ccrs
from yaml import safe_load
from memray import Tracker
from utils.constants import MIN_DATE, MAX_DATE

st.title("Nimbus")
st.markdown("Visualizing Earth systems")

form = st.form("job-form")

with form:
    with open("observations.yml", "r") as f:
        datasets = safe_load(f)

    selected_dataset = st.selectbox(
        "Choose a dataset",
        datasets.keys()
    )

    start = st.date_input(
        "Start date",
        min_value=MIN_DATE,
        max_value=MAX_DATE
    )
    end   = st.date_input(
        "End date",
        min_value=MIN_DATE,
        max_value=MAX_DATE
    )

    zipimg  = st.checkbox("Zip frames")
    video   = st.checkbox("Render video")
    metrics = st.checkbox("Show metrics")
    interp  = st.checkbox("Interpolate frames")
    summary = st.checkbox("Summarize metrics")

    auth_msg = st.warning(
        "If your EarthData credentials are not set as environment variables, enter them below. " \
        "Otherwise, leave these following fields blank."
    )

    user_auth = st.text_input(
        "Enter your EarthData username"
    )
    user_pass = st.text_input(
        "Enter your EarthData password",
        type="password"
    )

    submit = st.form_submit_button("Submit")
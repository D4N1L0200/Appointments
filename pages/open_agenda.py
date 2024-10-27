import streamlit as st  # type: ignore
from view import View
import pandas as pd  # type: ignore

from models.client import Client
from models.service import Service
from models.appointment import Appointment

from typing import Union
from datetime import datetime, time

View.load_clients()
View.load_services()
View.load_appointments()

st.set_page_config(
    page_title="Open Agenda",
    page_icon="👋",
)

with st.sidebar:
    st.page_link("main.py", label="Appointment System")
    st.page_link("pages/clients.py", label="Clients Manager")
    st.page_link("pages/services.py", label="Services Manager")
    st.page_link("pages/appointments.py", label="Appointments Manager")
    st.page_link("pages/open_agenda.py", label="Open Agenda")

st.header("Open Agenda")

services: list[Service] = View.get_services()

if len(services) > 0:
    service: Union[Service, None] = st.selectbox(
        "Select the service", services, index=None
    )
else:
    st.warning("There are no services to select.")

date = st.date_input("Select the date")

start_time = st.time_input("Select the start time", value=time(8, 0))
end_time = st.time_input("Select the end time", value=time(18, 0))

spacing = st.time_input("Select the time between appointments", value=time(0, 0))

if st.button("Open Agenda"):
    if (
        service is not None
        and date is not None
        and start_time is not None
        and end_time is not None
        and spacing is not None
        and start_time < end_time
    ):
        count: int = View.open_agenda(
            service.get_id(), date, start_time, end_time, spacing
        )
        st.success(f"Agenda opened, {count} available appointments created.")
    else:
        st.warning("Please fill in all fields correctly.")

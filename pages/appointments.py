import streamlit as st  # type: ignore
from view import View
import pandas as pd  # type: ignore

from models.client import Client
from models.service import Service
from models.appointment import Appointment

from typing import Union
from datetime import datetime

View.load_clients()
View.load_services()
View.load_appointments()

st.set_page_config(
    page_title="Appointments",
    page_icon="👋",
)

with st.sidebar:
    st.page_link("main.py", label="Appointment System")
    st.page_link("pages/clients.py", label="Clients Manager")
    st.page_link("pages/services.py", label="Services Manager")
    st.page_link("pages/appointments.py", label="Appointments Manager")
    st.page_link("pages/open_agenda.py", label="Open Agenda")

st.header("Appointment Manager")

available_tab, scheduled_tab, schedule_tab, update_tab, delete_tab = st.tabs(
    [
        "List Available",
        "List Scheduled",
        "Schedule Appointment",
        "Update Appointment",
        "Delete Appointment",
    ]
)

with available_tab:
    st.title("Available Times")
    ids: list[int] = []
    service_ids: list[int] = []
    service_names: list[str] = []
    dates: list[str] = []

    appointments = View.get_available_appointments()
    for a in appointments:
        ids.append(a.get_id())

        service_ids.append(a.get_service_id())
        service: Union[Service, None] = View.get_service_by_id(a.get_service_id())
        if service is not None:
            service_names.append(service.get_name())
        else:
            service_names.append("")

        dates.append(a.get_date().isoformat())

    df = pd.DataFrame(
        {
            "id": ids,
            "service_id": service_ids,
            "service_name": service_names,
            "date": dates,
        }
    )

    if len(appointments) > 0:
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "service_id": "Service ID",
                "service_name": "Service Name",
                "date": st.column_config.DatetimeColumn(
                    "Date",
                    format="HH:mm, DD MMM YYYY",
                ),
            },
            hide_index=True,
        )
    else:
        st.warning("There are no appointments to list.")

with scheduled_tab:
    st.title("Scheduled Appointments")
    ids = []
    client_ids: list[int] = []
    client_names: list[str] = []
    service_ids = []
    service_names = []
    dates = []

    appointments = View.get_unavailable_appointments()
    for a in appointments:
        ids.append(a.get_id())

        client_ids.append(a.get_client_id())
        client: Union[Client, None] = View.get_client_by_id(a.get_client_id())
        if client is not None:
            client_names.append(client.get_name())
        else:
            client_names.append("")

        service_ids.append(a.get_service_id())
        service = View.get_service_by_id(a.get_service_id())
        if service is not None:
            service_names.append(service.get_name())
        else:
            service_names.append("")

        dates.append(a.get_date().isoformat())

    df = pd.DataFrame(
        {
            "id": ids,
            "client_id": client_ids,
            "client_name": client_names,
            "service_id": service_ids,
            "service_name": service_names,
            "date": dates,
        }
    )

    if len(appointments) > 0:
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "client_id": "Client ID",
                "client_name": "Client Name",
                "service_id": "Service ID",
                "service_name": "Service Name",
                "date": st.column_config.DatetimeColumn(
                    "Date",
                    format="HH:mm, DD MMM YYYY",
                ),
            },
            hide_index=True,
        )
    else:
        st.warning("There are no appointments to list.")

with schedule_tab:
    st.title("Make Appointment")

    client = st.selectbox("Select the client", View.get_clients(), index=None)

    if client is None:
        st.warning("Please select a client.")

    service = st.selectbox("Select the service", View.get_services(), index=None)

    if service is None:
        st.warning("Please select a service.")

    appointment = None

    available_appointments: list[Appointment] = View.get_available_appointments()
    available_appointments = [
        a
        for a in available_appointments
        if service is not None and a.get_service_id() == service.get_id()
    ]

    available_times: list[str] = []
    for a in available_appointments:
        available_times.append(a.get_date().strftime("%H:%M, %d %b %Y"))

    chosen_time: Union[str, None] = st.selectbox(
        "Select the time to schedule", available_times, index=None
    )

    if len(available_appointments) == 0:
        st.warning("There are no available times to schedule for the selected service.")

    if chosen_time is not None:
        appointment = available_appointments[available_times.index(chosen_time)]

    if client is not None and service is not None and appointment is not None:
        if st.button("Make"):
            View.update_appointment(
                appointment.get_id(),
                client.get_id(),
                service.get_id(),
                appointment.get_date(),
                False,
            )
            st.success("Appointment made.")


with update_tab:
    st.title("Update Appointment")

    appointments = View.get_appointments()
    appointment = st.selectbox(
        "Select the appointment to update", appointments, index=None
    )

    if len(appointments) == 0:
        st.warning("There are no appointments to update.")

    if appointment is not None:
        clients: list[Client] = View.get_clients()

        client_id = appointment.get_client_id()

        if client_id >= 0:
            client = View.get_client_by_id(client_id)
        else:
            client = None

        if client is not None:
            client_idx: Union[int, None] = clients.index(client)
        else:
            client_idx = None

        available: bool = appointment.get_available()

        empty_selectbox: st.delta_generator.DeltaGenerator = st.empty()

        services: list[Service] = View.get_services()

        service = View.get_service_by_id(appointment.get_service_id())
        if service is not None:
            service_idx: Union[int, None] = services.index(service)
        else:
            service_idx = None

        service = st.selectbox(
            "Select the service for the appointment", services, index=service_idx
        )

        date = st.date_input("Date of the appointment:", value=appointment.get_date())

        available = st.checkbox("Available", value=available)

        client = empty_selectbox.selectbox(
            "Select the client for the appointment",
            clients,
            index=client_idx,
            disabled=available,
        )

        if not available and client is not None:
            client_id = client.get_id()
        else:
            client_id = -1

        if st.button("Update"):
            if (not available and client_id < 0) or service is None or not date:
                st.warning("Please fill in all fields correctly.")
            else:
                View.update_appointment(
                    appointment.get_id(),
                    client_id,
                    service.get_id(),
                    date,
                    available,
                )
                st.success("Appointment updated.")

with delete_tab:
    st.title("Delete Appointment")

    appointments = View.get_appointments()
    appointment = st.selectbox(
        "Select the appointment to delete", appointments, index=None
    )

    if len(appointments) == 0:
        st.warning("There are no appointments to delete.")

    if appointment is not None:
        st.write("You selected appointment ID:", appointment.get_id())

        a_id = appointment.get_id()

        if st.button("Delete"):
            if View.get_appointment_by_id(a_id) is None:
                st.warning("Appointment not found.")
            else:
                View.delete_appointment(a_id)
                st.success("Appointment deleted.")

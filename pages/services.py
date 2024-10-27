import streamlit as st  # type: ignore
from view import View
import pandas as pd  # type: ignore

from typing import Union
from models.service import Service


View.load_services()

st.set_page_config(
    page_title="Services",
    page_icon="👋",
)

with st.sidebar:
    st.page_link("main.py", label="Appointment System")
    st.page_link("pages/clients.py", label="Clients Manager")
    st.page_link("pages/services.py", label="Services Manager")
    st.page_link("pages/appointments.py", label="Appointments Manager")
    st.page_link("pages/open_agenda.py", label="Open Agenda")

st.header("Service Manager")

list_tab, insert_tab, update_tab, delete_tab = st.tabs(
    ["List Services", "Add Service", "Update Service", "Delete Service"]
)

with list_tab:
    st.title("List Services")
    ids: list[int] = []
    names: list[str] = []
    prices: list[str] = []
    durations: list[str] = []

    services = View.get_services()
    for c in services:
        ids.append(c.get_id())
        names.append(c.get_name())
        prices.append(f"{c.get_price():.2f}")
        durations.append(
            f"{c.get_duration()} mins"
            if c.get_duration() > 1
            else f"{c.get_duration()} min"
        )

    df = pd.DataFrame(
        {
            "id": ids,
            "name": names,
            "price": prices,
            "duration": durations,
        }
    )

    if len(services) > 0:
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "name": "Name",
                "price": "Price",
                "duration": "Duration",
            },
            hide_index=True,
        )
    else:
        st.warning("There are no services to list.")

with insert_tab:
    st.title("Add Service")
    name: str = st.text_input("Name of the service: ")
    price: float = float(st.number_input("Price of the service: "))
    duration: int = int(st.number_input("Duration of the service (in minutes): "))

    if st.button("Register"):
        if not name or not price or not duration:
            st.warning("Please fill in all fields.")
        else:
            View.insert_service(name, price, duration)
            st.success("Service registered.")

with update_tab:
    st.title("Update Service")

    services = View.get_services()
    service = st.selectbox("Select the service to update", services, index=None)

    if len(services) == 0:
        st.warning("There are no services to update.")

    if service is not None:
        name = st.text_input("Name of the service: ", value=service.get_name())
        price = float(
            st.number_input("Price of the service: ", value=service.get_price())
        )
        duration = int(
            st.number_input(
                "Duration of the service (in minutes): ", value=service.get_duration()
            )
        )

        s_id: int = service.get_id()

        if st.button("Update"):
            if not name or not price or not duration:
                st.warning("Please fill in all fields.")
            else:
                View.update_service(s_id, name, price, duration)
                st.success("Service updated.")

with delete_tab:
    st.title("Delete Service")

    services = View.get_services()
    service = st.selectbox("Select the service to delete", services, index=None)

    if len(services) == 0:
        st.warning("There are no services to delete.")

    if service is not None:
        st.write("You selected:", service.get_name())

        s_id = service.get_id()

        if st.button("Delete"):
            if View.get_service_by_id(s_id) is None:
                st.warning("Service not found.")
            else:
                View.delete_service(s_id)
                st.success("Service deleted.")

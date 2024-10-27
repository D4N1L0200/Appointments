import streamlit as st  # type: ignore
from view import View
import pandas as pd  # type: ignore

from typing import Union
from models.client import Client


View.load_clients()

st.set_page_config(
    page_title="Clients",
    page_icon="👋",
)

with st.sidebar:
    st.page_link("main.py", label="Appointment System")
    st.page_link("pages/clients.py", label="Clients Manager")
    st.page_link("pages/services.py", label="Services Manager")
    st.page_link("pages/appointments.py", label="Appointments Manager")
    st.page_link("pages/open_agenda.py", label="Open Agenda")

st.header("Client Manager")

list_tab, insert_tab, update_tab, delete_tab = st.tabs(
    ["List Clients", "Add Client", "Update Client", "Delete Client"]
)

with list_tab:
    st.title("List Clients")

    ids: list[int] = []
    names: list[str] = []
    ages: list[int] = []
    phones: list[str] = []
    cpfs: list[str] = []

    clients = View.get_clients()
    for c in clients:
        ids.append(c.get_id())
        names.append(c.get_name())
        ages.append(c.get_age())
        phones.append(c.get_phone())
        cpfs.append(c.get_cpf())

    df = pd.DataFrame(
        {
            "id": ids,
            "name": names,
            "age": ages,
            "phone": phones,
            "cpf": cpfs,
        }
    )

    if len(clients) > 0:
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "name": "Name",
                "age": "Age",
                "phone": "Phone",
                "cpf": "CPF",
            },
            hide_index=True,
        )
    else:
        st.warning("There are no clients to list.")

with insert_tab:
    st.title("Add Client")
    name: str = st.text_input("Name of the client: ")
    age: int = int(st.number_input("Age of the client: "))
    phone: str = st.text_input("Phone number of the client: ")
    cpf: str = st.text_input("CPF of the client: ")

    if st.button("Register"):
        if not name or not age or not phone or not cpf:
            st.warning("Please fill in all fields.")
        else:
            View.insert_client(name, age, phone, cpf)
            st.success("Client registered.")

with update_tab:
    st.title("Update Client")

    clients = View.get_clients()
    client = st.selectbox("Select the client to update", clients, index=None)

    if len(clients) == 0:
        st.warning("There are no clients to update.")

    if client is not None:
        name = st.text_input("Name of the client: ", value=client.get_name())
        age = int(st.number_input("Age of the client: ", value=client.get_age()))
        phone = st.text_input("Phone number of the client: ", value=client.get_phone())
        cpf = st.text_input("CPF of the client: ", value=client.get_cpf())

        c_id: int = client.get_id()

        if st.button("Update"):
            if not name or not age or not phone or not cpf:
                st.warning("Please fill in all fields.")
            else:
                View.update_client(c_id, name, age, phone, cpf)
                st.success("Client updated.")

with delete_tab:
    st.title("Delete Client")

    clients = View.get_clients()
    client = st.selectbox("Select the client to delete", clients, index=None)

    if len(clients) == 0:
        st.warning("There are no clients to delete.")

    if client is not None:
        st.write("You selected:", client.get_name())

        c_id = client.get_id()

        if st.button("Delete"):
            if View.get_client_by_id(c_id) is None:
                st.warning("Client not found.")
            else:
                View.delete_client(c_id)
                st.success("Client deleted.")

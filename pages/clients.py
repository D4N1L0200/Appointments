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

st.header("Client Manager")

list_tab, insert_tab, update_tab, delete_tab = st.tabs(
    ["List Clients", "Add Client", "Update Client", "Delete Client"]
)

with list_tab:
    st.title("List Clients")

    ids: list = []
    names: list = []
    ages: list = []
    phones: list = []
    cpfs: list = []

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

with insert_tab:
    st.title("Add Client")
    name: str = st.text_input("Name of the client: ")
    age: int = int(st.number_input("Age of the client: "))
    phone: str = st.text_input("Phone number of the client: ")
    cpf: str = st.text_input("CPF of the client: ")

    if st.button("Register"):
        View.insert_client(name, age, phone, cpf)
        st.success("Client registered.")

with update_tab:
    st.title("Update Client")

    client: Union[Client, None] = st.selectbox(
        "Select the client to update", View.get_clients(), index=None
    )

    if client is not None:
        st.write("You selected:", client.get_name())

        name = st.text_input("Name of the client: ", value=client.get_name())
        age = int(st.number_input("Age of the client: ", value=client.get_age()))
        phone = st.text_input("Phone number of the client: ", value=client.get_phone())
        cpf = st.text_input("CPF of the client: ", value=client.get_cpf())

        c_id: int = client.get_id()

        if st.button("Update"):
            View.update_client(c_id, name, age, phone, cpf)
            st.success("Client updated.")

with delete_tab:
    st.title("Delete Client")

    client = st.selectbox("Select the client to delete", View.get_clients(), index=None)

    if client is not None:
        st.write("You selected:", client.get_name())

        c_id = client.get_id()

        if st.button("Delete"):
            View.delete_client(c_id)
            st.success("Client deleted.")

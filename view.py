from models.client import Client, ClientsCRUD
from typing import Union


class View:
    @staticmethod
    def load_clients() -> None:
        ClientsCRUD.load()

    @staticmethod
    def insert_client(name: str, age: int, phone: str, cpf: str) -> None:
        obj = Client(0, name, age, phone, cpf)
        ClientsCRUD.insert(obj)

    @staticmethod
    def get_clients() -> list[Client]:
        return ClientsCRUD.get_clients()

    @staticmethod
    def get_client_by_id(c_id: int) -> Union[Client, None]:
        return ClientsCRUD.get_client_by_id(c_id)

    @staticmethod
    def update_client(c_id: int, name: str, age: int, phone: str, cpf: str) -> None:
        ClientsCRUD.update(c_id, name, age, phone, cpf)

    @staticmethod
    def delete_client(c_id: int) -> None:
        ClientsCRUD.delete(c_id)

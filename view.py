from models.client import Client, ClientsCRUD
from models.service import Service, ServicesCRUD
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

    @staticmethod
    def load_services() -> None:
        ServicesCRUD.load()

    @staticmethod
    def insert_service(name: str, price: float, duration: int) -> None:
        obj = Service(0, name, price, duration)
        ServicesCRUD.insert(obj)

    @staticmethod
    def get_services() -> list[Service]:
        return ServicesCRUD.get_services()

    @staticmethod
    def get_service_by_id(c_id: int) -> Union[Service, None]:
        return ServicesCRUD.get_service_by_id(c_id)

    @staticmethod
    def update_service(c_id: int, name: str, price: float, duration: int) -> None:
        ServicesCRUD.update(c_id, name, price, duration)

    @staticmethod
    def delete_service(c_id: int) -> None:
        ServicesCRUD.delete(c_id)

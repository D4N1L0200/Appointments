from models.client import Client, ClientsCRUD
from models.service import Service, ServicesCRUD
from models.appointment import Appointment, AppointmentsCRUD
from typing import Union
from datetime import datetime, time


class View:
    # Clients
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

    # Services
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

    # Appointments
    @staticmethod
    def load_appointments() -> None:
        AppointmentsCRUD.load()

    @staticmethod
    def insert_appointment(
        c_id: int, s_id: int, date: datetime, available: bool
    ) -> None:
        obj = Appointment(0, c_id, s_id, date, available)
        AppointmentsCRUD.insert(obj)

    @staticmethod
    def get_appointments() -> list[Appointment]:
        return AppointmentsCRUD.get_appointments()

    @staticmethod
    def get_available_appointments() -> list[Appointment]:
        return [a for a in AppointmentsCRUD.get_appointments() if a.get_available()]

    @staticmethod
    def get_unavailable_appointments() -> list[Appointment]:
        return [a for a in AppointmentsCRUD.get_appointments() if not a.get_available()]

    @staticmethod
    def get_appointment_by_id(a_id: int) -> Union[Appointment, None]:
        return AppointmentsCRUD.get_appointment_by_id(a_id)

    @staticmethod
    def update_appointment(
        a_id: int, c_id: int, s_id: int, date, available: bool
    ) -> None:
        AppointmentsCRUD.update(a_id, c_id, s_id, date, available)

    @staticmethod
    def delete_appointment(a_id: int) -> None:
        AppointmentsCRUD.delete(a_id)

    @staticmethod
    def open_agenda(
        s_id: int, date, start_time: time, end_time: time, spacing: time
    ) -> int:
        return AppointmentsCRUD.open_agenda(s_id, date, start_time, end_time, spacing)

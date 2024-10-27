import json
from datetime import datetime, time, timedelta
from typing import Union
from models.service import Service, ServicesCRUD


class Appointment:
    def __init__(
        self, a_id: int, c_id: int, s_id: int, date: datetime, available: bool
    ) -> None:
        self.__id: int = 0
        self.__client_id: int = 0
        self.__service_id: int = 0
        self.__date: datetime = datetime.now()
        self.__available: bool = True

        self.set_id(a_id)
        self.set_client_id(c_id)
        self.set_service_id(s_id)
        self.set_date(date)
        self.set_available(available)

    def set_id(self, a_id: int) -> None:
        if isinstance(a_id, int) and a_id >= 0:
            self.__id = a_id
        else:
            raise ValueError("Id has to be a positive integer")

    def get_id(self) -> int:
        return self.__id

    def set_client_id(self, c_id: int) -> None:
        if isinstance(c_id, int):
            self.__client_id = c_id
        else:
            raise ValueError("Id has to be an integer")

    def get_client_id(self) -> int:
        return self.__client_id

    def set_service_id(self, s_id: int) -> None:
        if isinstance(s_id, int) and s_id >= 0:
            self.__service_id = s_id
        else:
            raise ValueError("Id has to be a positive integer")

    def get_service_id(self) -> int:
        return self.__service_id

    def set_date(self, date) -> None:
        if date is not None:
            self.__date = date
        else:
            raise ValueError("Date has to be a datetime")

    def get_date(self) -> datetime:
        return self.__date

    def set_available(self, available: bool) -> None:
        if isinstance(available, bool):
            self.__available = available
        else:
            raise ValueError("Available has to be a boolean")

    def get_available(self) -> bool:
        return self.__available

    def __str__(self) -> str:
        return f"Id: {self.get_id()} - Client: {self.get_client_id()} - Service: {self.get_service_id()} - Date: {self.get_date()} - Available: {self.get_available()}"


class AppointmentsCRUD:
    appointments: list[Appointment] = []

    @classmethod
    def save(cls) -> None:
        data = []
        for a in cls.appointments:
            data.append(
                {
                    "id": a.get_id(),
                    "client_id": a.get_client_id(),
                    "service_id": a.get_service_id(),
                    "date": a.get_date().isoformat(),
                    "available": a.get_available(),
                }
            )
        with open("data/appointments.json", mode="w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls) -> None:
        cls.appointments = []
        try:
            with open("data/appointments.json", mode="r") as f:
                data = json.load(f)
                for a in data:
                    cls.appointments.append(
                        Appointment(
                            a["id"],
                            a["client_id"],
                            a["service_id"],
                            datetime.fromisoformat(a["date"]),
                            a["available"],
                        )
                    )
        except FileNotFoundError:
            pass

    @classmethod
    def insert(cls, obj: Appointment) -> None:
        if not isinstance(obj, Appointment):
            raise TypeError("Object must be of type Appointment")

        ids: list[int] = [a.get_id() for a in cls.appointments]
        ids.sort()
        if len(ids) == 0:
            obj.set_id(0)
        else:
            for i in range(len(ids)):
                if ids[i] != i:
                    obj.set_id(i)
                    break
            else:
                obj.set_id(len(ids))
        cls.appointments.append(obj)
        cls.appointments.sort(key=lambda a: a.get_id())

        cls.save()

    @classmethod
    def get_appointments(cls) -> list[Appointment]:
        return cls.appointments

    @classmethod
    def get_appointment_by_id(cls, a_id: int) -> Union[Appointment, None]:
        if not isinstance(a_id, int) or a_id < 0:
            raise ValueError("Id has to be a positive integer")

        for a in cls.appointments:
            if a_id == a.get_id():
                return a
        else:
            return None

    @classmethod
    def update(cls, a_id: int, c_id: int, s_id: int, date, available: bool) -> None:
        if not isinstance(a_id, int) or a_id < 0:
            raise ValueError("Id has to be a positive integer")

        if not isinstance(c_id, int) or c_id < 0:
            raise ValueError("Id has to be a positive integer")

        if not isinstance(s_id, int) or s_id < 0:
            raise ValueError("Id has to be a positive integer")

        if not isinstance(available, bool):
            raise ValueError("Available has to be a boolean")

        a: Union[Appointment, None] = cls.get_appointment_by_id(a_id)
        if a is not None:
            a.set_client_id(c_id)
            a.set_service_id(s_id)
            a.set_date(date)
            a.set_available(available)
            cls.save()

    @classmethod
    def delete(cls, a_id: int) -> None:
        if not isinstance(a_id, int) or a_id < 0:
            raise ValueError("Id has to be a positive integer")

        for a in cls.appointments:
            if a_id == a.get_id():
                cls.appointments.remove(a)
                cls.save()

    @classmethod
    def open_agenda(
        cls, s_id: int, date, start_time: time, end_time: time, spacing: time
    ) -> int:
        if not isinstance(s_id, int):
            raise ValueError("Id has to be an integer")

        if not isinstance(start_time, time):
            raise ValueError("Start time has to be a time")

        if not isinstance(end_time, time):
            raise ValueError("End time has to be a time")

        if not isinstance(spacing, time):
            raise ValueError("Spacing has to be a time")

        start_dt: datetime = datetime.combine(date, start_time)
        end_time_dt: datetime = datetime.combine(date, end_time)
        spacing_td: timedelta = timedelta(hours=spacing.hour, minutes=spacing.minute)
        count: int = 0

        service: Union[Service, None] = ServicesCRUD.get_service_by_id(s_id)

        if service is None:
            raise ValueError("Service not found")

        spacing_td += timedelta(minutes=service.get_duration())

        while True:
            if start_dt + spacing_td > end_time_dt:
                break
            AppointmentsCRUD.insert(Appointment(0, -1, s_id, start_dt, True))
            count += 1
            start_dt += spacing_td

        return count

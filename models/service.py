import json
from typing import Union


class Service:
    def __init__(self, s_id: int, name: str, price: float, duration: int) -> None:
        self.__id: int = 0
        self.__name: str = ""
        self.__price: float = 0.0
        self.__duration: int = 0

        self.set_id(s_id)
        self.set_name(name)
        self.set_price(price)
        self.set_duration(duration)

    def set_id(self, c_id: int) -> None:
        if c_id >= 0:
            self.__id = c_id
        else:
            raise ValueError("Id has to be a positive number")

    def get_id(self) -> int:
        return self.__id

    def set_name(self, name: str) -> None:
        if name:
            self.__name = name
        else:
            raise ValueError("Name can't be empty")

    def get_name(self) -> str:
        return self.__name

    def set_price(self, price: float) -> None:
        if price > 0:
            self.__price = price
        else:
            raise ValueError("Price has to be a positive number")

    def get_price(self) -> float:
        return self.__price

    def set_duration(self, duration: int) -> None:
        if duration > 0:
            self.__duration = duration
        else:
            raise ValueError("Duration has to be a positive number")

    def get_duration(self) -> int:
        return self.__duration

    def __str__(self) -> str:
        return f"Id: {self.get_id()} - Name: {self.get_name()} - Price: {self.get_price()} - Duration: {self.get_duration()}"


class ServicesCRUD:
    services: list[Service] = []

    @classmethod
    def save(cls) -> None:
        data = []
        for s in cls.services:
            data.append(
                {
                    "id": s.get_id(),
                    "name": s.get_name(),
                    "price": s.get_price(),
                    "duration": s.get_duration(),
                }
            )
        with open("data/services.json", mode="w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls) -> None:
        cls.services = []
        try:
            with open("data/services.json", mode="r") as f:
                data = json.load(f)
                for s in data:
                    cls.services.append(
                        Service(
                            s["id"],
                            s["name"],
                            s["price"],
                            s["duration"],
                        )
                    )
        except FileNotFoundError:
            pass

    @classmethod
    def insert(cls, obj: Service) -> None:
        ids: list[int] = [s.get_id() for s in cls.services]
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
        cls.services.append(obj)
        cls.services.sort(key=lambda s: s.get_id())

        cls.save()

    @classmethod
    def get_services(cls) -> list[Service]:
        return cls.services

    @classmethod
    def get_service_by_id(cls, s_id: int) -> Union[Service, None]:
        for s in cls.services:
            if s_id == s.get_id():
                return s
        else:
            return None

    @classmethod
    def update(cls, s_id: int, name: str, price: float, duration: int) -> None:
        s: Union[Service, None] = cls.get_service_by_id(s_id)
        if s is not None:
            s.set_name(name)
            s.set_price(price)
            s.set_duration(duration)
            cls.save()

    @classmethod
    def delete(cls, s_id: int) -> None:
        for s in cls.services:
            if s_id == s.get_id():
                cls.services.remove(s)
                cls.save()

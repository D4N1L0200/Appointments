import json
from typing import Union


class Client:
    def __init__(self, c_id: int, name: str, age: int, phone: str, cpf: str) -> None:
        self.__id: int = 0
        self.__name: str = ""
        self.__age: int = 0
        self.__phone: str = ""
        self.__cpf: str = ""

        self.set_id(c_id)
        self.set_name(name)
        self.set_age(age)
        self.set_phone(phone)
        self.set_cpf(cpf)

    def set_id(self, c_id: int) -> None:
        if isinstance(c_id, int) and c_id >= 0:
            self.__id = c_id
        else:
            raise ValueError("Id has to be a positive integer")

    def get_id(self) -> int:
        return self.__id

    def set_name(self, name: str) -> None:
        if isinstance(name, str) and name:
            self.__name = name
        else:
            raise ValueError("Name has to be a string and can't be empty")

    def get_name(self) -> str:
        return self.__name

    def set_phone(self, phone: str) -> None:
        if isinstance(phone, str) and phone:
            self.__phone = phone
        else:
            raise ValueError("Phone has to be a string and can't be empty")

    def get_phone(self) -> str:
        return self.__phone

    def set_cpf(self, cpf: str) -> None:
        if isinstance(cpf, str) and cpf:
            self.__cpf = cpf
        else:
            raise ValueError("CPF has to be a string and can't be empty")

    def get_cpf(self) -> str:
        return self.__cpf

    def set_age(self, age: int) -> None:
        if isinstance(age, int) and age >= 0:
            self.__age = age
        else:
            raise ValueError("Age has to be a positive integer")

    def get_age(self) -> int:
        return self.__age

    def __str__(self) -> str:
        return f"ID: {self.__id} - Name: {self.__name} - Age: {self.__age} - Phone: {self.__phone} - CPF: {self.__cpf}"


class ClientsCRUD:
    clients: list[Client] = []

    @classmethod
    def save(cls) -> None:
        data = []
        for c in cls.clients:
            data.append(
                {
                    "id": c.get_id(),
                    "name": c.get_name(),
                    "age": c.get_age(),
                    "phone": c.get_phone(),
                    "cpf": c.get_cpf(),
                }
            )
        with open("data/clients.json", mode="w") as f:
            json.dump(data, f)

    @classmethod
    def load(cls) -> None:
        cls.clients = []
        try:
            with open("data/clients.json", mode="r") as f:
                data = json.load(f)
                for c in data:
                    cls.clients.append(
                        Client(
                            c["id"],
                            c["name"],
                            c["age"],
                            c["phone"],
                            c["cpf"],
                        )
                    )
        except FileNotFoundError:
            pass

    @classmethod
    def insert(cls, obj: Client) -> None:
        if not isinstance(obj, Client):
            raise TypeError("Object must be of type Client")

        ids: list[int] = [c.get_id() for c in cls.clients]
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
        cls.clients.append(obj)
        cls.clients.sort(key=lambda c: c.get_id())

        cls.save()

    @classmethod
    def get_clients(cls) -> list[Client]:
        return cls.clients

    @classmethod
    def get_client_by_id(cls, c_id: int) -> Union[Client, None]:
        if not isinstance(c_id, int) or c_id < 0:
            raise ValueError("Id has to be a positive integer")

        for c in cls.clients:
            if c_id == c.get_id():
                return c
        else:
            return None

    @classmethod
    def update(cls, c_id: int, name: str, age: int, phone: str, cpf: str) -> None:
        if not isinstance(c_id, int) or c_id < 0:
            raise ValueError("Id has to be a positive integer")

        if not isinstance(name, str) or not name:
            raise ValueError("Name has to be a string and can't be empty")

        if not isinstance(age, int) or age < 0:
            raise ValueError("Age has to be a positive integer")

        if not isinstance(phone, str) or not phone:
            raise ValueError("Phone has to be a string and can't be empty")

        if not isinstance(cpf, str) or not cpf:
            raise ValueError("CPF has to be a string and can't be empty")

        c: Union[Client, None] = cls.get_client_by_id(c_id)
        if c is not None:
            c.set_name(name)
            c.set_age(age)
            c.set_phone(phone)
            c.set_cpf(cpf)
            cls.save()

    @classmethod
    def delete(cls, c_id: int) -> None:
        if not isinstance(c_id, int) or c_id < 0:
            raise ValueError("Id has to be a positive integer")

        for c in cls.clients:
            if c_id == c.get_id():
                cls.clients.remove(c)
                cls.save()

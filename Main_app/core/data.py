from dataclasses import dataclass


@dataclass
class Reservation:
    id: int | None
    name: str
    number : str
    room_type : str
    check_in: str
    check_out: str


@dataclass
class Room:
    room_id: int
    room_type : str
    price : int
    status : str

@dataclass
class Logins:
    user_id: int
    user_name: str
    password: str





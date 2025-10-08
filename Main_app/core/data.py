from dataclasses import dataclass

@dataclass
class Reservation:
    id: int | None
    name: str
    number: str
    room_type: str
    check_in: str
    check_out: str
    price : int


from dataclasses import dataclass


@dataclass
class Reservation:
    id: int | None
    name: str
    number : str
    room_type : str
    check_in: str
    check_out: str
    status: str
    price: int

@dataclass
class Room:
    room_id: int
    room_type : str
    price : int
    availability : str

    # @property
    # def price_display(self) -> str:
    #     return f"₱{self.price_cents/100:,.2f}"

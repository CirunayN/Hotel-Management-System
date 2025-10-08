from Main_app.core.data import Reservation
from .repo import ReservationItem

class MainFunc:
    def __init__(self, repo: ReservationItem):
        self.repo = repo

    def validate(self, data: Reservation):
        if not data.name.strip():
            raise ValueError("Name is required")
        if not data.number.strip():
            raise ValueError("Number is required")

    def list(self):
        return self.repo.get_list()

    def create(self, name: str, number: str, room_type: str, check_in: str, check_out: str,price: float) -> Reservation:
        data = Reservation(id=None, name=name, number=number, room_type=room_type, check_in=check_in, check_out=check_out,price=price)
        self.validate(data)
        return self.repo.repo_add(data)

    def update(self, data: Reservation) -> Reservation:
        self.validate(data)
        return self.repo.repo_update(data)

    def delete(self, id_: int) -> None:
        self.repo.repo_delete(id_)

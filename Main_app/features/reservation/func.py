from Main_app.core.data import Reservation
from .repo import ReservationItem


class MainFunc:
    def __init__(self, repo: ReservationItem):
        self.repo = repo

    # Basic business rules
    def validate(self, data: Reservation):
        if not data.name.strip():
            raise ValueError("Name is required")
        if not data.room_type.strip():
            raise ValueError("Room is required")
        if not data.number.strip():
            raise ValueError("Number is required")
        if not data.check_in.strip():
            raise ValueError("Checkin is required")
        if not data.check_out.strip():
            raise ValueError("Checkout is required")

    def list(self):
        return self.repo.get_list()

    def create(self, name: str,number : str, room_type: str, check_in: str, check_out: str,) -> Reservation:
        data = Reservation(id=None, name=name,number=number, room_type=room_type, check_in=check_in, check_out=check_out)
        self.validate(data)
        return self.repo.repo_add(data)

    def update(self, data: Reservation) -> Reservation:
        self.validate(data)
        return self.repo.repo_update(data)

    def delete(self, id_: int) -> None:
        self.repo.repo_delete(id_)
    #
    # def search(self, data : Reservation):
    #     id = data.id




from .data import Reservation

class ReservationItem():
    def __init__(self, conn):
        self.conn = conn
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS reservation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number TEXT NOT NULL,
        room_type TEXT NOT NULL,
        checkin TEXT NOT NULL,
        checkout TEXT NOT NULL,
        status TEXT NOT NULL,
        price INTEGER NOT NULL
        )
        """)
        # self.conn.execute("""
        # CREATE TABLE IF NOT EXISTS app_data
        # (
        #     id
        #     INTEGER
        #     PRIMARY
        #     KEY
        #     AUTOINCREMENT,
        #     name
        #     TEXT
        #     NOT
        #     NULL,
        #     number
        #     TEXT
        #     NOT
        #     NULL,
        #     room
        #     TEXT,
        #     checkin
        #     TEXT,
        #     checkout
        #     TEXT,
        #     status
        #     TEXT,
        #     price
        #     INTEGER
        #     NOT
        #     NULL,
        # )
        # """)


    def get_list(self) -> list[Reservation]:
        stored: list[Reservation] = []
        rows = self.conn.execute(
            "SELECT id, name,number, room_type, checkin, checkout,status,price FROM reservation ORDER BY id DESC"
        ).fetchall()

        if not rows:
            return []

        for r in rows:
            item = Reservation(*r)
            stored.append(item)

        return stored


    def get_data(self, id_: int) -> Reservation | None:
        row = self.conn.execute(
            "SELECT id, name,number, room_type, checkin, checkout, status,price FROM reservation WHERE id=?",
            (id_,),
        ).fetchone()
        return Reservation(*row) if row else None



    def repo_add(self, data: Reservation) -> Reservation:
        cur = self.conn.execute(
            "INSERT INTO reservation(name,number,room_type,checkin,checkout,status,price) VALUES (?,?,?,?,?,?,?)",
            (data.name,data.number, data.room_type, data.check_in, data.check_out,data.status,data.price),
        )
        self.conn.commit()
        return Reservation(
            id=cur.lastrowid,
            name=data.name,
            number=data.number,
            room_type=data.room_type,
            check_in=data.check_in,
            check_out=data.check_out,
            status=data.status,
            price=data.price,
        )

    def repo_update(self, data: Reservation) -> Reservation:
        assert data.id is not None
        self.conn.execute(
            "UPDATE reservation SET name=?,number=?, room_type=?, checkin=?, checkout=?, status=?, price=? WHERE id=?",
            (data.name,data.number, data.room_type, data.check_in, data.check_out,data.status,data.price),
        )
        self.conn.commit()
        return data

    def repo_delete(self, id_: int) -> None:
        self.conn.execute("DELETE FROM reservation WHERE id=?", (id_,))
        self.conn.commit()






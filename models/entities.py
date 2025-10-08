from dataclasses import dataclass

@dataclass
class Flight:
    id: int
    flight_number: str
    departure_id: str
    arrival_id: str
    departure_time: str
    arrival_time: str
    status: str


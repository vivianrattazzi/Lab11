import datetime
from dataclasses import dataclass
@dataclass
class Connessione:
    p1: str
    p2: str
    peso: int




    def __str__(self):
        return f"Arco da {self.p1} a {self.p2} con peso {self.peso}"

    def __hash__(self):
        return hash((self.p1, self.p2))

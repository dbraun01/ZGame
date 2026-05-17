from typing import List, Tuple
from entities.actor import Actor


class Survivor(Actor):
    def __init__(self, name: str, start_pos: Tuple[int, int, int, int]) -> None:
        # Dans la 2e Édition, un survivant commence généralement avec 2 PV
        super().__init__(name, health=3, start_pos=start_pos, actions=3)

        self.adrenaline: int = 0
        self.inventory: List[str] = []  # On pourra créer une classe Item plus tard
        self.skills: List[str] = ["Blue Skill"]  # Compétence de départ

    def gain_adrenaline(self, points: int) -> None:
        self.adrenaline += points
        # La logique de montée de niveau (Jaune, Orange, Rouge) viendra ici

    def can_open_door(self) -> bool:
        return True

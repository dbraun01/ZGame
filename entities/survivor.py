from typing import List, Tuple
from entities.actor import Actor

class Survivor(Actor):
    def __init__(self, name: str, start_pos: Tuple[int, int, int, int]) -> None:
        # Dans la 2e Édition, un survivant commence généralement avec 2 PV
        super().__init__(name, health=2, start_pos=start_pos)
        
        self.actions_per_turn: int = 3
        self.remaining_actions: int = 3
        self.adrenaline: int = 0
        self.inventory: List[str] = [] # On pourra créer une classe Item plus tard
        self.skills: List[str] = ["Blue Skill"] # Compétence de départ

    def gain_adrenaline(self, points: int) -> None:
        self.adrenaline += points
        # La logique de montée de niveau (Jaune, Orange, Rouge) viendra ici

    def reset_actions(self) -> None:
        self.remaining_actions = self.actions_per_turn
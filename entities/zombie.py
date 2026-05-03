from typing import Tuple
from entities.actor import Actor

class Zombie(Actor):
    def __init__(self, zombie_type: str, start_pos: Tuple[int, int, int, int]) -> None:
        # Configuration selon le type
        stats = {
            "WALKER": {"health": 1, "actions": 1},
            "RUNNER": {"health": 1, "actions": 2},
            "FATTY":  {"health": 2, "actions": 1},
            "ABOM":   {"health": 3, "actions": 1}
        }
        
        type_data = stats.get(zombie_type, stats["WALKER"])
        super().__init__(zombie_type, health=type_data["health"], start_pos=start_pos)
        
        self.type: str = zombie_type
        self.actions: int = type_data["actions"]
from typing import Tuple, List

class Actor:
    def __init__(self, name: str, health: int, start_pos: Tuple[int, int, int, int]) -> None:
        """
        start_pos: (tile_x, tile_y, zone_x, zone_y)
        """
        self.name: str = name
        self.max_health: int = health
        self.current_health: int = health
        
        # Position décomposée pour correspondre à notre structure modulaire
        self.tile_coords: List[int] = [start_pos[0], start_pos[1]]
        self.zone_coords: List[int] = [start_pos[2], start_pos[3]]

    def take_damage(self, amount: int) -> None:
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def move(self, direction: str) -> None:
        if direction == "N":
            self.zone_coords[1] -= 1
        elif direction == "S":
            self.zone_coords[1] += 1
        elif direction == "E":
            self.zone_coords[0] += 1
        elif direction == "W":
            self.zone_coords[0] -= 1

        # Gestion du changement de Tuile (grille 3x3 zones par tuile)
        if self.zone_coords[0] < 0:
            self.tile_coords[0] -= 1
            self.zone_coords[0] = 2
        elif self.zone_coords[0] > 2:
            self.tile_coords[0] += 1
            self.zone_coords[0] = 0

        if self.zone_coords[1] < 0:
            self.tile_coords[1] -= 1
            self.zone_coords[1] = 2
        elif self.zone_coords[1] > 2:
            self.tile_coords[1] += 1
            self.zone_coords[1] = 0
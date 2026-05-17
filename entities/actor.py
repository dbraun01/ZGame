from typing import Tuple, List


class Actor:
    def __init__(
        self,
        name: str,
        health: int,
        start_pos: Tuple[int, int, int, int],
        actions: int = 1,
    ) -> None:
        """
        start_pos: (tile_x, tile_y, zone_x, zone_y)
        """
        self.name: str = name
        self.max_health = health
        self.current_health = health
        self.actions = actions
        self.reset_actions()

        # Position décomposée pour correspondre à notre structure modulaire
        self.tile_coords: List[int] = [start_pos[0], start_pos[1]]
        self.zone_coords: List[int] = [start_pos[2], start_pos[3]]

    @property
    def x(self) -> int:
        """Calcule la coordonnée globale X (utilisée par le render et l'engine)."""
        return self.tile_coords[0] * 3 + self.zone_coords[0]

    @x.setter
    def x(self, value: int):
        # divmod(7, 3) retourne (2, 1) -> Tuile 2, Zone 1
        self.tile_coords[0], self.zone_coords[0] = divmod(value, 3)

    @property
    def y(self) -> int:
        """Calcule la coordonnée globale Y."""
        return self.tile_coords[1] * 3 + self.zone_coords[1]

    @y.setter
    def y(self, value: int):
        # divmod(7, 3) retourne (2, 1) -> Tuile 2, Zone 1
        self.tile_coords[1], self.zone_coords[1] = divmod(value, 3)

    def set_global_position(self, gx: int, gy: int):
        """Met à jour les coordonnées décomposées à partir d'une position globale."""
        self.tile_coords[0], self.zone_coords[0] = divmod(gx, 3)
        self.tile_coords[1], self.zone_coords[1] = divmod(gy, 3)

    def take_damage(self, amount: int) -> None:
        self.current_health = max(0, self.current_health - amount)

    def reset_actions(self) -> None:
        self.remaining_actions = self.actions

    def can_open_door(self) -> bool:
        return False

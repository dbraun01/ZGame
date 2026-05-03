from typing import List, Dict, Optional, Union

class Door:
    def __init__(self, state: str = "CLOSED") -> None:
        # state doit être une chaîne de caractères : "OPEN", "CLOSED", ou "LOCKED"
        self.state: str = state

    def toggle(self) -> None:
        if self.state == "CLOSED":
            self.state = "OPEN"
        elif self.state == "OPEN":
            self.state = "CLOSED"

class Zone:
    def __init__(self, zone_type: str) -> None:
        # zone_type doit être "STREET" ou "BUILDING"
        self.type: str = zone_type
        
        # boundaries est un dictionnaire. 
        # Les clés sont des chaînes de caractères ("N", "S", "E", "W").
        # Les valeurs peuvent être de 3 types : l'objet Door, la chaîne "WALL", ou None (vide).
        self.boundaries: Dict[str, Union['Door', str, None]] = {
            "N": None, 
            "S": None, 
            "E": None, 
            "W": None
        }

class Tile:
    def __init__(self, layout: List[List[Zone]]) -> None:
        # layout est explicitement une liste contenant des listes, qui elles-mêmes contiennent des objets Zone.
        # Cela correspond parfaitement à notre grille de 3x3 zones de la 2e Édition.
        self.grid: List[List[Zone]] = layout
        self.size: int = len(layout)

class Board:
    def __init__(self) -> None:
        # tiles_map est une grille 2D d'objets Tile.
        self.tiles_map: List[List['Tile']] = []
        
    def add_tile_row(self, row_of_tiles: List['Tile']) -> None:
        # On ajoute une rangée complète de tuiles au plateau
        self.tiles_map.append(row_of_tiles)
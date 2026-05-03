from core.board import Board, Door
from core.movement import can_move
from entities.survivor import Survivor
from entities.actor import Actor


class GameEngine:
    def __init__(self, board: Board):
        self.board = board

    def attempt_move(self, actor: Actor, direction: str) -> bool:
        """
        Tente de déplacer un acteur. Vérifie les actions, les murs et les portes.
        """
        # 1. Si c'est un survivant, a-t-il assez d'actions ?
        if isinstance(actor, Survivor):
            if actor.remaining_actions <= 0:
                print(f"{actor.name} n'a plus d'actions !")
                return False

        # 2. Récupérer la zone actuelle
        current_tile = self.board.tiles_map[actor.tile_coords[1]][actor.tile_coords[0]]
        current_zone = current_tile.grid[actor.zone_coords[1]][actor.zone_coords[0]]

        # 3. Vérifier les bordures (Mur, Porte fermée, etc.)
        if can_move(current_zone, direction):
            actor.move(direction)
            if isinstance(actor, Survivor):
                actor.remaining_actions -= 1
            return True

        print("Mouvement impossible : Mur ou porte fermée.")
        return False

    def interact_door(self, actor: Actor, target_direction: str = None) -> bool:
        """
        Cherche une porte fermée dans la zone actuelle.
        Si plusieurs portes sont présentes, nécessite target_direction.
        """
        # 1. Vérification des actions
        if isinstance(actor, Survivor) and actor.remaining_actions <= 0:
            print(f"{actor.name} est épuisé et ne peut pas ouvrir de porte.")
            return False

        # 2. Récupération de la zone actuelle
        t_x, t_y = actor.tile_coords
        z_x, z_y = actor.zone_coords
        current_zone = self.board.tiles_map[t_y][t_x].grid[z_y][z_x]

        # 3. Lister toutes les portes fermées autour de l'acteur
        closed_doors = {}
        for direction, boundary in current_zone.boundaries.items():
            if isinstance(boundary, Door) and boundary.state == "CLOSED":
                closed_doors[direction] = boundary

        # 4. Traitement selon le nombre de portes trouvées
        if not closed_doors:
            print("Il n'y a aucune porte fermée à proximité.")
            return False

        door_to_open = None

        if len(closed_doors) == 1:
            # S'il n'y a qu'une seule porte, on l'ouvre automatiquement, direction précisée ou non
            direction, door_to_open = list(closed_doors.items())[0]
            print(f"Ouverture automatique de la seule porte disponible ({direction}).")
        else:
            # S'il y a plusieurs portes, le joueur DOIT préciser la direction
            if target_direction in closed_doors:
                door_to_open = closed_doors[target_direction]
            else:
                available_dirs = ", ".join(closed_doors.keys())
                print(
                    f"Plusieurs portes fermées ({available_dirs}). Maintenez une flèche + Espace pour choisir !"
                )
                return False

        # 5. Ouverture effective de la porte et consommation de l'action
        if door_to_open:
            door_to_open.state = "OPEN"
            if isinstance(actor, Survivor):
                actor.remaining_actions -= 1
            print(f"Porte ouverte ! PA restants : {actor.remaining_actions}")
            return True

        return False

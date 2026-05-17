from core.board import Board, Door, Border

# from core.movement import can_move
from entities.survivor import Survivor
from entities.actor import Actor


class GameEngine:
    def __init__(self, board: Board):
        self.board = board

    def attempt_move(self, actor: Actor, dx: int, dy: int) -> bool:
        """Tente de déplacer un acteur et retourne True si réussi."""
        current_gx, current_gy = actor.x, actor.y
        target_gx, target_gy = current_gx + dx, current_gy + dy

        # 1. Vérifier si on sort de la carte
        tile_size = self.board.tiles[0][0].size
        if not (
            0 <= target_gx < self.board.cols * tile_size
            and 0 <= target_gy < self.board.rows * tile_size
        ):
            print("on sort de la carte")
            return False

        # 2. Vérifier les bordures physiques (Murs, Portes fermées)
        boundary = self.board.get_boundary(
            (current_gx, current_gy), (target_gx, target_gy)
        )
        if boundary == Border.WALL or (
            isinstance(boundary, Door) and not boundary.is_open
        ):
            print("obstacle")
            return False  # Obstacle infranchissable

        # 3. Vérifier la fusion logique pour le coût en PA
        current_zone = self.board.get_global_zone(current_gx, current_gy)
        target_zone = self.board.get_global_zone(target_gx, target_gy)

        print(f"current Zone: {current_zone.id}")
        print(f"current Zone: {target_zone.id}")

        # Si c'est la même instance d'objet en mémoire, le mouvement est gratuit
        action_cost = 0 if current_zone is target_zone else 1

        if getattr(actor, "remaining_actions", 0) >= action_cost:
            actor.remaining_actions -= action_cost
            actor.x, actor.y = target_gx, target_gy
            return True
        else:
            return False  # Pas assez de PA

    def interact_door(self, actor: Actor, door: Door = None) -> bool:
        """
        Interagit avec une porte.
        Si 'door' est fourni, tente de l'ouvrir.
        Sinon, cherche une porte unique dans la zone actuelle (ouverture auto).
        """
        # 1. Vérification des actions (uniquement pour les Survivants)
        if isinstance(actor, Survivor) and actor.can_open_door():
            print(f"{actor.name} n'a plus de points d'action.")
            return False

        # 2. Si aucune porte n'est précisée, on cherche autour de l'acteur
        if door is None:
            # On utilise les propriétés globales x et y de l'acteur
            gx, gy = actor.x, actor.y

            # On liste les 4 cases adjacentes (Nord, Sud, Est, Ouest)
            neighbors = [(gx, gy - 1), (gx, gy + 1), (gx + 1, gy), (gx - 1, gy)]
            closed_doors = []

            # Calcul des limites du plateau pour éviter les erreurs "Out of bounds"
            tile_size = self.board.tiles[0][0].size
            max_x = self.board.cols * tile_size
            max_y = self.board.rows * tile_size

            for nx, ny in neighbors:
                # On s'assure que la case voisine est bien sur le plateau
                if 0 <= nx < max_x and 0 <= ny < max_y:
                    # On interroge la couche physique (le Board)
                    boundary = self.board.get_boundary((gx, gy), (nx, ny))
                    if isinstance(boundary, Door) and not boundary.is_open:
                        closed_doors.append(boundary)

            if not closed_doors:
                print("Aucune porte fermée à proximité.")
                return False

            if len(closed_doors) == 1:
                door = closed_doors[0]
                print("Ouverture automatique de la seule porte disponible.")
            else:
                print(
                    f"Il y a {len(closed_doors)} portes fermées ici. Laquelle ouvrir ?"
                )
                return False

        # 3. Ouverture effective
        if door and not door.is_open:
            door.open()  # Utilise la méthode .open() de ta classe Door

            if isinstance(actor, Survivor):
                actor.remaining_actions -= 1

            print(
                f"Porte ouverte par {actor.name} ! (PA restants : {actor.remaining_actions})"
            )
            return True

        return False

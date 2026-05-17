import pygame
from core.board import Board, Door, Border
from entities.actor import Actor

TILE_PIXEL_SIZE: int = 300
ZONE_PIXEL_SIZE: int = 100


def draw_board(screen: pygame.Surface, board: Board) -> None:
    # 1. Dessin du sol (Couleurs)
    for gx, gy, zone in board.iter_global_zones():
        px, py = gx * ZONE_PIXEL_SIZE, gy * ZONE_PIXEL_SIZE
        color = (80, 80, 80) if zone.type == "STREET" else (120, 60, 30)
        pygame.draw.rect(
            screen, color, pygame.Rect(px, py, ZONE_PIXEL_SIZE, ZONE_PIXEL_SIZE)
        )

    # 2. Dessin de la grille intelligente (Fusion Visuelle)
    max_x = board.cols * board.tiles[0][0].size
    max_y = board.rows * board.tiles[0][0].size

    for gx, gy, zone in board.iter_global_zones():
        px, py = gx * ZONE_PIXEL_SIZE, gy * ZONE_PIXEL_SIZE

        # Ligne Droite (Est) : Ne se dessine que si la zone de droite est différente
        if gx < max_x - 1:
            if zone is not board.get_global_zone(gx + 1, gy):
                pygame.draw.line(
                    screen,
                    (180, 180, 180),
                    (px + ZONE_PIXEL_SIZE, py),
                    (px + ZONE_PIXEL_SIZE, py + ZONE_PIXEL_SIZE),
                    1,
                )

        # Ligne Bas (Sud) : Ne se dessine que si la zone en bas est différente
        if gy < max_y - 1:
            if zone is not board.get_global_zone(gx, gy + 1):
                pygame.draw.line(
                    screen,
                    (180, 180, 180),
                    (px, py + ZONE_PIXEL_SIZE),
                    (px + ZONE_PIXEL_SIZE, py + ZONE_PIXEL_SIZE),
                    1,
                )

    # 3. Dessin des Bordures (Murs et Portes par-dessus la grille)
    for (gx1, gy1), (gx2, gy2), border_obj in board.iter_global_borders():
        if border_obj == Border.NONE:
            continue

        px = max(gx1, gx2) * ZONE_PIXEL_SIZE
        py = max(gy1, gy2) * ZONE_PIXEL_SIZE
        is_vertical = gx1 != gx2

        color = (0, 0, 0)  # Mur
        if isinstance(border_obj, Door):
            color = (0, 255, 0) if border_obj.is_open else (255, 0, 0)

        thickness = 5
        if is_vertical:
            pygame.draw.line(
                screen, color, (px, py), (px, py + ZONE_PIXEL_SIZE), thickness
            )
        else:
            pygame.draw.line(
                screen, color, (px, py), (px + ZONE_PIXEL_SIZE, py), thickness
            )


def draw_door(screen, door, px, py):
    """Logique spécifique pour dessiner une porte selon son état."""
    color = (0, 255, 0) if door.is_open else (255, 0, 0)
    # Dessin d'un rectangle pour symboliser la porte
    d_rect = pygame.Rect(px - 15, py - 5, 30, 10)
    pygame.draw.rect(screen, color, d_rect)


# def draw_board(screen: pygame.Surface, board: Board) -> None:
#     for t_y, row in enumerate(board.tiles_map):
#         for t_x, tile in enumerate(row):
#             for z_y, zone_row in enumerate(tile.grid):
#                 for z_x, zone in enumerate(zone_row):

#                     # 1. Calcul de la position de la zone
#                     px = (t_x * TILE_PIXEL_SIZE) + (z_x * ZONE_PIXEL_SIZE)
#                     py = (t_y * TILE_PIXEL_SIZE) + (z_y * ZONE_PIXEL_SIZE)
#                     rect = pygame.Rect(px, py, ZONE_PIXEL_SIZE, ZONE_PIXEL_SIZE)

#                     # 2. Dessin du sol (Street vs Building)
#                     color = COLOR_STREET if zone.type == "STREET" else COLOR_BUILDING
#                     pygame.draw.rect(screen, color, rect)
#                     pygame.draw.rect(screen, COLOR_GRID, rect, 1)  # Contour de la zone

#                     # 3. Dessin des bordures (Murs et Portes)
#                     for direction, obj in zone.boundaries.items():
#                         # Définition des coordonnées du trait de bordure
#                         # On dessine sur les bords du rectangle de la zone
#                         if direction == "N":
#                             line_coords = ((px, py), (px + ZONE_PIXEL_SIZE, py))
#                         elif direction == "S":
#                             line_coords = (
#                                 (px, py + ZONE_PIXEL_SIZE),
#                                 (px + ZONE_PIXEL_SIZE, py + ZONE_PIXEL_SIZE),
#                             )
#                         elif direction == "E":
#                             line_coords = (
#                                 (px + ZONE_PIXEL_SIZE, py),
#                                 (px + ZONE_PIXEL_SIZE, py + ZONE_PIXEL_SIZE),
#                             )
#                         elif direction == "W":
#                             line_coords = ((px, py), (px, py + ZONE_PIXEL_SIZE))

#                         # Logique d'affichage selon le type d'obstacle
#                         if obj == "WALL":  # Si c'est un mur simple
#                             pygame.draw.line(
#                                 screen, COLOR_WALL, line_coords[0], line_coords[1], 4
#                             )

#                         elif isinstance(obj, Door):  # Si c'est notre nouvel objet Door
#                             # Couleur dynamique selon l'état de la porte
#                             d_color = (
#                                 COLOR_DOOR_CLOSED
#                                 if obj.state == "CLOSED"
#                                 else COLOR_DOOR_OPEN
#                             )

#                             # On dessine un trait plus épais pour la porte (ou un petit rectangle)
#                             # Ici, on dessine une ligne épaisse au centre de la bordure
#                             pygame.draw.line(
#                                 screen, d_color, line_coords[0], line_coords[1], 6
#                             )

#                             # Optionnel : Petit indicateur visuel pour les portes d'objectif (Bleu/Vert/Rose)
#                             if obj.color != "RED" and obj.state == "CLOSED":
#                                 # Dessiner un petit carré de couleur au centre de la porte
#                                 mid_x = (line_coords[0][0] + line_coords[1][0]) // 2
#                                 mid_y = (line_coords[0][1] + line_coords[1][1]) // 2
#                                 pygame.draw.circle(
#                                     screen, (0, 0, 255), (mid_x, mid_y), 5
#                                 )


def draw_actor(screen: pygame.Surface, actor: Actor) -> None:
    # Calcul de la position réelle en pixels
    tile_offset_x = actor.tile_coords[0] * TILE_PIXEL_SIZE
    tile_offset_y = actor.tile_coords[1] * TILE_PIXEL_SIZE
    zone_offset_x = actor.zone_coords[0] * ZONE_PIXEL_SIZE
    zone_offset_y = actor.zone_coords[1] * ZONE_PIXEL_SIZE

    # Centre de la zone
    pos_x = tile_offset_x + zone_offset_x + (ZONE_PIXEL_SIZE // 2)
    pos_y = tile_offset_y + zone_offset_y + (ZONE_PIXEL_SIZE // 2)
    center = (pos_x, pos_y)
    # Dessiner un cercle (Bleu pour survivant, on pourra varier selon l'acteur)
    pygame.draw.circle(screen, (0, 100, 255), center, 20)
    # Petit contour blanc pour la visibilité
    pygame.draw.circle(screen, (255, 255, 255), center, 20, 2)

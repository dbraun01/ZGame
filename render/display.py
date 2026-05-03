import pygame
from core.board import Board, Door
from entities.actor import Actor

TILE_PIXEL_SIZE: int = 300
ZONE_PIXEL_SIZE: int = 100


def draw_board(screen: pygame.Surface, board: Board) -> None:
    for t_y, row in enumerate(board.tiles_map):
        for t_x, tile in enumerate(row):
            for z_y, zone_row in enumerate(tile.grid):
                for z_x, zone in enumerate(zone_row):

                    # Position de la zone
                    px = (t_x * TILE_PIXEL_SIZE) + (z_x * ZONE_PIXEL_SIZE)
                    py = (t_y * TILE_PIXEL_SIZE) + (z_y * ZONE_PIXEL_SIZE)

                    rect = pygame.Rect(px, py, ZONE_PIXEL_SIZE, ZONE_PIXEL_SIZE)

                    # Couleur du sol
                    color = (80, 80, 80) if zone.type == "STREET" else (120, 60, 30)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Grille

                    door_color = {"CLOSED": (255, 0, 0), "WALL": (0, 0, 0)}
                    # Dessin des portes (si présentes)
                    for direction, obj in zone.boundaries.items():
                        if isinstance(obj, Door):
                            # On dessine un petit indicateur de porte
                            if direction == "N":
                                d_rect = pygame.Rect(px + 40, py, 20, 10)
                            elif direction == "S":
                                d_rect = pygame.Rect(px + 40, py + 90, 20, 10)
                            elif direction == "E":
                                d_rect = pygame.Rect(px + 95, py + 35, 10, 30)
                            elif direction == "W":
                                d_rect = pygame.Rect(px - 5, py + 35, 10, 30)
                            pygame.draw.rect(
                                screen, door_color.get(obj.state, (0, 255, 0)), d_rect
                            )


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

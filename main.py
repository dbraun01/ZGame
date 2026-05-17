import pygame
from core.board import Zone, Tile, Board, Door, Border
from core.engine import GameEngine
from entities.survivor import Survivor
from render.display import draw_board, ZONE_PIXEL_SIZE


def main():
    pygame.init()
    # Fenêtre pour 2 tuiles (6 zones en X, 3 zones en Y) -> 600x300 pixels
    screen = pygame.display.set_mode((600, 300))
    pygame.display.set_caption("Zombicide Digital - Nouveau Rendu")
    clock = pygame.time.Clock()

    big_zone_1 = Zone("BUILDING")
    big_zone_2 = Zone("BUILDING")

    # --- TUILE 1 : BÂTIMENT ---
    layout_t1 = [
        [big_zone_1, big_zone_1, big_zone_2],
        [Zone("STREET"), Zone("STREET"), big_zone_2],
        [Zone("BUILDING"), Zone("STREET"), Zone("BUILDING")],
    ]
    tile1 = Tile(layout_t1)
    tile1.set_border((0, 0), (0, 1), Border.WALL)
    tile1.set_border((1, 0), (2, 0), Door())
    tile1.set_border((1, 0), (1, 1), Door(color="blue"))
    tile1.set_border((0, 1), (0, 2), Border.WALL)
    tile1.set_border((1, 1), (2, 1), Border.WALL)
    tile1.set_border((2, 1), (2, 2), Door())
    tile1.set_border((0, 2), (1, 2), Door(is_open=True))
    tile1.set_border((1, 2), (2, 2), Border.WALL)

    # --- TUILE 2 : RUE ---
    layout_t2 = [
        [Zone("BUILDING"), Zone("STREET"), Zone("BUILDING")],
        [Zone("STREET"), Zone("STREET"), Zone("STREET")],
        [Zone("BUILDING"), Zone("STREET"), Zone("BUILDING")],
    ]
    tile2 = Tile(layout_t2)
    tile2.set_border((0, 0), (1, 0), Border.WALL)
    tile2.set_border((0, 0), (0, 1), Border.WALL)
    tile2.set_border((1, 0), (2, 0), Door(color="green"))
    tile2.set_border((2, 0), (2, 1), Border.WALL)
    tile2.set_border((0, 1), (0, 2), Border.WALL)
    tile2.set_border((0, 2), (1, 2), Border.WALL)
    tile2.set_border((1, 2), (2, 2), Door())
    tile2.set_border((2, 2), (2, 1), Border.WALL)

    # Création du plateau
    board = Board([[tile1, tile2]])
    board.set_global_border((2, 1), (3, 1), Border.WALL)

    # --- SETUP DOUG ---
    # Doug commence sur la Tuile (0,0) à la Zone (0,0)
    doug = Survivor("Doug", start_pos=(0, 0, 0, 0))
    engine = GameEngine(board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_UP:
                    dy = -1
                elif event.key == pygame.K_DOWN:
                    dy = 1
                elif event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1

                if dx != 0 or dy != 0:
                    if engine.attempt_move(doug, dx, dy):
                        print(
                            f"Position: Tuile {doug.tile_coords}, Zone {doug.zone_coords} | PA: {doug.remaining_actions}"
                        )

                elif event.key == pygame.K_SPACE:
                    # Interaction porte (exemple simplifié)
                    if engine.interact_door(doug):
                        print(
                            f"Porte ouverte: Tuile {doug.tile_coords}, Zone {doug.zone_coords} | PA: {doug.remaining_actions}"
                        )
                    # for adj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    #     boundary = board.get_boundary(
                    #         (doug.x, doug.y), (doug.x + adj[0], doug.y + adj[1])
                    #     )
                    #     if isinstance(boundary, Door):
                    #         boundary.open()
                    #         print("Porte ouverte !")

        # --- RENDU ---
        screen.fill((0, 0, 0))
        draw_board(screen, board)

        # Dessin de Doug en utilisant ses propriétés calculées .x et .y
        px = doug.x * ZONE_PIXEL_SIZE + ZONE_PIXEL_SIZE // 2
        py = doug.y * ZONE_PIXEL_SIZE + ZONE_PIXEL_SIZE // 2
        pygame.draw.circle(screen, (0, 100, 255), (px, py), 20)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()

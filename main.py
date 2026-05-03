import pygame
import sys
from typing import List

# Importation de tes modules
from core.board import Board, Tile, Zone, Door
from core.engine import GameEngine
from entities.survivor import Survivor
from render.display import draw_board, draw_actor, TILE_PIXEL_SIZE


def create_test_board() -> Board:
    """
    Crée un scénario de test : 2 tuiles (1 Bâtiment, 1 Rue).
    """
    board = Board()

    # --- Création de la Tuile 1 (3x3 Bâtiments) ---
    layout_1V: List[List[Zone]] = [
        [Zone("BUILDING"), Zone("BUILDING"), Zone("STREET")],
        [Zone("BUILDING"), Zone("BUILDING"), Zone("STREET")],
        [Zone("STREET"), Zone("STREET"), Zone("STREET")],
    ]

    # Ajout d'une porte au nord de la zone centrale de cette tuile
    layout_1V[1][1].boundaries["S"] = Door(state="CLOSED")
    layout_1V[1][1].boundaries["E"] = Door(state="WALL")
    layout_1V[0][1].boundaries["E"] = Door(state="WALL")
    layout_1V[1][0].boundaries["S"] = Door(state="WALL")

    tile_1V = Tile(layout_1V)

    # --- Création de la Tuile 2 (3x3 Rue) ---
    layout_3V: List[List[Zone]] = [
        [Zone("STREET"), Zone("STREET"), Zone("STREET")],
        [Zone("STREET"), Zone("BUILDING"), Zone("BUILDING")],
        [Zone("STREET"), Zone("BUILDING"), Zone("BUILDING")],
    ]

    # Ajout d'une porte au nord de la zone centrale de cette tuile
    layout_3V[1][1].boundaries["N"] = Door(state="CLOSED")
    layout_3V[1][1].boundaries["W"] = Door(state="WALL")
    layout_3V[1][2].boundaries["N"] = Door(state="WALL")
    layout_3V[2][1].boundaries["W"] = Door(state="CLOSED")

    tile_3V = Tile(layout_3V)

    # --- Assemblage du plateau (une ligne avec les deux tuiles) ---
    board.add_tile_row([tile_1V, tile_3V])

    return board


def main():
    # Initialisation de Pygame
    pygame.init()

    # Création du plateau de test
    game_board = create_test_board()
    engine = GameEngine(game_board)

    # On place un survivant sur la Tuile 0,0 dans la Zone centrale 1,1
    player = Survivor(name="Doug", start_pos=(0, 0, 1, 1))

    # Calcul de la taille de la fenêtre (2 tuiles de large, 1 de haut)
    screen_width = TILE_PIXEL_SIZE * 2
    screen_height = TILE_PIXEL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Zombicide Digital - Prototype")

    clock = pygame.time.Clock()

    # Boucle de jeu
    while True:
        # 1. Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                direction = None

                # --- Déplacements ---
                if event.key == pygame.K_UP:
                    direction = "N"
                elif event.key == pygame.K_DOWN:
                    direction = "S"
                elif event.key == pygame.K_LEFT:
                    direction = "W"
                elif event.key == pygame.K_RIGHT:
                    direction = "E"

                # --- Interactions ---
                elif event.key == pygame.K_SPACE:
                    # On vérifie quelles autres touches sont enfoncées à ce moment précis
                    keys = pygame.key.get_pressed()
                    target_dir = None

                    if keys[pygame.K_UP]:
                        target_dir = "N"
                    elif keys[pygame.K_DOWN]:
                        target_dir = "S"
                    elif keys[pygame.K_LEFT]:
                        target_dir = "W"
                    elif keys[pygame.K_RIGHT]:
                        target_dir = "E"

                    success = engine.interact_door(player, target_dir)

                # Exécution du mouvement si une flèche a été pressée
                if direction:
                    success = engine.attempt_move(player, direction)
                    if success:
                        print(
                            f"Mouvement {direction}. PA restants: {player.remaining_actions}"
                        )
                    else:
                        print("Mouvement bloqué !")

        # 2. Logique (vide pour le moment)

        # 3. Affichage
        screen.fill((30, 30, 30))  # Fond noir

        draw_board(screen, game_board)

        # Dessiner le survivant
        draw_actor(screen, player)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS


if __name__ == "__main__":
    main()

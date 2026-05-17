from typing import List, Union


class Door:
    def __init__(self, color: str = "neutral", is_open: bool = False):
        # state doit être une chaîne de caractères : "OPEN", "CLOSED", ou "LOCKED"
        self.is_open = is_open
        self.color = color

    def open(self):
        self.is_open = True


class Border:
    NONE = 0
    WALL = 1
    DOOR_CLOSED = Door(is_open=False)
    DOOR_OPEN = Door(is_open=True)


class Zone:
    def __init__(self, zone_type: str, zone_id: str = None):
        self.id = zone_id if zone_id else hex(id(self))[-4:]
        # zone_type doit être "STREET" ou "BUILDING"
        self.type = zone_type
        self.zombies = []
        self.players = []


class Tile:
    def __init__(self, layout: List[List[Zone]]):
        self.grid: List[List[Zone]] = layout
        self.size: int = len(layout)
        self.internal_borders = {}

    def get_zone_at(self, x: int, y: int) -> Zone:
        return self.grid[y][x]

    def set_border(self, pos1: tuple, pos2: tuple, border_type: Union[int, Door]):
        """Définit un mur ou une porte entre deux cases (0,0) à (2,2)"""
        # On trie les positions pour que (pos1, pos2) soit identique à (pos2, pos1)
        edge = tuple(sorted((pos1, pos2)))
        self.internal_borders[edge] = border_type

    def get_border(self, pos1: tuple, pos2: tuple) -> Union[int, Door]:
        edge = tuple(sorted((pos1, pos2)))
        return self.internal_borders.get(edge, Border.NONE)


class Board:
    def __init__(self, tile_layout: List[List["Tile"]], street_fusion: bool = False):
        self.tiles = tile_layout
        self.rows = len(tile_layout)
        self.cols = len(tile_layout[0])
        self.external_borders = {}
        if street_fusion:
            self.resolve_street_fusions()

    def resolve_street_fusions(self):
        """Parcourt les bordures des tuiles et fusionne les objets Zone de type STREET."""

        # 1. Fusion Horizontale (Tuile Gauche <-> Tuile Droite)
        for y in range(self.rows):
            for x in range(self.cols - 1):
                left_tile = self.tiles[y][x]
                right_tile = self.tiles[y][x + 1]

                # On vérifie les 3 cases de la bordure verticale
                for i in range(3):
                    z_left = left_tile.grid[i][2]  # Bord droit
                    z_right = right_tile.grid[i][0]  # Bord gauche

                    if z_left.type == "STREET" and z_right.type == "STREET":
                        self._merge_zones(z_right, z_left)

        # 2. Fusion Verticale (Tuile Haut <-> Tuile Bas)
        for y in range(self.rows - 1):
            for x in range(self.cols):
                top_tile = self.tiles[y][x]
                bottom_tile = self.tiles[y + 1][x]

                # On vérifie les 3 cases de la bordure horizontale
                for i in range(3):
                    z_top = top_tile.grid[2][i]  # Bord bas
                    z_bottom = bottom_tile.grid[0][i]  # Bord haut

                    if z_top.type == "STREET" and z_bottom.type == "STREET":
                        self._merge_zones(z_bottom, z_top)

    def _merge_zones(self, zone_to_replace: Zone, zone_to_keep: Zone):
        """Remplace toutes les instances de zone_to_replace par zone_to_keep sur tout le plateau."""
        if zone_to_replace is zone_to_keep:
            return

        for ty in range(self.rows):
            for tx in range(self.cols):
                tile = self.tiles[ty][tx]
                for gy in range(3):
                    for gx in range(3):
                        if tile.grid[gy][gx] is zone_to_replace:
                            tile.grid[gy][gx] = zone_to_keep

    def get_global_zone(self, gx: int, gy: int) -> Zone:
        """Récupère l'objet Zone à partir de coordonnées globales (x, y)."""
        tile_size = self.tiles[0][0].size
        tx, zx = divmod(gx, tile_size)
        ty, zy = divmod(gy, tile_size)
        return self.tiles[ty][tx].get_zone_at(zx, zy)

    def get_boundary(self, g_pos1: tuple, g_pos2: tuple):
        """Récupère la bordure (Mur, Porte, None) entre deux cases globales."""
        tile_size = self.tiles[0][0].size
        gx1, gy1 = g_pos1
        gx2, gy2 = g_pos2

        tx1, zx1 = divmod(gx1, tile_size)
        ty1, zy1 = divmod(gy1, tile_size)
        tx2, zx2 = divmod(gx2, tile_size)
        ty2, zy2 = divmod(gy2, tile_size)

        if tx1 == tx2 and ty1 == ty2:
            # Même tuile : on interroge les bordures internes
            tile = self.tiles[ty1][tx1]
            return tile.get_border((zx1, zy1), (zx2, zy2))
        else:
            # Frontière inter-tuile
            # On stocke ça dans un attribut self.external_borders (à init dans __init__)
            edge = tuple(sorted((g_pos1, g_pos2)))
            return getattr(self, "external_borders", {}).get(edge, Border.NONE)

    def iter_global_zones(self):
        """
        Générateur qui 'aplatit' le plateau.
        Renvoie (global_x, global_y, objet_zone) pour éviter les boucles imbriquées.
        """
        for ty, row in enumerate(self.tiles):
            for tx, tile in enumerate(row):
                for zy, zone_row in enumerate(tile.grid):
                    for zx, zone in enumerate(zone_row):
                        global_x = (tx * tile.size) + zx
                        global_y = (ty * tile.size) + zy
                        yield global_x, global_y, zone

    def set_global_border(
        self, g_pos1: tuple, g_pos2: tuple, border_type: Union[int, Door]
    ):
        """
        Définit un mur ou une porte entre deux cases sur le plateau global (inter-tuiles).
        Utilise les coordonnées globales (gx, gy).
        """
        # On trie pour garantir que (A, B) soit toujours la même clé que (B, A)
        edge = tuple(sorted((g_pos1, g_pos2)))
        self.external_borders[edge] = border_type

    def iter_global_borders(self):
        """
        Générateur qui traduit les bordures internes des tuiles en coordonnées globales
        et y ajoute les bordures externes (inter-tuiles).
        Renvoie ((x1, y1), (x2, y2), objet_bordure).
        """
        for ty, row in enumerate(self.tiles):
            for tx, tile in enumerate(row):
                offset_x = tx * tile.size
                offset_y = ty * tile.size

                for (p1, p2), border_obj in tile.internal_borders.items():
                    # Traduction des coordonnées locales (p1, p2) vers globales (gp1, gp2)
                    gp1 = (p1[0] + offset_x, p1[1] + offset_y)
                    gp2 = (p2[0] + offset_x, p2[1] + offset_y)
                    yield gp1, gp2, border_obj

        for (gp1, gp2), border_obj in self.external_borders.items():
            yield gp1, gp2, border_obj

    def iter_entities(self):
        """
        Parcourt récursivement le plateau et cède chaque entité.
        Usage: for tile, entity in board.iter_entities(): ...
        """
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                # On itère sur les objets contenus dans la case (ex: Portes, Zombies, Survivants)
                for entity in tile.contents:
                    yield tile, entity

    def get_zone_cells(self, target_zone: Zone) -> List[tuple]:
        """
        Retourne la liste des coordonnées globales (gx, gy)
        de toutes les cases physiques appartenant à la zone cible.
        """
        return [
            (gx, gy) for gx, gy, zone in self.iter_global_zones() if zone is target_zone
        ]

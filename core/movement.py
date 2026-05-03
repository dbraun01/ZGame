from core.board import Zone, Door

def can_move(zone_depart: Zone, direction: str) -> bool:
    """
    Vérifie si le passage est libre vers une direction ("N", "S", "E", "W").
    Renvoie True si le mouvement est possible, False sinon.
    """
    boundary = zone_depart.boundaries[direction]
    
    if boundary is None: 
        return True
    if isinstance(boundary, Door):
        return boundary.state == "OPEN" 
    if boundary == "WALL":
        return False
        
    return False
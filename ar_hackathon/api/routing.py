"""
Amazon Robotics Hackathon - Routing API

This module defines the routing API for the Amazon Robotics Hackathon.
Students will implement the route_package function in this module.

*****IMPORTANT*****
Team name:Fulfillers
Email address:yma60@student.ubc.ca, singhaniamanushree@gmail.com, oliveirade.matheus@gmail.com, annie.wu2024@gmail.com
*******************
"""

from typing import Optional, Dict, List
from collections import deque
from ar_hackathon.models.game_state import GameState
from ar_hackathon.models.package import Package
from ar_hackathon.models.connection import Connection

def route_package(state: GameState, package: Package) -> Optional[str]:
    """
    LEVEL 1 (unweighted, directed):
    Choose the next hop that lies on a BFS-shortest path from current_fc to destination_fc.
    Returns next FC id (str) or None to stay put.
    """
    src = package.current_fc          # str
    dst = package.destination_fc      # str

    if not src or not dst or src == dst:
        return None

    # Build directed adjacency using Connection.from_fc -> Connection.to_fc
    adj: Dict[str, List[str]] = {}

    # Materialize nodes
    for fc in getattr(state, "fulfillment_centers", []):
        fid = getattr(fc, "id", None)
        if fid is not None and fid not in adj:
            adj[fid] = []

    # Add edges
    for conn in getattr(state, "connections", []):
        u = getattr(conn, "from_fc", None)
        v = getattr(conn, "to_fc", None)
        if u is None or v is None:
            continue
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, adj.get(v, []))  # ensure sink exists

    # If either endpoint isn't in the graph, don't move
    if src not in adj or dst not in adj:
        return None

    # Fast path: direct edge to destination
    neighbors = adj.get(src, [])
    if dst in neighbors:
        return dst

    # BFS that remembers only the first hop out of src (saves memory/time)
    visited = set([src])
    q = deque()

    # Seed queue with neighbors of src, remembering their first hop (themselves)
    for nb in neighbors:
        if nb not in visited:
            if nb == dst:
                return nb
            visited.add(nb)
            q.append((nb, nb))  # (node, first_hop)

    while q:
        node, first_hop = q.popleft()
        for nb in adj.get(node, []):
            if nb not in visited:
                if nb == dst:
                    return first_hop
                visited.add(nb)
                q.append((nb, first_hop))

    # No path from src to dst
    return None
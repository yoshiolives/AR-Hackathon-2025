"""
Amazon Robotics Hackathon - Routing API

This module defines the routing API for the Amazon Robotics Hackathon.
Students will implement the route_package function in this module.

*****IMPORTANT*****
Team name:Fulfillers
Email address:yma60@student.ubc.ca, singhaniamanushree@gmail.com, oliveirade.matheus@gmail.com, annie.wu2024@gmail.com
*******************
"""

from typing import Optional
from ar_hackathon.models.game_state import GameState
from ar_hackathon.models.package import Package

def dijkstra(state: GameState, src: str, dst: str):
    """Run Dijkstra’s algorithm from src to dst and return path as a list of FC IDs."""
    # Build adjacency list
    graph = {}
    for conn in state.connections:
        u, v, w = conn.source_fc, conn.dest_fc, conn.length
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))  # undirected graph

    # Initialize distances
    dist = {fc.id: float('inf') for fc in state.fulfillment_centers}
    prev = {}
    dist[src] = 0

    # Priority queue (min-heap)
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst:
            break
        if d > dist[u]:
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    # No path found
    if dst not in prev and src != dst:
        return []

    # Reconstruct path from dst to src
    path = []
    cur = dst
    while cur != src:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path  # list of FC IDs, excluding src


def route_package(state: GameState, package: Package) -> Optional[str]:
    """
    Determine the next FC to route a package to using Dijkstra’s shortest path.
    """
    # If already at destination, no routing needed
    if package.current_fc == package.destination_fc:
        return None  

    # Get shortest path from current location to destination
    path = dijkstra(state, package.current_fc, package.destination_fc)

    if not path:
        return None  # no valid route

    # Return the next hop (first FC in path)
    print("Result: ", path[0])
    return path[0]

# def route_package(state: GameState, package: Package) -> Optional[str]:
#     """
#     Determine the next FC to route a package to.
    
#     This is the function that students will implement. The game engine will call
#     this function for each package at each time step to determine where to route it.
    
#     Args:
#         state: GameState object containing the current state of the network
#         package: Package object containing information about the package
        
#     Returns:
#         next_fc_id: ID of the next FC to route the package to, or None to stay at current FC
#     """
#     # Student implementation here
    
#     pass

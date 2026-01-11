import networkx as nx
from crewai.tools import tool

GRAPH_PATH = "src/mars_exploration_flow/inputs/mars_terrain.graphml"


def load_graph():
    return nx.read_graphml(GRAPH_PATH)


@tool("shortest_terrain_path")
def shortest_terrain_path(source: str, target: str) -> dict:
    """
    Compute the shortest path and distance between two nodes
    in the Mars terrain graph, considering terrain difficulty.
    """
    G = load_graph()

    def terrain_weight(s, t, data):
        terrain_s = G.nodes[s].get("terrain", "plain")
        terrain_t = G.nodes[t].get("terrain", "plain")

        terrain_multipliers = {
            "plain": 1.0,
            "rocky": 1.5,
            "sandy": 2.0,
            "crater": 2.5
        }

        base_weight = 10
        multiplier = (
            terrain_multipliers.get(terrain_s, 1.0)
            + terrain_multipliers.get(terrain_t, 1.0)
        ) / 2

        return base_weight * multiplier

    distance = nx.dijkstra_path_length(
        G, source, target, weight=terrain_weight)
    path = nx.dijkstra_path(G, source, target, weight=terrain_weight)

    return {
        "source": source,
        "target": target,
        "distance": distance,
        "path": path
    }

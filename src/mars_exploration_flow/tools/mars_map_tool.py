from crewai.tools import tool

@tool("mars_path_planner")
def mars_path_planner(start_node: str, end_node: str) -> str:
    """
    Computes shortest path and distance between two nodes in Mars terrain graph.
    """
    # Aquí luego cargas GraphML y calculas caminos
    return f"Path from {start_node} to {end_node}, distance X"

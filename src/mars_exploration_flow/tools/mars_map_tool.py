from crewai.tools import BaseTool
from typing import Type, List, Dict
from pydantic import BaseModel, PrivateAttr
import networkx as nx
from typing import ClassVar, Dict


from mars_exploration_flow.types import (
    DronePath,
    DronePlanOutput,
    RoverPlanOutput,
    RoverPath,
)


# =========================
# Tool Input Schema
# =========================


class RoverNavigationInput(BaseModel):
    rovers: List[Dict]
    mission_report: Dict


class DroneNavigationInput(BaseModel):
    drones: List[Dict]
    mission_report: Dict


# =========================
# Tool Implementation
# =========================


class RoverNavigationTool(BaseTool):
    name: str = "rover_navigation_plan"
    description: str = (
        "Compute a full rover navigation plan using rover constraints, "
        "terrain compatibility, speed, and mission objectives."
    )
    args_schema: Type[RoverNavigationInput] = RoverNavigationInput

    graph_path: str = "src/mars_exploration_flow/inputs/mars_terrain.graphml"

    terrain_multipliers: dict = {
        "plain": 1.0,
        "rocky": 1.5,
        "sandy": 2.0,
        "icy": 2.0,
        "crater": 2.5,
    }

    priority_order: ClassVar[Dict[str, int]] = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    # Private attribute (CRUCIAL)
    _G: nx.Graph = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._G = nx.read_graphml(self.graph_path)

    def _run(self, rovers, mission_report) -> RoverPlanOutput:
        rover_plans: List[RoverPath] = []

        objectives = sorted(
            mission_report.get("objectives", []),
            key=lambda o: self.priority_order.get(o["priority"], 99),
        )

        print("🔥 TOOL CALLED")
        print("rovers =", rovers)
        print("mission_report =", mission_report)

        for rover in rovers:
            current_node = rover["location"]
            full_path: List[str] = [current_node]
            total_distance = 0.0

            for obj in objectives:
                target_node = obj["node"]

                def terrain_weight(u, v, data):
                    terrain_u = self._G.nodes[u].get("terrain", "plain")
                    terrain_v = self._G.nodes[v].get("terrain", "plain")

                    if (
                        terrain_u not in rover["terrain_compatibility"]
                        or terrain_v not in rover["terrain_compatibility"]
                    ):
                        return float("inf")

                    base_distance = float(data.get("distance", 10))
                    multiplier = (
                        self.terrain_multipliers.get(terrain_u, 1.0)
                        + self.terrain_multipliers.get(terrain_v, 1.0)
                    ) / 2

                    # velocidad = eficiencia
                    return (base_distance * multiplier) / rover["speed"]

                try:
                    segment = nx.dijkstra_path(
                        self._G, current_node, target_node, weight=terrain_weight
                    )
                    segment_distance = nx.dijkstra_path_length(
                        self._G, current_node, target_node, weight=terrain_weight
                    )
                except nx.NetworkXNoPath:
                    raise ValueError(
                        f"No valid path for rover '{rover['id']}' "
                        f"from {current_node} to {target_node}"
                    )

                # Evitar duplicar nodos
                full_path.extend(segment[1:])
                total_distance += segment_distance
                current_node = target_node

            rover_plans.append(
                RoverPath(
                    rover_id=rover["id"],
                    start_node=rover["location"],
                    end_node=current_node,
                    path=full_path,
                    distance=round(total_distance, 2),
                )
            )

        return RoverPlanOutput(rover_plans=rover_plans)


class DroneNavigationTool(BaseTool):
    name: str = "drone_navigation_plan"
    description: str = (
        "Compute an optimal drone navigation plan considering "
        "flight range, altitude, camera resolution and mission objectives."
    )

    args_schema: Type[DroneNavigationInput] = DroneNavigationInput

    graph_path: str = "src/mars_exploration_flow/inputs/mars_terrain.graphml"

    priority_order: ClassVar[Dict[str, int]] = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    CAMERA_SCORE: ClassVar[Dict[str, float]] = {
        "12MP": 1.0,
        "15MP": 1.3,
        "20MP": 1.6,
    }

    _G: nx.Graph = PrivateAttr()

    def __init__(self, **data):
        super().__init__(**data)
        self._G = nx.read_graphml(self.graph_path)

    # =========================
    # Main logic
    # =========================
    def _run(self, drones, mission_report) -> DronePlanOutput:
        drone_plans: List[DronePath] = []

        objectives = sorted(
            mission_report.get("objectives", []),
            key=lambda o: self.priority_order.get(o["priority"], 99),
        )

        for drone in drones:
            start = drone["location"]
            current = start
            path: List[str] = [start]
            total_distance = 0.0

            for obj in objectives:
                target = obj["node"]

                segment = nx.shortest_path(self._G, current, target, weight="distance")
                segment_distance = nx.shortest_path_length(
                    self._G, current, target, weight="distance"
                )

                # 🚨 Drone constraint: must return to base
                if total_distance + segment_distance * 2 > drone["range"]:
                    continue

                # 🎥 Observation quality check
                if not self._valid_observation(drone, obj):
                    continue

                path.extend(segment[1:])
                total_distance += segment_distance
                current = target

            # 🔁 Mandatory return
            if current != start:
                return_segment = nx.shortest_path(
                    self._G, current, start, weight="distance"
                )
                return_distance = nx.shortest_path_length(
                    self._G, current, start, weight="distance"
                )
                path.extend(return_segment[1:])
                total_distance += return_distance

            drone_plans.append(
                DronePath(
                    drone_id=drone["id"],
                    start_node=start,
                    end_node=start,
                    path=path,
                    distance=round(total_distance, 2),
                )
            )

        return DronePlanOutput(drone_plans=drone_plans)

    # =========================
    # Helpers
    # =========================
    def _valid_observation(self, drone: Dict, objective: Dict) -> bool:
        score = self.CAMERA_SCORE.get(drone["camera_resolution"], 1.0)

        if objective["type"] == "panoramic":
            if drone["altitude"] < 150:
                score *= 0.7

        elif objective["type"] == "radiation":
            if drone["altitude"] > 300:
                score *= 0.8

        return score >= 0.8

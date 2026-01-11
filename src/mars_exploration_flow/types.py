from pydantic import BaseModel, Field
from typing import List, Dict


# =========================
# Mission Crew Output
# =========================

class MissionAnalysisOutput(BaseModel):
    scientific_goals: List[str] = Field(description="Scientific objectives")
    operational_constraints: List[str] = Field(
        description="Operational constraints")
    mission_priorities: List[str] = Field(
        description="Mission priorities ordered")
    known_hazards: List[str] = Field(description="Known hazards")


# =========================
# Rover Crew
# =========================
class RoverCrewInput(BaseModel):
    rovers: List[dict]
    mission_report: dict


class RoverPath(BaseModel):
    rover_id: str
    start_node: str
    end_node: str
    path: List[str]
    distance: float


class RoverPlanOutput(BaseModel):
    rover_plans: List[RoverPath]


# =========================
# Drone Crew Output
# =========================

class DroneFlightPlan(BaseModel):
    drone_id: str
    survey_areas: List[str]
    flight_altitude: int
    estimated_duration: int


class DronePlanOutput(BaseModel):
    drone_flights: List[DroneFlightPlan]
    coverage_objectives: List[str]


# =========================
# Integration Crew Output
# =========================

class CoordinatedAction(BaseModel):
    vehicle_id: str = Field(description="ID of the vehicle (rover or drone)")
    action: str = Field(description="Action to be executed")
    time_window: str = Field(
        description="Time window or execution order for the action"
    )


class FinalMissionPlanOutput(BaseModel):
    mission_summary: str = Field(
        description="High-level summary of the final mission strategy"
    )
    coordinated_actions: List[CoordinatedAction] = Field(
        description="Coordinated actions among all vehicles"
    )
    risk_mitigation_strategies: List[str] = Field(
        description="Strategies to mitigate identified mission risks"
    )

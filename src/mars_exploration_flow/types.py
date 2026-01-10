from pydantic import BaseModel, Field
from typing import List, Dict


# =========================
# Mission Crew Output
# =========================

class MissionAnalysisOutput(BaseModel):
    scientific_goals: List[str] = Field(description="Scientific objectives")
    operational_constraints: List[str] = Field(description="Operational constraints")
    mission_priorities: List[str] = Field(description="Mission priorities ordered")
    known_hazards: List[str] = Field(description="Known hazards")


# =========================
# Rover Crew Output
# =========================

class RoverTaskPlan(BaseModel):
    rover_id: str = Field(description="Identifier of the rover")
    assigned_tasks: List[str] = Field(description="Tasks assigned to the rover")
    planned_path: List[str] = Field(
        description="Sequence of terrain nodes representing the rover path"
    )


class RoverPlanOutput(BaseModel):
    rover_plans: List[RoverTaskPlan] = Field(
        description="Detailed plans for each rover"
    )
    assumptions: List[str] = Field(
        description="Assumptions made during rover planning"
    )


# =========================
# Drone Crew Output
# =========================

class DroneFlightPlan(BaseModel):
    drone_id: str = Field(description="Identifier of the drone")
    survey_areas: List[str] = Field(
        description="Areas or nodes surveyed by the drone"
    )
    flight_altitude: int = Field(description="Planned flight altitude")
    estimated_duration: int = Field(
        description="Estimated flight duration in minutes"
    )


class DronePlanOutput(BaseModel):
    drone_flights: List[DroneFlightPlan] = Field(
        description="Planned drone flight missions"
    )
    coverage_objectives: List[str] = Field(
        description="Objectives achieved through aerial surveys"
    )


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

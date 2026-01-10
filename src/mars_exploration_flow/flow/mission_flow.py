from crewai.flow import Flow, start, listen
from mars_exploration_flow.crews.mission_crew.mission_crew import MissionCrew
from mars_exploration_flow.crews.rover_crew.rover_crew import RoverCrew
from mars_exploration_flow.crews.drone_crew.drone_crew import DroneCrew
from mars_exploration_flow.crews.integration_crew.integration_crew import IntegrationCrew

class MarsMissionFlow(Flow):
    """
    CrewAI Flow coordinating the Mars exploration mission.
    Execution order:
        1. Mission Crew
        2. Rover Crew and Drone Crew (in parallel)
        3. Integration Crew
    """

    @start()
    def run_mission_crew(self):
        print("🛰️ Running Mission Crew...")
        with open("src/mars_exploration_flow/inputs/mission_report.md", "r") as f:
            mission_text = f.read()
        MissionCrew().crew().kickoff(inputs={"mission_report": mission_text})
        return "mission_analysis_completed"

    @listen(run_mission_crew)
    def run_rover_crew(self, _):
        print("🚙 Running Rover Crew...")
        with open("src/mars_exploration_flow/inputs/rovers.json", "r") as f:
            rovers = f.read()
        with open("src/mars_exploration_flow/inputs/mars_map.graphml", "r") as f:
            terrain = f.read()
        RoverCrew().crew().kickoff(inputs={
            "rovers": rovers,
            "mars_map": terrain,
            "mission_analysis_file": "src/mars_exploration_flow/outputs/mission_analysis.md"
        })
        return "rover_planning_completed"

    @listen(run_mission_crew)
    def run_drone_crew(self, _):
        print("🚁 Running Drone Crew...")
        with open("src/mars_exploration_flow/inputs/drones.json", "r") as f:
            drones = f.read()
        with open("src/mars_exploration_flow/inputs/mars_map.graphml", "r") as f:
            terrain = f.read()
        DroneCrew().crew().kickoff(inputs={
            "drones": drones,
            "mars_map": terrain,
            "mission_analysis_file": "src/mars_exploration_flow/outputs/mission_analysis.md"
        })
        return "drone_planning_completed"

    @listen(run_rover_crew)
    @listen(run_drone_crew)
    def run_integration_crew(self, _):
        print("🧩 Running Integration Crew...")
        IntegrationCrew().crew().kickoff(inputs={
            "rover_plan_file": "src/mars_exploration_flow/outputs/rover_plan.md",
            "drone_plan_file": "src/mars_exploration_flow/outputs/drone_plan.md",
            "mission_analysis_file": "src/mars_exploration_flow/outputs/mission_analysis.md"
        })
        return "mission_integration_completed"

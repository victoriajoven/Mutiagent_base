from crewai.flow import Flow, start, listen
from mars_exploration_flow.crews.mission_crew.mission_crew import MissionCrew
from mars_exploration_flow.crews.rover_crew.rover_crew import RoverCrew
from mars_exploration_flow.crews.drone_crew.drone_crew import DroneCrew
from mars_exploration_flow.crews.integration_crew.integration_crew import IntegrationCrew
from mars_exploration_flow.tools.mission_files_tool import MissionFiles


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
        # MissionCrew().crew().kickoff(
        #     inputs={"mission_report": MissionFiles.get_mission_report()})
        return "mission_analysis_completed"

    @listen(run_mission_crew)
    def run_rover_crew(self, _):
        print("🚙 Running Rover Crew...")
        RoverCrew().crew().kickoff(inputs={"rovers": MissionFiles.get_rovers(
        ), "mission_analysis_file": MissionFiles.get_mission_analysis()})
        return "rover_planning_completed"

    @listen(run_mission_crew)
    def run_drone_crew(self, _):
        print("🚁 Running Drone Crew...")
        DroneCrew().crew().kickoff(inputs={"drones": MissionFiles.get_drones(
        ), "mission_analysis_file": MissionFiles.get_mission_analysis()})
        return "drone_planning_completed"

    @listen(run_rover_crew)
    @listen(run_drone_crew)
    def run_integration_crew(self, _):
        print("🧩 Running Integration Crew...")
        IntegrationCrew().crew().kickoff(inputs={"mission_analysis": MissionFiles.get_mission_analysis(),
                                                 "rover_plan": MissionFiles.get_rover_plan(),
                                                 "drone_plan": MissionFiles.get_drone_plan()
                                                 },)
        return "mission_integration_completed"

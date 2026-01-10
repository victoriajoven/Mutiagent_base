from crewai.flow import Flow, start, listen

from mars_exploration_flow.crews.mission_crew.mission_crew import MissionCrew
from mars_exploration_flow.crews.drone_crew.drone_crew import DroneCrew
from mars_exploration_flow.crews.integration_crew.integration_crew import IntegrationCrew
from mars_exploration_flow.crews.rover_crew.rover_crew import RoverCrew



class MarsMissionFlow(Flow):
    """
    CrewAI Flow coordinating the Mars exploration mission.
    Execution order:
    1. Mission Crew
    2. Rover Crew and Drone Crew (in parallel)
    3. Integration Crew
    """

    @start()
    def run_crew(self):
        """
        Step 1: Analyze mission report and extract relevant information.
        """
        print("🛰️ Running Mission Crew...")
        MissionCrew().crew().kickoff()

        # The output is expected to be stored in outputs/mission_analysis.md
        return "mission_analysis_completed"

    @listen(run_crew)
    def run_rover_planning(self, _):
        """
        Step 2a: Plan rover operations based on mission analysis.
        """
        print("🚙 Running Rover Crew...")
        RoverCrew().crew().kickoff()

        return "rover_planning_completed"

    @listen(run_crew)
    def run_drone_planning(self, _):
        """
        Step 2b: Plan drone operations based on mission analysis.
        """
        print("🚁 Running Drone Crew...")
        DroneCrew().crew().kickoff()

        return "drone_planning_completed"

    @listen(run_rover_planning)
    @listen(run_drone_planning)
    def run_integration(self, _):
        """
        Step 3: Integrate all plans into a final mission strategy.
        """
        print("🧩 Running Integration Crew...")
        IntegrationCrew().crew().kickoff()

        return "mission_integration_completed"

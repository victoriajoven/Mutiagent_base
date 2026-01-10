"""
Main entry point for the Mars Exploration Multi-Agent System (MAS).

This file initializes and executes the CrewAI Flow that coordinates
the different agent crews involved in the mission.
"""

from mars_exploration_flow.flow.mission_flow import MarsMissionFlow


def main():
    """
    Executes the Mars exploration mission flow.
    """
    print("🚀 Starting Mars Exploration Multi-Agent System...")

    flow = MarsMissionFlow()
    #flow.run()
    flow.kickoff()

    print("✅ Mars mission planning completed.")
    print("📄 Check the outputs folder for generated plans.")


if __name__ == "__main__":
    main()

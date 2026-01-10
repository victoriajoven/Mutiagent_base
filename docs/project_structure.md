# Project Structure

This project implements a Multi-Agent System using CrewAI to simulate a Mars exploration mission.

## Main Components
- `flow/`: Defines the CrewAI Flow and execution order.
- `crews/`: One folder per required crew (Mission, Rover, Drone, Integration).
- `tools/`: Custom tools such as Mars terrain path planning.
- `inputs/`: Mission inputs as specified in the assignment.
- `outputs/`: Intermediate and final results for independent crew testing.

The execution order follows:
Mission Crew → Rover & Drone Crews → Integration Crew

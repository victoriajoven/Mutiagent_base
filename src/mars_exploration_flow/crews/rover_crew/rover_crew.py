import json
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew

from mars_exploration_flow.types import RoverPlanOutput


@CrewBase
class RoverCrew:
    """
    Rover Crew:
    Responsible for planning rover operations based on
    mission analysis and terrain constraints.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = LLM(
        model="ollama/mistral",
        base_url="http://localhost:11434",
        api_key="NA",
        provider="ollama",
    )

    # ---------- Agents ----------

    @agent
    def rover_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["rover_planner"],
            llm=self.llm,
            verbose=True,
        )

    # ---------- Tasks ----------

    @task
    def plan_rover_operations(self) -> Task:
        with open("src/mars_exploration_flow/inputs/rovers.json", "r") as f:
            rovers_data = json.load(f)
        with open("src/mars_exploration_flow/outputs/mission_analysis.md", "r") as f:
            mission_analysis = f.read()
        # lectura del mapa
        with open("src/mars_exploration_flow/inputs/mars_map.graphml", "r") as f:
            terrain_map = f.read()
        return Task(
            config=self.tasks_config["plan_rover_operations"],
            llm=self.llm,
            input_data={
                "rovers": rovers_data,
                "mission_analysis": mission_analysis,
                "mars_map": terrain_map
            },
            output_pydantic=RoverPlanOutput,
            output_file="src/mars_exploration_flow/outputs/rover_plan.md",
            
        )

    # ---------- Crew ----------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

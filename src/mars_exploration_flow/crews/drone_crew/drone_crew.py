import json
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew

from mars_exploration_flow.types import DronePlanOutput


@CrewBase
class DroneCrew:
    """
    Drone Crew:
    Responsible for planning drone flights for aerial surveys.
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
    def drone_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["drone_planner"],
            llm=self.llm,
            verbose=True,
        )

    # ---------- Tasks ----------

    @task
    def plan_drone_missions(self) -> Task:
        with open("src/mars_exploration_flow/inputs/drones.json", "r") as f:
            drones_data = json.load(f)
        with open("src/mars_exploration_flow/outputs/mission_analysis.md", "r") as f:
            mission_analysis = f.read()
        with open("src/mars_exploration_flow/inputs/mars_map.graphml", "r") as f:
            terrain_map = f.read()
        return Task(
            config=self.tasks_config["plan_drone_missions"],
            agent=self.drone_planner,
            llm=self.llm,
            input_data={
                "drones": drones_data,
                "mission_analysis": mission_analysis,
                "mars_map": terrain_map
            },
            output_pydantic=DronePlanOutput,
            output_file="src/mars_exploration_flow/outputs/drone_plan.md",
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

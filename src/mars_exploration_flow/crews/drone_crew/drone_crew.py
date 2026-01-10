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
        return Task(
            config=self.tasks_config["plan_drone_missions"],
            output_pydantic=DronePlanOutput,
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

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew

from mars_exploration_flow.types import FinalMissionPlanOutput


@CrewBase
class IntegrationCrew:
    """
    Integration Crew:
    Integrates rover and drone plans into a final mission strategy.
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
    def mission_integrator(self) -> Agent:
        return Agent(
            config=self.agents_config["mission_integrator"],
            llm=self.llm,
            verbose=True,
        )

    # ---------- Tasks ----------
    @task
    def integrate_mission_plan(self) -> Task:
        with open("src/mars_exploration_flow/outputs/rover_plan.md", "r") as f:
            rover_plan = f.read()
        with open("src/mars_exploration_flow/outputs/drone_plan.md", "r") as f:
            drone_plan = f.read()
        with open("src/mars_exploration_flow/outputs/mission_analysis.md", "r") as f:
            mission_analysis = f.read()

        return Task(
            config=self.tasks_config["integrate_mission_plan"],
            agent=self.mission_integrator,
            llm=self.llm,
            input_data={
                "mission_analysis": mission_analysis,
                "rover_plan": rover_plan,
                "drone_plan": drone_plan
            },
            output_pydantic=FinalMissionPlanOutput,
            output_file="outputs/final_mission_plan.md",
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

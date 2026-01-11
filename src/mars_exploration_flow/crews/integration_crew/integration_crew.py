from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew

from mars_exploration_flow.tools.mission_files_helper import MissionFiles
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
        return Task(
            config=self.tasks_config["integrate_mission_plan"],
            llm=self.llm,
            output_pydantic=FinalMissionPlanOutput,
            callback=MissionFiles.set_final_mission_plan,
            markdown=True
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

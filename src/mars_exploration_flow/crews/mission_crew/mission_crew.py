from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from mars_exploration_flow.types import MissionAnalysisOutput

# =========================
# Mission Crew Definition
# =========================

@CrewBase
class MissionCrew:
    """
    Mission Crew:
    Responsible for analyzing the mission report and extracting
    structured mission requirements.
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
    def mission_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["mission_analyst"],
            llm=self.llm,
            verbose=True,
        )

    # ---------- Tasks ----------  
    @task
    def plan_rover_path(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_mission"], output_pydantic=MissionAnalysisOutput
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

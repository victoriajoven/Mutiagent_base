import json
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from mars_exploration_flow.tools.mission_files_tool import MissionFiles
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
        return Task(
            config=self.tasks_config["plan_rover_operations"],
            llm=self.llm,
            output_pydantic=RoverPlanOutput,
            callback=MissionFiles.set_rover_plan,
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

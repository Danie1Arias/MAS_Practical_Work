from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from emergency_flow.tools.OSMnxCustomTool import ShortestPathTool
from emergency_flow.models.models import FireReport


@CrewBase
class GasFirefighterCrew:
    """GasFirefighterCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def firefighter_driver(self) -> Agent:
        return Agent(
            config=self.agents_config['firefighter_driver'],
            tools=[ShortestPathTool(), FileReadTool()],
            verbose=True,
            llm='ollama/llama3.1'
        )

    @agent
    def gas_firefighter(self) -> Agent:
        return Agent(
            config=self.agents_config['gas_firefighter'],
            verbose=True,
            llm='ollama/llama3.1'
        )

    @task
    def drive_to_emergency_site(self) -> Task:
        return Task(
            config=self.tasks_config['drive_to_emergency_site'],
            output_file='src/emergency_flow/outputs/gas_firefighter_crew/drive_to_emergency_site_report.md'
        )

    @task
    def extinguish_gas_fire(self) -> Task:
        return Task(
            config=self.tasks_config['extinguish_gas_fire'],
            output_pydantic=FireReport,
            output_file='src/emergency_flow/outputs/gas_firefighter_crew/extinguish_gas_fire_report.md'
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Gas Firefighter crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

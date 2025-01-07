from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from emergency_flow.tools.custom_tool import ShortestPathTool
from typing import Dict

@CrewBase
class MedicalserviceCrew:
    """MedicalserviceCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, inputs: Dict = None):
        self.inputs = inputs or {}

    @agent
    def ambulance_driver(self) -> Agent:
        return Agent(
            config=self.agents_config['ambulance_driver'],
            tools=[ShortestPathTool(), FileReadTool()],
            verbose=False,
            llm='ollama/llama3.1'
        )

    @agent
    def paramedic(self) -> Agent:
        return Agent(
            config=self.agents_config['paramedic'],
            verbose=False,
            llm='ollama/llama3.1'
        )

    @task
    def drive_to_emergency_site(self) -> Task:
        location = {
            "latitude": self.inputs.get("latitude"),
            "longitude": self.inputs.get("longitude")
        }
        return Task(
            config=self.tasks_config['drive_to_emergency_site'],
            parameters=location
        )

    @task
    def treat_injured_people(self) -> Task:
        details = {
            "severity": self.inputs.get("severity"),
            "people_in_danger": self.inputs.get("people_in_danger")
        }
        return Task(
            config=self.tasks_config['treat_injured_people'],
            parameters=details,
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MedicalserviceCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False
        )

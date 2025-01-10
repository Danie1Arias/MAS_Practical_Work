from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from emergency_flow.tools.OSMnxCustomTool import ShortestPathTool

@CrewBase
class MedicalserviceCrew:
    """MedicalserviceCrew crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def ambulance_driver(self) -> Agent:
        return Agent(
            config=self.agents_config['ambulance_driver'],
            tools=[ShortestPathTool(), FileReadTool()],
            verbose=True,
            llm='ollama/llama3.1'
        )

    @agent
    def paramedical(self) -> Agent:
        return Agent(
            config=self.agents_config['paramedical'],
            verbose=True,
            llm='ollama/llama3.1'
        )

    @task
    def drive_to_emergency_site(self) -> Task:
        print("Driving to the emergency site")
        return Task(
            config=self.tasks_config['drive_to_emergency_site'],
            output_file='src/emergency_flow/outputs/medicalservice_crew/drive_to_emergency_site_report.md'
        )

    @task
    def treat_injured_people(self) -> Task:
        print("Treating injured people")
        return Task(
            config=self.tasks_config['treat_injured_people'],
            output_file='src/emergency_flow/outputs/medicalservice_crew/treat_injured_people_report.md'
        )
    
    @task
    def drive_to_hospital(self) -> Task:
        print("Driving to the hospital")
        return Task(
            config=self.tasks_config['drive_to_hospital'],
            output_file='src/emergency_flow/outputs/medicalservice_crew/drive_to_hospital_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MedicalserviceCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

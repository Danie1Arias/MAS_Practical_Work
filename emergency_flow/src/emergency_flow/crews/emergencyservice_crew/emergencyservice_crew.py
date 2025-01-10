from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from emergency_flow.crews.models.models import PhoneCallDetails


@CrewBase
class EmergencyServiceCrew():
	"""Emergency Service Crew that processes fire emergency reports"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def call_center_manager(self) -> Agent:
		"""Agent that reads the emergency report and extracts information"""
		return Agent(
			config=self.agents_config['call_center_manager'],
			tools=[FileReadTool()],
			llm='ollama/llama3.1'
		)

	@task
	def read_emergency_report(self) -> Task:
		return Task(
			config=self.tasks_config['read_emergency_report'],
			output_pydantic=PhoneCallDetails,
			output_file='src/emergency_flow/outputs/emergencyservice_crew/read_emergency_report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Emergency Service Crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
		)

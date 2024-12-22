from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import FileReadTool

@CrewBase
class EmergencyServiceCrew():
	"""Emergency Service Crew that processes fire emergency reports"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def call_center_agent(self) -> Agent:
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
			expected_output="""
			A map of the most important varaibles (Fire type, Location X, 
			Location Y, Injured people, Fire Severity) and their values"""
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

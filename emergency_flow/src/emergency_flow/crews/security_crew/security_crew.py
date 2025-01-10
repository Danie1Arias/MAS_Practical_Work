from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from emergency_flow.tools.OSMnxCustomTool import ShortestPathTool
from typing import Dict

@CrewBase
class SecurityCrew:
	"""SecurityCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def rescue_supporter(self) -> Agent:
		return Agent(
			config=self.agents_config['rescue_supporter'],
			verbose=False,
			llm='ollama/llama3.1'
		)
	
	@agent
	def security_supervisor(self) -> Agent:
		return Agent(
			config=self.agents_config['security_supervisor'],
			verbose=True,
			llm='ollama/llama3.1'
		)
	
	@agent
	def traffic_driver(self) -> Agent:
		return Agent(
			config=self.agents_config['traffic_driver'],
			tools=[ShortestPathTool(), FileReadTool()],
			verbose=True,
			llm='ollama/llama3.1'
		)

	@task
	def rescue_support(self) -> Task:
		details = {
			"Names": [{"name": "Ana", "status": "Ok"},
			 		  {"name": "Luis", "status": "Ok"},
					  {"name": "Silvia", "status": "revision"},
					  {"name": "Benito(gato)", "status": "unknown"}]
        }
		print("Create rescue individuals report")
		return Task(
			config=self.tasks_config['rescue_support'],
			parameters=details,
			output_file='src/emergency_flow/outputs/security_crew/rescue_support_report.md'
		)
	
	@task
	def drive_to_emergency_site(self) -> Task:
		print("Create rescue individuals report")
		return Task(
			config=self.tasks_config['drive_to_emergency_site'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the SecurityCrew crew"""
		return Crew(
			agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
		)
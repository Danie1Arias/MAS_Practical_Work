#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.emergencyservice_crew.emergencyservice_crew import EmergencyServiceCrew
from .crews.firefighter_crew.firefighter_crew import FirefighterCrew
from .crews.medicalservice_crew.medicalservice_crew import MedicalserviceCrew
from .crews.security_crew.security_crew import SecurityCrew
from .crews.models.models import PhoneCallDetails, FireType, Severity
import os


class EmergencyState(BaseModel):
    emergency_active: bool = True
    firefighter_crew_active: bool = False
    medicalservices_crew_active: bool = False
    security_crew_active: bool = False
    phone_call_details: PhoneCallDetails = None


class EmergencyFlow(Flow[EmergencyState]):

    @start()
    def attend_emergency_call(self):
        """Receives the emergency call and extract the details"""
        print("Emergency call received. Extracting relevant details.")
        
        file_path = os.path.join(os.path.dirname(__file__), 'inputs', 'emergency_report.md')
        result = EmergencyServiceCrew().crew().kickoff(inputs={
            'file_path': file_path
        })

        self.state.phone_call_details = PhoneCallDetails(
            longitude=result['longitude'],
            latitude=result['latitude'],
            fire_type=result['fire_type'],
            severity=result['severity'],
            people_in_danger=result['people_in_danger']
        )


    @listen(attend_emergency_call)
    def activate_relevant_crews(self):
        """Activates the relevant Crews based on the phone call details"""
        print("Activating relevant crews based on call details:")
        if (
             self.state.phone_call_details.people_in_danger > 0
        ): 
            print("- Security Crew Active")
            self.state.security_crew_active = True
            SecurityCrew().crew().kickoff(inputs={
                "phone_call_details": self.state.phone_call_details,
                "graph_path": os.path.join(os.path.dirname(__file__), 'inputs', 'valencia.graphml')
                })

        if (
            self.state.phone_call_details.fire_type != FireType.NONE
        ): 
            print("- Firefighter Crew Active")
            self.state.firefighter_crew_active = True
            # FirefighterCrew().crew().kickoff(inputs=self.state.phone_call_details)
        if (
            self.state.phone_call_details.people_in_danger > 0
        ): 
            print("- Medical Services Crew Active")
            self.state.medicalservices_crew_active = True
            MedicalserviceCrew().crew().kickoff(inputs={
                "phone_call_details": self.state.phone_call_details,
                "data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'ambulances.json'),
                "graph_path": os.path.join(os.path.dirname(__file__), 'inputs', 'valencia.graphml')
            })
            


def kickoff():
    emergency_flow = EmergencyFlow()
    emergency_flow.kickoff()


def plot():
    emergency_flow = EmergencyFlow()
    emergency_flow.plot()


if __name__ == "__main__":
    kickoff()

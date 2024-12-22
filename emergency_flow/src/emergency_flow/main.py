#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.emergencyservice_crew.emergencyservice_crew import EmergencyServiceCrew
from .crews.firefighter_crew.firefighter_crew import FirefighterCrew
from .crews.medicalservice_crew.medicalservice_crew import MedicalserviceCrew
from .crews.security_crew.security_crew import SecurityCrew
from .crews.models.models import PhoneCallDetails, FireType, Severity
from crewai_tools import FileReadTool


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
        
        result = EmergencyServiceCrew().crew().kickoff(inputs={
            'file_path': '/inputs/emergency_report.md'
        })

        print(result)

        # This code below shold be provided by the EmergencyServiceCrew
        self.state.phone_call_details = PhoneCallDetails(
                location = "Location",
                fire_type = FireType.ORDINARY,
                severity = Severity.HIGH,
                people_in_danger= 5
            )
        
        print(f"Detials extracted: {self.state.phone_call_details}")

    @listen(attend_emergency_call)
    def activate_relevant_crews(self):
        """Activates the relevant Crews based on the phone call details"""
        print("Activating relevant crews based on call details:")

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
            # MedicalserviceCrew().crew().kickoff(inputs=self.state.phone_call_details)

        if (
            self.state.phone_call_details.severity == Severity.MEDIUM or
            self.state.phone_call_details.severity == Severity.HIGH
        ): 
            print("- Security Crew Active")
            self.state.security_crew_active = True
            # SecurityCrew().crew().kickoff(inputs=self.state.phone_call_details)


    # TODO: (Proposal) Create an agent that creats a report of the emergency


def kickoff():
    emergency_flow = EmergencyFlow()
    emergency_flow.kickoff()


def plot():
    emergency_flow = EmergencyFlow()
    emergency_flow.plot()


if __name__ == "__main__":
    kickoff()

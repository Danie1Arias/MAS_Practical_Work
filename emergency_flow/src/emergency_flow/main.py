#!/usr/bin/env python
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router, or_
from .crews.ordinary_firefighter_crew.ordinary_firefighter_crew import OrdinaryFirefighterCrew
from .crews.electrical_firefighter_crew.electrical_firefighter_crew import ElectricalFirefighterCrew
from .crews.gas_firefighter_crew.gas_firefighter_crew import GasFirefighterCrew
from .crews.emergencyservice_crew.emergencyservice_crew import EmergencyServiceCrew
from .crews.reinforcement_firefighter_crew.reinforcement_firefighter_crew import ReinforcementFirefighterCrew
from .crews.medicalservice_crew.medicalservice_crew import MedicalserviceCrew
from .crews.security_crew.security_crew import SecurityCrew
from .models.models import PhoneCallDetails, FireType, Severity
import os

class EmergencyState(BaseModel):
    phone_call_details: PhoneCallDetails = None
    fire_active: bool = False
    people_in_danger_rescued: bool = False

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

        if self.state.phone_call_details.fire_type != FireType.NONE:
            self.state.fire_active = True


    @router(attend_emergency_call)
    def activate_firefighters_crew(self):
        """Activates the relevant Firefighter crew based on the call details"""

        print("Activating relevant firefighter crew.")
        
        if (self.state.phone_call_details.fire_type == FireType.GAS):
            print("- Gas Firefighter Crew Active")
            result = GasFirefighterCrew().crew().kickoff(inputs={
                "phone_call_details": self.state.phone_call_details,
                "data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'fire_trucks.json')
            })

            if (result['extinguished'] == True):
                self.state.fire_active = False

        if (self.state.phone_call_details.fire_type == FireType.ELECTRICAL):
            print("- Electrical Firefighter Crew Active")
            result = ElectricalFirefighterCrew().crew().kickoff(inputs={
                "phone_call_details": self.state.phone_call_details,
                "data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'fire_trucks.json')
            })

            if (result['extinguished'] == True):
                self.state.fire_active = False

        if (self.state.phone_call_details.fire_type == FireType.ORDINARY):
            print("- Ordinary Firefighter Crew Active")
            result = OrdinaryFirefighterCrew().crew().kickoff(inputs={
                "phone_call_details": self.state.phone_call_details,
                "data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'fire_trucks.json')
            })

            if (result['extinguished'] == True):
                self.state.fire_active = False

        if (self.state.phone_call_details.severity != Severity.LOW and self.state.fire_active):
            print("- Reinforcement Firefighter Crew Active")
            result = ReinforcementFirefighterCrew().crew().kickoff(inputs={
                "phone_call_details": self.state.phone_call_details,
                "data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'fire_trucks.json')
            })

            if (result['extinguished'] == True):
                self.state.fire_active = False

        if self.state.fire_active:
            return "send_reinforcement_firefighters"
        else:
            return "fire_extinguished"
            
        
    @listen(or_("fire_extinguished", "activate_reinforcement_firefighter_crew"))
    def activate_security_crew(self):
        if self.state.fire_active == False:
            if (self.state.phone_call_details.people_in_danger > 0):
                print("Activating Security Crew Active")
                SecurityCrew().crew().kickoff(inputs={
                    "phone_call_details": self.state.phone_call_details,
                    "graph_path": os.path.join(os.path.dirname(__file__), 'inputs', 'valencia.graphml')
                    })

                people_in_danger_rescued = True

                if people_in_danger_rescued:
                    print("People in danger rescued.")
                    self.state.people_in_danger_rescued = True
                else:
                    print("Send reinforcement rescuers.")
                    SecurityCrew().crew().kickoff(inputs={
                        "phone_call_details": self.state.phone_call_details,
                        "graph_path": os.path.join(os.path.dirname(__file__), 'inputs', 'valencia.graphml')
                        })
                    self.state.people_in_danger_rescued = True
            else:
                self.state.people_in_danger_rescued = True
            
    @listen(activate_security_crew)
    def activate_medical_services_crew (self):
        if self.state.people_in_danger_rescued:
            print("Activating Medical Services Crew Active")
            MedicalserviceCrew().crew().kickoff(inputs={
                "phone_call_details": self.state.phone_call_details,
                "data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'ambulances.json'),
                "hospital_data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'hospital_beds.json')
            })

            print("People rescued and attended by medical services. Emergency resolved.")
        
    @listen("send_reinforcement_firefighters")
    def activate_reinforcement_firefighter_crew (self):
        print("- Second Reinforcement Firefighter Crew Active")
        result = ReinforcementFirefighterCrew().crew().kickoff(inputs={
            "phone_call_details": self.state.phone_call_details,
            "data_path": os.path.join(os.path.dirname(__file__), 'inputs', 'fire_trucks.json')
        })

        if (result['extinguished'] == True):
            self.state.fire_active = False
            

def kickoff():
    emergency_flow = EmergencyFlow()
    emergency_flow.kickoff()


def plot():
    emergency_flow = EmergencyFlow()
    emergency_flow.plot()


if __name__ == "__main__":
    kickoff()

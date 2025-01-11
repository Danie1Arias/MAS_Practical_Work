# Fire Emergency Project

## Overview

The **Fire Emergency Project** is a multi-agent AI simulation designed to emulate a city's emergency response system. Built on the **CrewAI framework**, the project orchestrates role-playing autonomous AI agents to address various emergency scenarios efficiently.  

The simulation environment is based in *Valencia* and involves the coordination of multiple specialized crews.

## Crew Clusters

1. **Firefighter Cluster**  
   Tasked with extinguishing fires, this cluster includes specialized teams:  
   - **Gas Crew**: Manages fires caused by gas leaks.  
   - **Electrical Crew**: Handles electrical-related fire hazards.  
   - **Ordinary Crew**: Deals with general fire incidents.  
   - **Reinforcement Crew**: Provides additional support to other teams as required.  

2. **Emergency Service Crew**  
   Responsible for initiating the emergency response process by:  
   - Receiving incident details via phone calls.  
   - Analyzing the information.  
   - Dispatching important details to the relevant crews.  

3. **Security Crew**  
   - Focuses on rescuing individuals and ensuring safety during emergencies.  

4. **Medical Service Crew**  
   - Provides on-site medical care to injured individuals.  
   - Arranges transportation of patients to the appropriate hospitals.  

This system provides a realistic simulation to analyze the efficiency and collaboration of multi-agent systems in emergency scenarios.

## Installation

Follow these steps to set up and run the project:

1. Install the required dependencies using the following command:  
```bash
crewai install
```

2. Ensure the following dependencies are installed:
```
dependencies = [
    "crewai[tools]>=0.79.4,<1.0.0",
    "osmnx>=1.5.0",
    "networkx>=3.0",
    "scikit-learn>=1.0.0"
]
```

## Input Files

The simulation relies on input data stored in the src/inputs directory:

1. **Databases**
    - ```ambulances.json```: Contains information about ambulance resources.
    - ```fire_trucks.json```: Details the available fire trucks and their specifications.
    - ```hospital_beds.json```: Tracks hospital bed availability for patient allocation.
    - ```security_station.json```: Contains information about the workstation coordinates.


2. **Phone Call Simulation**
    - ```emergency_report.md```: Simulates the phone call received by the Emergency Service Crew, providing incident details.

## Output Files

Simulation results and crew actions are stored in the src/outputs directory. Each crew has a dedicated subfolder where reports are saved in Markdown format. 

These reports include:

- Decisions made by the crew.
- Actions taken during the response.
- Final outcomes of their assigned tasks.

## How to Use

1. Install the dependencies using the provided command.
2. Populate the input files (```ambulances.json```, ```fire_trucks.json```, ```hospital_beds.json```, and ```emergency_report.md```) with relevant data.
3. Run the simulation using the command ```crewai flow kickoff```.
4. Review the output reports in the ```src/outputs``` directory to evaluate the crew's performance and coordination.
# Mars Exploration Multi-Agent System (MAS)

This project implements a Multi-Agent System (MAS) for simulating a Mars exploration mission using the **CrewAI** framework. The system coordinates different autonomous agents to generate an optimal exploration plan based on mission objectives, vehicle capabilities, and terrain constraints.

The project has been developed as part of the **MAS practical work** for the course *Multi-Agent Systems (ETSE-URV, 2025–26)*.


---
## Folder Structure

```
src
├── mars_exploration_mas/
│    │
│    ├── requirements.txt
│    ├── main.py                     
│    │
│    ├── flow/
│    │   └── mission_flow.py
│    │
│    ├── crews/
│    │   ├── mission_crew/
│    │   │   ├── config
│    │   │   │     ├── agents.py
│    │   │   │     └── tasks.py  
│    │   │   └── crew.py
│    │   │
│    │   ├── rover_crew/
│    │   │   ├── config
│    │   │   │     ├── agents.py
│    │   │   │     └── tasks.py  
│    │   │   └── crew.py
│    │   │
│    │   ├── drone_crew/
│    │   │   ├── config
│    │   │   │     ├── agents.py
│    │   │   │     └── tasks.py  
│    │   │   └── crew.py
│    │   │
│    │   └── integration_crew/
│    │   │   ├── config
│    │   │   │     ├── agents.py
│    │   │   │     └── tasks.py  
│    │   │   └── crew.py
│    │
│    ├── tools/
│    │   └── mars_map_tool.py        
│    │
│    ├── inputs/
│    │   ├── mars_map.graphml
│    │   ├── mission_report.md
│    │   ├── rovers.json
│    │   └── drones.json
│    │
│    └── outputs/
│        ├── mission_analysis.md
│        ├── rover_plan.md
│        ├── drone_plan.md
│        └── final_mission_plan.md
│       
├── docs/
│    └── project_structure.md
│
└── README.md
```

---

## Project Overview

The goal of the system is to:
- Analyze a mission report describing scientific goals, priorities, constraints, and hazards.
- Plan coordinated operations for **rovers** and **drones**.
- Integrate all individual plans into a final mission strategy.

The system is structured into multiple **agent crews**, each responsible for a specific task, and coordinated using a **CrewAI Flow**.

---

## System Architecture

The Multi-Agent System is composed of the following crews:

### Mission Crew
- Analyzes the mission report.
- Extracts objectives, priorities, constraints, and hazards.
- Produces a structured mission analysis output.

### Rover Crew
- Plans rover navigation and operations.
- Computes terrain-aware paths using a graph-based environment.
- Considers rover constraints such as speed, energy, and terrain compatibility.

### Drone Crew
- Plans aerial surveys and drone missions.
- Considers drone-specific constraints such as range, altitude, and sensors.

### Integration Crew
- Integrates rover and drone plans.
- Produces a unified and coherent mission strategy.

---

## Execution Flow

The system execution is coordinated using a CrewAI Flow with the following order:

1. **Mission Crew**
2. **Rover Crew** and **Drone Crew** (executed at the same logical level)
3. **Integration Crew**

Each crew can be tested independently, as intermediate outputs are stored in files.

---

## Environment Representation

- The Martian surface is modeled as a **GraphML graph**.
- Nodes represent locations and include terrain properties (rocky, sandy, icy, crater, etc.).
- Edges represent traversable paths with associated distances.
- Custom tools are used to compute paths and distances based on vehicle constraints.

---

## Input Files

The following input files are required:

- **Mars terrain graph** (`.graphml`)
- **Mission report** (`.md`)
- **Rovers information** (`rovers.json`)
  - ID, location, energy, speed, terrain compatibility
- **Drones information** (`drones.json`)
  - ID, location, range, altitude, camera resolution

Example input files are provided with the project.

---

## Output Files

The system generates the following outputs:

- Mission analysis (structured and saved as file)
- Rover operation plan (Pydantic output + file)
- Drone operation plan (Pydantic output + file)
- Final integrated mission plan (Markdown)

Structured outputs are defined using **Pydantic models** to ensure consistency and reliability.

---

## Custom Tools

The project includes custom CrewAI tools, such as:
- Rover navigation tool (terrain-aware path planning)
- Drone planning tool (aerial mission planning)

These tools encapsulate domain-specific logic and are invoked directly by the agents.

---

## How to Run the Project

1. Install dependencies:
   ```bash
   cd src
   pip install -r requirements.txt
   python main.py



## Author
Victoria Joven

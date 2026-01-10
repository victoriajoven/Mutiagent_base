# Mutiagent_base


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
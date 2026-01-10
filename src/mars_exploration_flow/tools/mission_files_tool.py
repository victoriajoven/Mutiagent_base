from pathlib import Path
from typing import Any


class MissionFiles:
    _BASE = Path("src/mars_exploration_flow")

    _FILES = {
        "rovers": "inputs/rovers.json",
        "drones": "inputs/drones.json",
        "mission_report": "inputs/mission_report.md",
        "mission_analysis": "outputs/mission_analysis.md",
        "rover_plan": "outputs/rover_plan.md",
        "drone_plan": "outputs/drone_plan.md",
        "final_mission_plan": "outputs/final_mission_plan.md",
    }

    @classmethod
    def _read(cls, key: str, *, encoding: str | None = None) -> str:
        return (cls._BASE / cls._FILES[key]).read_text(encoding=encoding)

    @classmethod
    def _write(cls, key: str, content: str, *, encoding: str = "utf8") -> None:
        (cls._BASE / cls._FILES[key]).write_text(content, encoding=encoding)

    # ===== File readers =====

    @classmethod
    def get_rovers(cls) -> str:
        return cls._read("rovers")

    @classmethod
    def get_drones(cls) -> str:
        return cls._read("drones")

    @classmethod
    def get_mission_report(cls) -> str:
        return cls._read("mission_report", encoding="utf8")

    @classmethod
    def get_mission_analysis(cls) -> str:
        return cls._read("mission_analysis")

    @classmethod
    def get_rover_plan(cls) -> str:
        return cls._read("rover_plan")

    @classmethod
    def get_drone_plan(cls) -> str:
        return cls._read("drone_plan")

    # ===== File writers =====

    @classmethod
    def set_mission_analysis(cls, content: Any) -> None:
        cls._write("mission_analysis", content.raw)
        
    @classmethod
    def set_rover_plan(cls, content: Any) -> None:
        cls._write("rover_plan", content.raw)

    @classmethod
    def set_drone_plan(cls, content: Any) -> None:
        cls._write("drone_plan", content.raw)
        
    @classmethod
    def set_final_mission_plan(cls, content: Any) -> None:
        cls._write("final_mission_plan", content.raw)
        


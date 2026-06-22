import time
import json
from variables.physics_engine import ExergyEngine

class ExergyObserver:
    """
    The Brainstem: Monitors physics engine telemetry and enforces 
    operational constraints on the Exergy-Core.
    """
    def __init__(self, engine: ExergyEngine):
        self.engine = engine
        self.log_buffer = []

    def scan_cycle(self, measured_hz: float):
        """
        Parses raw sensor data and audits system integrity.
        """
        telemetry = self.engine.run_cycle(measured_hz)
        
        # Diagnostic Logic
        if not telemetry['resonance_locked']:
            status = "CRITICAL: Spin-Trap Frequency Mismatch"
        else:
            status = "NOMINAL: Power Extraction Active"
            
        self.log_buffer.append({
            "timestamp": time.time(),
            "status": status,
            **telemetry
        })
        return telemetry

# Implementation for Homeos integration
if __name__ == "__main__":
    # Initialize the engine (the physics) and the observer (the brainstem)
    core_engine = ExergyEngine()
    brainstem = ExergyObserver(core_engine)
    
    # Simulate a drift event (110Hz -> 105Hz)
    test_frequencies = [110.0, 108.5, 105.0]
    
    for hz in test_frequencies:
        data = brainstem.scan_cycle(hz)
        print(f"Monitoring at {hz}Hz: Yield={data['wattage_yield']:.2e}W, Status={'Locked' if data['resonance_locked'] else 'Unlocked'}")

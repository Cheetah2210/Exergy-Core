import numpy as np
import json

class ExergyEngine:
    def __init__(self, config_path='materials_matrix.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Load core quantum parameters
        self.kb = 1.380649e-23  # Boltzmann Constant
        self.T = 300.0          # Baseline Ambient Temp (K)
        
    def calculate_graphene_power(self):
        """Calculates power output from out-of-plane buckling (Brownian)."""
        gamma = self.config['layer_3_quantum_exergy']['ambient_graphene_pulse']['intrinsic_damping_gamma']
        mass = self.config['layer_3_quantum_exergy']['ambient_graphene_pulse']['domain_effective_mass_kg']
        
        # Power density approximation from fluctuation-dissipation theorem
        power_density = (self.kb * self.T) / gamma
        return power_density

    def calculate_spin_stability(self, frequency):
        """Determines magnetic stabilization effectiveness vs resonance."""
        target = self.config['layer_3_quantum_exergy']['magnetic_spin_trap']['resonance_frequency_hz']
        tolerance = self.config['layer_3_quantum_exergy']['magnetic_spin_trap']['precession_lock_tolerance_hz']
        
        # Calculates the 'Stability Factor' (0.0 to 1.0)
        stability = max(0, 1 - (abs(target - frequency) / (tolerance * 2)))
        return stability

    def run_cycle(self, current_hz):
        """Simulates one integration step of the Exergy-Core."""
        p_out = self.calculate_graphene_power()
        stability = self.calculate_spin_stability(current_hz)
        
        return {
            "wattage_yield": p_out * stability,
            "system_stability": stability,
            "resonance_locked": stability > 0.95
        }

# Example usage for the Brainstem integration
if __name__ == "__main__":
    engine = ExergyEngine()
    # Simulate the system operating at the target 110Hz
    results = engine.run_cycle(110.0)
    print(f"Core Output: {results['wattage_yield']:.2e} W | Stability: {results['system_stability']:.2f}")

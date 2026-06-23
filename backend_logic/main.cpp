#include "Engine.hpp"
#include <iostream>
#include <iomanip>

int main() {
    // Example
    double initial_asset_price = 100.0;
    double risk_free_rate = 0.05;
    double asset_volatility = 0.20;
    double target_time = 1.0;
    int simulation_paths = 1000000;

    std::cout << "Initializing Simulation Core..." << std::endl;
    
    SimulationEngine core_engine(initial_asset_price, risk_free_rate, asset_volatility, target_time, simulation_paths);

    std::cout << "Executing 1,000,000 price paths in parallel..." << std::endl;
    std::vector<double> execution_results = core_engine.run_simulation_matrix();

    double calculated_mean = core_engine.calculate_expected_value(execution_results);
    
    // Ideal: calculated_mean = analytical_target: the closer, the better
    double analytical_target = initial_asset_price * std::exp(risk_free_rate * target_time);

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Simulated Expected Price: $" << calculated_mean << std::endl;
    std::cout << "Analytical Target Base: $" << analytical_target << std::endl;
    return 0;
}
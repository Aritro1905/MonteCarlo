#ifndef ENGINE_HPP
#define ENGINE_HPP

#include <vector>
#include <random>

class SimulationEngine {
private:
    // S_T = S0 * exp((r - 0.5 * sigma^2) * T + sigma * sqrt(T) * Z)
    double S0;         // Initial Asset Price (e.g., Crude Oil price per barrel)
    double drift;      // Expected continuous growth rate (r)
    double sigma;      // Asset Volatility (annualized standard deviation)
    double T;          // Time horizon in years (e.g., 0.25 for 3 months)
    int num_paths;     // Total simulation executions (e.g., 1,000,000)

    std::mt19937_64 execution_generator;
    std::normal_distribution<double> normal_dist;

public:
    SimulationEngine(double initial_price, double rate, double volatility, double time_horizon, int paths);
    double execute_single_path();
    std::vector<double> run_simulation_matrix();
    double calculate_expected_value(const std::vector<double>& results);
    double calculate_value_at_risk(const std::vector<double>& results, double confidence_level);
};

#endif 
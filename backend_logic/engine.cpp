#include "Engine.hpp"
#include <cmath>
#include <numeric>
#include <execution>
#include <algorithm>
#include <iostream>

SimulationEngine::SimulationEngine(double initial_price, double rate, double volatility, double time_horizon, int paths)
    : S0(initial_price), drift(rate), sigma(volatility), T(time_horizon), num_paths(paths),
      execution_generator(std::random_device{}()), normal_dist(0.0, 1.0) 
{}

// Low-Level Simulation Execution Unit
double SimulationEngine::execute_single_path() {
    double Z = normal_dist(execution_generator);
    double drift_term = (drift - 0.5 * sigma * sigma) * T;
    double diffusion_term = sigma * std::sqrt(T) * Z;
    return S0 * std::exp(drift_term + diffusion_term);
}

std::vector<double> SimulationEngine::run_simulation_matrix() {
    std::vector<double> price_matrix(num_paths);
    std::for_each(std::execution::par, price_matrix.begin(), price_matrix.end(), [&](double& final_price) {
        final_price = execute_single_path();
    });

    return price_matrix;
}

double SimulationEngine::calculate_expected_value(const std::vector<double>& results) {
    double total_sum = std::reduce(std::execution::par, results.begin(), results.end(), 0.0);
    return total_sum / num_paths;
}

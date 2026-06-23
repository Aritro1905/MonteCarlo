#include <pybind11/pybind11.h>
#include <pybind11/stl.h> //Auto-converts C++ std::vector to Python lists
#include "Engine.hpp"

namespace py = pybind11;

PYBIND11_MODULE(hedge_core, m) {
    m.doc() = "High-Performance Monte Carlo Engine (C++ Backend)";

    // Bind the SimulationEngine class
    py::class_<SimulationEngine>(m, "SimulationEngine")
        .def(py::init<double, double, double, double, int>())
        .def("run_simulation_matrix", &SimulationEngine::run_simulation_matrix, "Executes the parallel Monte Carlo paths")
        .def("calculate_expected_value", &SimulationEngine::calculate_expected_value, "Aggregates the simulated paths into an expected price");
}
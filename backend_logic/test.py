import os
ucrt64_bin_path = r"C:\msys64\ucrt64\bin"
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(ucrt64_bin_path)
import backend_logic.hedge_core as hedge_core
import time

print("Initializing Python-to-C++ Bridge...")

# S0=100.0, r=5%, Volatility=20%, T=1.0 year, 1,000,000 paths
engine = hedge_core.SimulationEngine(100.0, 0.05, 0.20, 1.0, 1000000)

start_time = time.time()

print("Executing 1,000,000 paths via C++ backend")
results = engine.run_simulation_matrix()
expected_price = engine.calculate_expected_value(results)

execution_time = time.time() - start_time


print(f"Simulated Expected Price: ${expected_price:.4f}")
print(f"Engine Execution Time:    {execution_time:.4f} seconds")

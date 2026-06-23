import sysconfig
import pybind11
import sys
import os
py_inc = sysconfig.get_path('include')
py_lib = os.path.join(sys.prefix, 'libs')
pybind_inc = pybind11.get_include()
py_version = f"python{sys.version_info.major}{sys.version_info.minor}"

# command construction
cmd = f'g++ -O3 -shared -std=c++20 -I"{py_inc}" -I"{pybind_inc}" bindings.cpp Engine.cpp -o hedge_core.pyd -L"{py_lib}" -l{py_version} -ltbb12'

print("\nEXACT COMMAND\n")
print(cmd)


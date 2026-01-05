# resume

## Build

``` bash
python3 -m venv venv
source venv/bin/activate
pip install pyyaml
mkdir build
cd build
cmake .. -DPython3_EXECUTABLE=/home/carlos/resume/venv/bin/python3
cmake --build . --clean-first
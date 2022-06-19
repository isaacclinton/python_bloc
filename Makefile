run_tests:
	venv/Scripts/python -m unittest discover . -v

install_build_tools:
	venv/Scripts/python -m pip install build

build_wheel:
	venv/Scripts/python -m build --wheel
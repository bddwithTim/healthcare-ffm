# FFM - Healthcare plans extraction

This repository utilizes [pytest](https://docs.pytest.org/en/7.1.x/) framework for automation testing.

## Development
### Prerequisites:

* Python 3.9.2 Ensure that you have python installed in your system preferably Python 3.9.2.
* PyCharm Community Edition 2021.1+
* [Poetry 1.1.12](https://github.com/python-poetry/poetry)

[poetry](https://github.com/python-poetry/poetry) is a tool to handle dependency installation as well as building and packaging of Python packages. It only needs one file to do all of that: the new, [standardized](https://www.python.org/dev/peps/pep-0518/) `pyproject.toml`.

In other words, poetry uses pyproject.toml to replace `setup.py`, `requirements.txt`, `setup.cfg`, `MANIFEST.in` and the newly added `Pipfile`.

### Poetry and virtual environment setup

After cloning this github repository, prepare your development environment like so:

* Set up a Python virtual environment by navigating to PyCharm's Project [Python Interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#add_new_project_interpreter) and create a **new** `.venv` environment.

     ![Add Python Interpreter](https://user-images.githubusercontent.com/89407715/152498209-f82b2e26-9bda-40e1-85be-d28dbce55d2e.PNG)

* Click the **OK** button and close the Settings modal as the packages will not be populated at first. Open the [Python Interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#add_new_project_interpreter) once again and add the `poetry` package. Click the `Specify version` checkbox and from its drop-down selection, select the version **1.1.12** and click `Install Package`. Once installed, close the Project Settings altogether.

     ![Poetry Package](https://user-images.githubusercontent.com/89407715/152507704-7dd657fe-9716-4347-9c08-98a03a53cfba.png)

* Open a cmd/bash terminal `Alt+F12` in PyCharm and execute:
  ```console
  poetry install
  ```


## Test Execution

* Executing parallel tests. `pytest -n <num>` where `<num>` is the number of test instances.
   ```console
   pytest -n 3
   ```

* Executing tests which match the given substring expression. `pytest -k expression`.  An expression is a python evaluatable expression where all names are substring-matched against test names and their parent classes.
  * executes all tests under the python file `healthcare_ffm_test.py`
  ```console
  pytest -k healthcare_ffm_test.py
  ```
  * executes the test function named `test_healthcare_basic_flow`
  ```console
  pytest -k test_healthcare_basic_flow
  ```

* Executing all tests under a directory.
  ```console
  pytest ./tests
  ```

Alternatively, if the commands on the terminal doesn't work due to some corporate restrictions then utilize Pycharm's [Run/Debug Configuration](https://www.jetbrains.com/help/pycharm/run-debug-configuration-py-test.html) and add the sample arguments above inside the `Additional Arguments` text field.

   ![pytest_run_debug_configurations](https://user-images.githubusercontent.com/89407715/187354752-79632637-04ea-4944-8b92-36c226f7a976.png)


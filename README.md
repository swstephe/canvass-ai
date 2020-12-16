# Canvass AI assignment

I created a module "assignment" with two files.

- assignment/transform.py, which does the data transformation
- assignment/app.py, which implements a very basic REST APi

I also created a file "test.py", which uses the
Python built-in "unittest" to test the transform
and app modules.

I decided to create it with no requirements
beyond what comes built-in to Python.  I
used Python 3.9, but any 3.3+ Python should
work.

The endpoint is "/" which accepts POST requests
in JSON format.  It returns the transformed
result in JSON format.  All data is passed
using "utf8" encoding.

To run, run the module "assignment.app" for the
server ... (from the root of the directory)

    python -m assignment.app

... then run CURL commands against port 8080 ...

    curl -d @data/sensor-1.json http://localhost:8080

... or run the unittest.

    python test.py

You will need to run "python -m assignment.app" at the same time as the others.

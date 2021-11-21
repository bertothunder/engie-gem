# ENGIE GEM Test project

## Requirements

- python 3.7+ (used 3.9 in my dev env)
- pip
- docker
- virtualenv


Caveats:

- Only tested on Linux


## Setup the dev environment

- Create a virtualenv via `virtualenv <venv_dir>`. In my case, it was `.venv`.
- Activate virtualenv via `source <venv_dir>/bin/activate`.
- Install all necessary packages: `pip install -r requirements.txt`.
- For running unit tests, install the test packages: `pip install -r test-requirements.txt`.
- Optionally, build a docker image: `docker build -t <image_name> .


## Run unit tests

Run the unit tests via:

`pytest -vv`.


## Run the API

### Locally

Execute: `python api.py`, and the send your requests to `http://localhost:8888/<path>`.


### Docker image

Run the container in the interactive manner.

`docker run -p 8888:8888 --name <container_name> -t <image_name>`

Or run it as daemon by changing `-t` for `-d`, in the command line above.

Then send your requests to `http://localhost:8888/<path>`.


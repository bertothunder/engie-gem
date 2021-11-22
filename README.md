# ENGIE GEM Test project

## Requirements

- python 3.9
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

Execute: `python main.py`, and the send your requests to `http://localhost:8888/<path>`.

Or you can alternatively install the package:

`python setup.py install`

follow by executing `api`. 


### Docker image


Once built the image, run the container in the interactive manner:

`docker run -p 8888:8888 --name <container_name> -t <image_name>`

Or run it as daemon by changing `-t` for `-d`, in the command line above.

Then send your requests to `http://localhost:8888/<path>`.


### Configuration


The system can be configured in two possible ways:

- by setting the values as env variables when running the script:

`LOG_LEVEL=DEBUG LOG_FILE=file.log LISTEN_HOST="172.16.0.1" python main.py`. This will change the default setup.

- by setting the values in a JSON file in `config` directory; you can copy from `config/dev.json` or edit it. The values are matching 
the same name(s) as the env variables, and this will actually override any value passed by environment. To control which file to use, 
change it by using `CFG_FILE` env variable.

`CFG_FILE=config/myconfig.json python main.py`


##### Variables available:


- LISTEN_HOST: The IP address the API will listen upon, default 127.0.0.1
- LISTEN_PORT: The ip port to listen upon, default 8888
- DEBUG: Enable debug logs and automatic reload, default False.
- LOG_FORMAT: The logging format to use, default is `%(asctime)s - %(levelname)s - %(name)s:%(filename)s:%(lineno)d - %(message)s`
- LOG_LEVEL: The logging level to use, default is INFO



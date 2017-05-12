[![Build Status](https://travis-ci.org/sonata-nfv/son-editor-backend.svg?branch=master)](https://travis-ci.org/sonata-nfv/son-editor-backend.svg?branch=master)


# son-editor-backend

This is the backend of SONATA's web-based service and function descriptor editor. It serves as the data storage for the editor and interacts with all other services that are needed to create, update and release SONATA Service and VNF descriptors. It is designed to be used with the [son-editor-frontend](https://github.com/sonata-nfv/son-editor-frontend) but because all interaction and communication is taking place through a RESTful API, it is possible to be used with other user interfaces.

![son-editor screenshot](https://github.com/sonata-nfv/son-editor-frontend/raw/master/screenshot_network_editor.png "Screenshot of son-editor's NSD editor view")

## Installation

The editor (frontend and backend) can be installed and deployed as single Docker container and a docker-compose script.

1. Since the editor uses OAuth to authenticate its users, a OAuth application token is required to run it. To retrieve such a token (from GitHub), go to [GitHub Settings > OAuth applications](https://github.com/settings/developers) and 'Register a new application'.
    * Chose an application name: `SONATA Editor`
    * Configure the URL of your installation: `http://localhost/` or `http://your-domain.com`
    * Configure the authentication callback URL: `http://localhost/backend/login` or `http://your-domain.com/backend/login`
    * `Save` and collect the generated `ClientID` and `ClientSecretnt` for step 4
2. Clone this repository:
    * `git clone https://github.com/sonata-nfv/son-editor-backend`
3. Switch to `build-docker` folder:
    * `cd son-editor-backend/build-docker/`
4. Add GitHub OAuth `ClientID` and `ClientSecret` to `config.yaml`
    * `vim config.yaml`
5. Build and run container:
    * `docker-compose up`

Open your web browser and point to your server / local machine, e.g., `http://localhost/` and login to the editor using your GitHub account.

## Development

### Python environment
We recommend using [venv](https://docs.python.org/dev/tutorial/venv.html). If you have setup your Python 3 environment, open a shell in your virtual environment
and install [son-cli:v2](https://github.com/sonata-nfv/son-cli/tree/v2.0).

* `pip install git+https://github.com/sonata-nfv/son-cli.git@v2.0`
* `python setup.py install`
* `python setup.py develop`

To re-build the container:

* Do `docker-compose build --no-cache` in `build-docker/`

### Testing

* Configuration file used during tests: `src/son_editor/config.yaml`
* Run tests: `python setup.py test`

### Continuous Integration

All SONATA projects are automatically tested with SONATA's Jenkins CI environment. But this editor is an exception to this and uses a Travis CI job that is configured in `.travis`.

## Dependencies

* [son-cli](https://github.com/sonata-nfv/son-cli) >= 2.0
* [flask-restplus](https://pypi.python.org/pypi/flask-restplus) ==0.9.2
* [flask](https://pypi.python.org/pypi/Flask) == 0.12
* [sqlalchemy](https://pypi.python.org/pypi/SQLAlchemy) == 1.1.6
* [requests](https://pypi.python.org/pypi/requests) == 2.13.0
* [pyaml](https://pypi.python.org/pypi/pyaml) == 16.12.2

## Contributing

Contributing to the son-editor is really easy. You must:

1. Clone [this repository](http://github.com/sonata-nfv/son-editor-backend);
2. Work on your proposed changes, preferably through submiting [issues](https://github.com/sonata-nfv/son-editor-backend/issues);
3. Submit a Pull Request;
4. Follow/answer related [issues](https://github.com/sonata-nfv/son-editor-backend/issues) (see Feedback-Chanel, below).

## Further Documentation

You can find the editor's manual [here](https://github.com/sonata-nfv/son-editor-backend/raw/master/technical_document_editor.pdf).

The server code is documented using sphinx: [documentation](https://cn-upb.github.io/upb-son-editor-backend/).

## License

Son-editor is published under Apache 2.0 license. Please see the LICENSE file for more details.

## Lead Developers

The following lead developers are responsible for this repository and have admin rights. They can, for example, merge pull requests.

* Manuel Peuster (https://github.com/mpeuster)

## Contributors

* Hadi Razzaghi Kouchaksaraei (https://github.com/hadik3r)
* Sevil Dräxler (https://github.com/mehraghdam)
* Jonas Manuel
* Christian Korfmacher
* Linghui Luo
* Surendra Kulkarni


## Feedback-Channel

* You may use the mailing list [sonata-dev@lists.atosresearch.eu](mailto:sonata-dev@lists.atosresearch.eu)
* [GitHub issues](https://github.com/sonata-nfv/son-editor-backend/issues)


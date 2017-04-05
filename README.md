[![Build Status](https://travis-ci.org/sonata-nfv/son-editor-backend.svg?branch=master)](https://travis-ci.org/sonata-nfv/son-editor-backend.svg?branch=master)


# son-editor-backend

## Installation

## Development

### Testing

### Continous Integration

## Dependencies

## Contributing

## Further Documentation

## License

## Lead Developers

## Contributors

## Feedback-Channel


######################

Student project group's network service editor backend.

The backend serves as the data storage for the editor and interacts with all other services that are needed to create, update and release SONATA Service and VNF descriptors. It is designed to be used with the [son-editor-frontend](https://github.com/sonata-nfv/son-editor-frontend) but because all interaction and communication is taking place through a RESTful API, it should also be possible to be used with other user interfaces.

The API can be viewed from [the root directory of the backend](http://fg-cn-sandman1.cs.upb.de:5000/)

## Installation

The easiest way to install and run the Editor Backend is by using [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/):

1. Download the repository
  * `git clone https://github.com/sonata-nfv/son-editor-backend`
2. Configuration  
  To use the Github OAuth login feature, an application token must be created and configured in the editor.  
  To do this go to your Github Settings > [OAuth applications](https://github.com/settings/developers) and 'Register a new application'  
  **Example:**  
    **Application Name:** SONATA Editor  
    **Homepage URL:** https://github.com/sonata-nfv/son-editor-backend  
    **Application description:** This is the SONATA Editor  
    **Authorization callback URL:** http://your.domain.com:<b>5000/login</b>  
    
  After creating the application copy and paste the ClientID and the Client Secret into their respective fields in the configuration file located at [src\son_editor\config.yaml](src/son_editor/config.yaml)  
  **session > secretKey:**  A random string used to encrypt the session  
  **frontend-redirect:** "/loginRedirect.html" the path to the loginRedirect.html page of the frontend editor that will be opened after the Github authentication.  
  **frontend-host:** The domain and possibly port of the frontend server  
  **allowed-hosts:** If the front and backend are deployed on different domains, the frontend domain must be listed here
  
  The standard port for the editor backend when starting it via `docker-compose` is **5000**. If the port is changed, also the port of the **Authoritzaion callback URL** must be changed.
3. Deploy  
  To deploy the editor start the docker container by running `docker-compose up -d' in the root of the project.  
4. Enjoy  
  The backend server is now running at your configured domain and will provide a documented api description at the root path. E.g.  http://your.domain.com:5000
  
For instructions on how to setup the web frontend of the editor please visit https://github.com/sonata-nfv/son-editor-frontend for more information.


## Development configuration
### Python environment
We recommend using [venv](https://docs.python.org/dev/tutorial/venv.html). If you have setup your python 3 environment, open a shell in your virtual environment
and install [son-cli:v2](https://github.com/sonata-nfv/son-cli/tree/v2.0).

### Test configuration
 
Edit config.yaml and fill in the requested values under the test section. If you are using travis ci or another build server, note that the github credentials to 
test github configuration can be set as environment variables "github_bot_user" and "github_access_token".
If you leave out test configuration, some tests will eventually fail. 

## Manual Updates
 To update the editor backend just run  
  `docker-compose down`  
  `git pull`  
  `docker-compose build --no-cache`  
  `docker-compose up -d`

### Known Issues:
If the database design changes it may happen that the automated deployment fails due to the old database not conforming to the new schema. If this is the case, the docker container should be torn down and rebuild as described in the Manual Update section. The data is preserved by writing the descriptors onto disk and the database will automatically be rebuilt by scanning the workspaces on startup.
  
## Documentation
The server code is documented using sphinx: [documentation](https://cn-upb.github.io/upb-son-editor-backend/)

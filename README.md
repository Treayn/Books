# Books-API
Service to pull data off O'Reily API.

## Setup
- Install `python 3.8` or greater, `pip`, `kubectl`, `helm`, and `minikube`.
- Minikube will prompt you to add your username to the docker group: `sudo usermod -aG docker $USER`
- `git clone this repo`
- `cd ./Books`
- `chmod 755` all scripts in `./cicd/scripts/*` to allow then to be executed.

### Run locally
- ./cicd/scripts/run_local.sh
- Navigate to localhost/books in your browser.

### Run on minikube
- `minikube start` to bring up minikube cluster.
- `./cicd/scripts/deploy_minikube.sh` to deploy books-app to cluster.
- `deploy_minikube.sh` will report a url that can be used to access the service in the cluster.

### Endpoints
- `./cicd/scripts/post_data.sh` will allow for test data to be posted to `/books`.
- A get request to `/books` will return all books relevant to the topic of Python.
- A get request to `/books/<isbn>` will return the entry associated with that isbn.
- `/docs` will take you to the Swagger API detailing all this.

### Additional details
- This project runs on the FastAPI web server.
- Minikube is used to spin up a local cluster.
- Container on Docker Hub at `https://hub.docker.com/r/treayn/books`

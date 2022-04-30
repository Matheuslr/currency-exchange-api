# eng-gruposbf-backend-python

Python FastAPI and MongoDB

## Technologies
- Python 3.9
- FastApi - Framework
- Motor - Asynchronous Python driver for MongoDB
- Docker - Project Structure
- Docker-compose - Development Environment
- MongoDB - Development Database
### Docker

1. Clone this repository

2. To copy `.env.example` to `.env`, run: `make copy-envs`

3. Build docker image and run migrates: `make build`

4. Run api: `make run`

5. In your browser call: [Swagger Localhost](http://localhost:8000/docs)

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
# ELIMINATION TOURNAMENT API

an Elimination tournament API with python django following Clean architecture Principles 

## Install and configuration

### with Docker

Requires Docker and docker-compose installed. 
1. Download and Install docker
    - [MacOS](https://www.docker.com/products/docker-desktop) 
    - [Debian](https://docs.docker.com/engine/install/debian/#installation-methods)
    - [Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
2. [Download and Install docker-compose here](https://docs.docker.com/compose/install/)

In root directory run ```docker-compose up```. App will start and run in port localhost:3000

#### Debug

Run bash inside the application container. Run ```docker exec -it djangoapp bash``` in another terminal while the container is running.


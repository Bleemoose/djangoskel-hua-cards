## HUA EMPLOYEE TIME TRACKING SYSTEM

### About
This project as thesis assigment and it's based on the huaskel authentication project. This application has been designed with the usage of physical Arduino card reader stations in mind and you can see a demo video [here](https://youtube.com/shorts/gB4t8IPaMvY?si=TU-KzXlb7p9TNzX9)

### Prerequisites
You need to have `docker` and `docker-compose` installed in your system. For Ubuntu check out:

- https://docs.docker.com/engine/install/ubuntu/
- https://docs.docker.com/compose/install/

### IMPORTANT!
You also need to be connected to the University's VPN in order for the Django container to be able to access the openldap directory. Otherwise authentication will not work, at least out-of-the-box.

### Bind distinguished name (DN)
Once you install `docker` and `docker-compose` you need to create a file `.env` containing your bind distinguished name (DN) and your user password. The Django app needs these credentials to carry out user searches at the University's openldap. A sample `.env` file can be found `.env.template` in the repo's root folder. Change this with your own credentials. Remember to stay connected at the university's VPN service to be able to access the openldap server!

### Djangoskel containers
The project uses three containers described in detail in the `docker-compose.yml` file:

- `postgres` is a standard PostGreSQL container that can be build from the official Docker archives. In production environments consider removing the `ports` statement which exposes the PostGreSQL port at the host.

```yaml
    ports:
      - "5432:5432"
```

- `nginx` is a standard nginx container that can be build from the official Docker archives. In production environments consider removing the `ports` statement which exposes the Gunicorn port at the host.

```yaml
    ports:
      - "8000:8000"
```

- `web` is the main Django application container that can either run the Django development server or the Gunicorn application server. The latter should be chosen for production environments. This container is build from  `Dockerfile` included in the root folder.


### Where does the code live?

The code lives in the `code/` folder of the root directory. This is volume-mounted in the `web` container. It already contains a Django project named `djangoskel` for testing purposes. It is highly advisable to start your own project and copy the `djangoskel` files to your new project folder inside 'code/'

### Data persistence

The folder `data/` is volume-mounted to the `postgres` container to enable database persistence when the container is stopped.

### Running the containers

You can run the containers using the `docker-compose` command at the root folder:

```bash
docker-compose up
```


### Application site URL 

The Django site is accessible though http at `http://localhost`. If you are running the development server, you can also use `http://localhost:8000`

### Admin site URL

The Django admin site is accessible though http at `http://localhost/admin`. If you are running the development server, you can also use `http://localhost/admin:8000`. The admin user credentials are defined as environment variables in the `docker-compose.yml` file.


### Logging

All loging is being carried out in the `logs/` directory









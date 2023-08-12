## Djangoskel: A containerized environment for developing Django applications for HUA

### About
This project can be used to create Django projects in the context of undergraduate / postgraduate theses or even production applications for the Harokopio University of Athens

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

### Using additional Python modules

You will most likely need to install additional `Python` modules at the `web` container. To do this, modify the `requirements.txt` file located at the root folder. 

### Adding Linux modules

There may also be circumstances where you need to install an additional `Linux` package in order for the module to work. Do this at the `Docker-file` adding the package name to the first `RUN` command

```
RUN apt-get update && apt-get install -y curl apt-utils apt-transport-https debconf-utils \
    gcc build-essential libsasl2-dev python-dev libldap2-dev libssl-dev ldap-utils python3-pip \
    netcat net-tools gettext
```

Note that the container start from a standard Ubuntu 20.04 image and uses the non-interactive front-end. If you need to pass options during the installation process you need to pass these using `debconf`

### Where does the code live?

The code lives in the `code/` folder of the root directory. This is volume-mounted in the `web` container. It already contains a Django project named `djangoskel` for testing purposes. It is highly advisable to start your own project and copy the `djangoskel` files to your new project folder inside 'code/'

### Data persistence

The folder `data/` is volume-mounted to the `postgres` container to enable database persistence when the container is stopped.

### Running the containers

You can run the containers using the `docker-compose` command at the root folder:

```bash
docker-compose up
```

If you make changes to `Dockerfile` or the `requirements.txt` file you should rebuild the containers using:
```bash
docker-compose up --build
```

The containers should be shutdown gracefully using:

```bash
docker-compose down
```

### Application site URL 

The Django site is accessible though http at `http://localhost`. If you are running the development server, you can also use `http://localhost:8000`

### Admin site URL

The Django admin site is accessible though http at `http://localhost/admin`. If you are running the development server, you can also use `http://localhost/admin:8000`. The admin user credentials are defined as environment variables in the `docker-compose.yml` file.

### Code editing 

You can edit the code directly on the host in the `code/` directory.

### Logging

Some rudimentary logging is carried out in the `logs/` folder. You should definitely add logging information to your own views

### Connecting to the Django container

You will surely need to run some commands using the `django-admin` or `python manage.py` at the Django container. To open a Bash terminal to the container use:

```bash
docker exec -it web /bin/bash
```

Make sure the container is running. Use this when for example you need to create a new Django app or build the translation dictionaries (see below)

### User model and authentication backend

The project comes with an `accounts` application that can be used to login HUA users through the university's openldap server. Users are required to login using their e-mail. 
- If the user e-mail ends with `@hua.gr` then authentication is deferred to the openldap server and if successful an instance of the `User` model is created including information drawn from the server such as the `title` and `department` fields. Using these fields you can handle authorization. 
- If the user e-mail does not end with '@hua.gr' then user authentication is carried out using the user instances stored in the PostgreSQL data-base. This can be useful when you are required to include external users, not contained in the openldap server.

### Internationalization

The project uses the default Django internationalization and translation tools. Check out the official documentation, e.g. https://docs.djangoproject.com/en/3.2/topics/i18n/translation/ and various tutorials on the internet. 

### Front-end

Bootstrap4 is pre-installed in the `accounts` templates. The Python module `django-crispy-forms` is already installed and can be used to make Bootstrap4 forms with (relative) ease. You can also use other front-ends including: --

- Angular (https://medium.com/swlh/django-angular-4-a-powerful-web-application-60b6fb39ef34) 
- React (https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react)


### Security

Do not leave the application running while not working on the code, especially if you are using the development server (which is used by default) since the host's 80 port (and others) are exposed. Issue a `docker-compose down` if you are not developing!









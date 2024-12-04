# Running the app in production
The following sections address topics, which come up when running the Application in production.

Since the `Wissensplattform` and the `CityGML Visulizations` app were developed independently, there are different deployment possiblities. Both apps can be used indipendently or together. In the following sections the different deployment strategies are described.

## High level structure
In this section the structure of the different repositories is shown. 
In general, there is the [wissen-digital-ewb repository](https://github.com/TUB-DVG/wissen-digital-ewb), the [djangoCesium repository](https://github.com/TUB-DVG/djangoCesium) and a [integration respository](https://github.com/TUB-DVG/integration-repo-cesium-ewb-wissen).
```{mermaid}
graph TD
    integration-repo-cesium-ewb-wissen["integration-repo"]
    wissen-digital-ewb["wissen-digital-ewb"]
    djangoCesium["djangoCesium"]

    integration-repo-cesium-ewb-wissen -->|webcentral/| wissen-digital-ewb
    integration-repo-cesium-ewb-wissen -->|djangoCesium/| djangoCesium
```
The above figure shows how the two independent repositories are included into a integration repository, which is used to deploy the two applications together. 
In the following sections the different deployment types are described in detail.


## Running Wissensplattform without CityGML visulizations
At first, the deployment of the `Wissensplattform` without the `CityGML visulizations` app is discussed. 
In general, the production mode of the application can be seen as a security hardend version of the development mode. This includes the security on the container level or web security features like HTTPS and CSP.

### HTTPS
Using the HTTPS protocol allows to encrypt the HTTP pakets going through the unsecure internet. Since many browsers today have implemented a HTTPS-only mode and using HTTP is generally flagged unsecure, the production mode of the `Wissensplattform` implements a HTTPS only mode. That means that only connections using HTTPS can be established. To enable the `nginx`-webserver to encrypt and decrypt traffic, a SSL-certificate and a private key needs to be given. These 2 files need to be stored in `nginx/conf/`-folder. Furthermore the filenames have to be provided inside the `.env`-file. The following code listing shows an example on how to add the filenames of the certificate and key file to the `.env`-file:
```
NGINX_SSL_CERTIFICATE_FILENAME=ssl_certificate.crt
NGINX_SSL_CERTIFICATE_KEY_FILENAME=private_key.key
```

### General procedure
1. Copy the certificate and private key file, like shown in the previous section.
2. Build the app: This needs to be done, since the certificate- and private key file needs to be copied into the `nginx` docker image:
```
./run build_initial prod
```
If on the computer you are deploying the `EWB Wissensplattform` a deployment has already be made, a database is already present inside a docker volume. 
#### Already present database
If this is the case you can just start the `EWB Wissensplattform` in the forground of the terminal you are using or in the background using `docker compose` together with the `-d` flag:
3. You can use the `run`-script:
```
./run up prod
```
This starts the application in production mode in the foreground of the terminal.
Or you can use the `docker compose` syntax:
```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
```{note}
The docker compose command is not fully equivalent to the run-script command since the -d flag is added, which detaches the compose command from the current terminal. If you like to keep the execution in the foreground of the current terminal you can skip the -d flag.
```
#### Newly created database
If there is no database present the following steps need to be done: 
3. Use the present dump in the `postgres/`-folder or a dump which was created in the past. You can either use the `run`-script with the `up_initial` command or a series of run-script commands, which will be described in the following:
```
./run up_initial prod postgres/dump_filename.sql 
```
The above command is a convience command, which executes the following actions: Starting the application, importing the dump with the name `dump_filename.sql` from the `postgres/` folder and restarting it to bring the `EWB Wissensplattform` into a healthy state.
Alternativly all the steps to import the dump can be done manually:
3. Start the application:
```
./run up prod
```
4. Open a second terminal and navigate to the root-folder of the project.
Executing the following command will load the dump with the filename `dump_filename.sql` from the `postgres/`-folder:
```
./run restore_db postgres/dump_filename.sql
```
5. After the import process has been completed, the web application needs to be restarted. To do that please switch back to the terminal where the `EWB Wissensplattform` is running and stop it using `CTRL+C`. After that restart it using:
```
./run up prod
```
or 
```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
to start it in detached mode in the background.
Optional:
Logos of tools, protocols, datasets and technical-standards are saved inside a seperate docker voume called `static-data`. These files need to be copied into the volume. In the following it is assumed, that the image files are locate inside a folder `webcentral/src/media/`. Then the following commands can be used to copy the images into the volume:
```    
source .env
docker cp webcentral/src/media/. webcentral:/home/$WEBCENTRAL_UNPRIVILEGED_USER/webcentral/media/
```
First the envionmental variables inside the `.env` file need to be loaded. Afterwards the images inside the `media` folder are copied into the container.
```{note}
It was assumed, that the command is executed from within the root folde root folder of the repository.
```
## Deploying the DjangoDesium-application without the Wissensplattform
The `DjangoCesium` application is build from 3 containers, the `frontend`-, `djangodb`- and the `citydb`-container. The `frontend` container holds a modified version of the [3DCityDB-web-map-Client](https://github.com/3dcitydb/3dcitydb-web-map), which uses [Cesium](https://cesium.com/) to show a virtual globe in the browser window. In that globe 3D building visulizations are displayed. To these 3D building visulizations demand timeseries can be simulated and saved in a [3DCityDB](https://www.3dcitydb.org/3dcitydb/) database instance. The saved timeseries can be shown by clicking the 3D building visulization in the browser window. That triggers a API call to the `djangodb` backend container, which fetches the timeseries from the database and returns them to the frontend inside a HTTP response.

## Cache busting techniques
When developing the application in an agile manner lots of changes will be introduced to the web application when its already running publicly. Because of that problems can arise. One problem has to do with the client browser caches static files (javascript/stylesheet-files) to reduce loading time. This can lead to websites look broken for clients re-visiting the website since the still use the old cached versions. 
To address that problem a static files bundler `webpack` is used. It transpiles the `scss`-files into one `css`-file. A hash-value is also put into the filename. The also installed package `wepback-bundler-tracker` creates a file `weback-stats.json` where the location of the created css-files is stored. The stats file is then used by the package `django-weback-loader` to insert the most up-to-date file in stylesheet link tag in the django templates.

The configuration of `django-weback-loader` is done in the `settings.py`-file. There, the following lines were added:
```python
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '/webpack_bundles/',
        'CACHE': not DEBUG,
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
    }
}
```
The location of the transpiled bundles are specified in the `BUNDLE_DIR_NAME` constant. The location specified must be reachable from within the location specified in the `STATICFILES_DIR` constant.
The location of the `webpack-bundler-loader` stats-file is specfied in `STATS_FILE`. A absolute path is taken as input. Furthermore the intervall in which changes in the stats file are checked can be set via `POLL_INTERVAL` in seconds. Polling is only activated if the django `DEBUG`-flag is set to true. `DEBUG` beeing `True` typically means that django is executed in a development environment, and `DEBUG` equals `False` is set on a production instance.  




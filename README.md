# CC Travel/Blog App

This app is a travel blog which retrieves live information regarding the weather and popular images from external APIs.
The app also has an internal API where you have the ability to view, add and delete existing blog entries that in the app. Information is returned in a JSON format.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need the following before continuing:

* Linux distributed platform
* Text Editor

The requirements file contains all the modules needed for the app.

```
pip>=9.0.1
Flask==0.12.2
requests
requests-cache
cassandra-driver
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

Open command line and navigate to the directory of the folder where the app is stored.

Create a virtual environment with your preferred name with the following command.

```
python3 -m venv name_of_project
source name_of_project/bin/activate
```
The virtual environment needs to be activated with this command:
```
source name_of_project/bin/activate
```

From the app directory, run the following command:

```
python -m pip install -U -r requirements.txt
```
This command recursively installs/updates the modules in the requirement.txt in the local environment.

**Ensure these two lines are removed:**
```
cluster = Cluster(['cassandra'])
session = cluster.connect()
```

You should now be able run the app:

```
python travelapp.py
```

This is successful if the terminal is displaying the following:

```
* Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 442-044-743
```
Clicking on the link should take you to the website.



## Deployment

You will need the following before continuing:

* Docker
* Kubernetes

This section will detail how to get this app ready for a cloud environment. For example, Google Cloud
Once the directory is uploaded, run the docker build command in the directory of the app:

```
docker build -t gcr.io/${PROJECT_ID}/name_of_app:v1 .
```
Once built, It will need to be pushed:
```
docker push gcr.io/${PROJECT_ID}/name_of_app:v1
```
After being pushed, the service needs to be run and exposed:
```
kubectl run pokemon-app --image=gcr.io/${PROJECT_ID}/pokemon-app:v1
--port 8080
kubectl expose deployment pokemon-app --type=LoadBalancer --port 80
--target-port 8080
```
Check services for the IP address

## Built With

* [Cassandra](http://cassandra.apache.org/doc/latest/) - Database used
* [Flask](http://flask.pocoo.org/docs/1.0/) - Web framework used
* [Apixu](https://www.apixu.com/api.aspx) - Used to retrieve weather
* [Pixabay](https://pixabay.com/api/docs/) - Used to retrieve images


## Authors

* **Inih Marcus** - *Initial work* - [Inih](https://github.com/inih)


## Acknowledgments

* Thanks for the teaching and the material Arman & Felix!

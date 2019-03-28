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

This project will assume you're deploying this within Google Cloud and using Kubernetes
You will need the following before continuing:

* Docker
* Kubernetes
* CSV file with the following as the **header** (Test data should be included)
  * Passage, Location, Title

This section will detail how to get this app ready for a cloud environment. This uses Google Cloud as the platform.

Within the 'Cassandra Services' folder are 4 files. The following will need to be executed (We'll come back to the last).
```
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml
```
Check the container is running correctly
```
kubectl get pods -l name=cassandra
```

To make it easier, we can copy the test CSV into the cassandra pod it save time from typing it out.
```
docker cp {NAME OF CSV FILE}.csv cassandra-{POD NUMBER}:/{PATH OF CSV FILE}/{NAME OF CSV FILE}.csv
```
Pick any 'cassandra' pod and execute the following command to add a new table and data
```
kubectl exec- it cassandra-{POD NUMBER} cqlsh
```
Execute the following command to create the DB
```
CREATE KEYSPACE travelrecords WITH REPLICATION = {'class':'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE travelrecords.posts (passage text, location text, title text PRIMARY KEY);

COPY travelrecords.posts(Passage, Location, Title) FROM '/test.csv' WITH DELIMITER=',' AND HEADER=TRUE;
```

In the previous section, these two lines were commented out:
```
cluster = Cluster(['cassandra'])
session = cluster.connect()
```
Ensure that this is not commented out.

Build the image and push it to the Google Repository
```
docker build -t gcr.io/${PROJECT_ID}/travelapp:v1 .

docker push gcr.io/${PROJECT_ID}/travelapp:v1

```

Run the following commands
```
kubectl run web --image=gcr.io/{PROJECT_ID}/travelapp:1.0 --port=8080

kubectl expose deployment web --target-port=8080 --type=NodePort

kubectl apply -f basic-ingress.yaml

```
*If the service name is changed, make sure that change is reflected in the basic-ingress.yaml file*

Wait for the external IP address by getting services
The directory will need to be uploaded within the 'home' directory

Run the following docker build command in the directory of the app:

Once built, It will need to be pushed:

After being pushed, the service needs to run and exposed:
```
kubectl run travel-app --image=gcr.io/${PROJECT_ID}/travelapp:v1
--port 8080
kubectl expose deployment travel-app --type=LoadBalancer --port 80
--target-port 8080
```
Check services for the IP address

## Built With

* [Cassandra](http://cassandra.apache.org/doc/latest/) - Database used
* [Flask](http://flask.pocoo.org/docs/1.0/) - Web framework used
* [Apixu](https://www.apixu.com/api.aspx) - Used to retrieve weather
* [Pixabay](https://pixabay.com/api/docs/) - Used to retrieve images
* [Kubernetes](https://kubernetes.io/docs/home/) - Distribute web service


## Authors

* **Inih Marcus** - *Initial work* - [Inih](https://github.com/inih)


## Acknowledgments

* Thanks for the teaching and the material Arman & Felix!

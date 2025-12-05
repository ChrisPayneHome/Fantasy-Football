# Fantasy Football Analytics

This repo contains code for a data analytics project around fantasy football data.

## Proposed Architecture

The porposed architecture for the project will look like this:


```mermaid
architecture-beta
	group kube(cloud)[Kubernetes]

	service api(cloud)[Fantasy API]
	service db(database)[Postgres Database] in kube
	service app(server)[Web UI]

	api:L -- db:R
	db:T -- app:B
	 
```

# Fantasy Football Analytics

This repo contains code for a data analytics project around fantasy football data.

## Proposed Architecture

The porposed architecture for the project will look like this:


```mermaid
flowchart LR
    subgraph kube[Kubernetes]
        db[(Postgres Database)]
        ml(ML Endpoint)
        app[Web UI]
    end

    api[Fantasy API]

    api --> db
    db --> app
    db --> ml
    ml --> db
```

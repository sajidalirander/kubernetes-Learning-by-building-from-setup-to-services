## PostgreSQL Deployment and Service
The process will feel very familiar, as we'll follow the same declarative, file-based approach we used for [MinIO](./ch3.md). We'll need to create a blueprint for each of the four main components:
* A `Secret` for the database password. Read and follow the instruction carefully at [Creating Secret](../postgres/build/create_secret.md).
* `Persistent Storage` (a PV and a PVC) for the database files.
* A `Deployment` to run the PostgreSQL container.
* A `Service` to expose the database within the cluster.

Just like with MinIO, the first step is to securely handle our credentials.
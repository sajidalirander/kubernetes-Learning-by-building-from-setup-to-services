For MinIO to store its data, it needs to claim a `Persistent Volume`. In a production cloud environment, we'd use a `StorageClass` to create a cloud disk automatically. Since we're on a single node for learning, we'll create a simple PV by hand using a directory on your local server.

To be clear, instead of connecting to an external MinIO cloud service, we'll deploy the official MinIO software inside our Kubernetes cluster. This way, we're still managing it with Kubernetes, but we're not tied to a specific local directory.

You have two important pieces of information we need to manage:
* The endpoint (localhost:9090)
* The credentials (access_key and secret_key)

Kubernetes has a secure way to handle these. We'll use a `Kubernetes Secret` to store the access and secret keys.

Here's the plan:
* Create a Kubernetes Secret to securely hold your minioadmin credentials. Read and follow the instruction carefully at [Creating Secret](../minio/build/create_secret.md).
* We need a place for MinIO to store its files. For this learning exercise, we'll create a `Persistent Volume` using a directory on your node. This is a necessary step to ensure the data isn't lost if the MinIO pod restarts. Explore how to [make the persistent volume](../minio/build/make_pv.md). This will be a three-step process:
    * Create a directory on your server to act as our `"storage"`.
    * Create the `PersistentVolume` (PV) by telling Kubernetes about this directory.
    * Deploy MinIO with a `PersistentVolumeClaim` (PVC) to request and use that PV.
* Deploy MinIO using its official container image. We'll create a `Deployment` to manage the MinIO pod. Let's dive in and [Run MinIO Pods](../minio/build/deploy_minio.md).
* a `Service` to give it a stable network address inside the cluster (like minio-service:9090). Read the next lesson to create a [Kubernetes Service](../minio/build/service.md) to expose it. 

This approach keeps everything managed by Kubernetes and prepares you to connect your Python code to it later.
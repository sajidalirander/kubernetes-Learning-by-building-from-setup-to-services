## PostgreSQL Deployment 
We need another blueprint is the Deployment. This file will bring everything together: it will tell Kubernetes to run the `PostgreSQL` container, connect it to the secret you made, and attach the persistent storage you just claimed.

## Creating YAML for Deployment
Let's create the YAML for the PostgreSQL Deployment.

This blueprint will look very similar to the one we made for MinIO. It will tell Kubernetes to:
* Run the official postgres container image.
* Use the postgres-secret to set the username and password.
* Attach the postgres-pvc to store the database files.

### First, create the new file:
```bash
nano postgres-deployment.yaml
```

### Now, copy and paste this YAML:

File: [PostgreSQL Deployment](../config/sql-dep.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:latest
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: POSTGRES_USER
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: POSTGRES_PASSWORD
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

Notice how the `env` and `volumes` sections are set up just like they were for MinIO. This file has one small but important difference in the `volumeMounts` section. For MinIO, we mounted the data to `/data`. Here, we're mounting it to `/var/lib/postgresql/data`.

> Any idea why we need to use this specific, longer path for PostgreSQL?

Each container image has a default directory where it expects to store its data. For the official postgres image, that location is `/var/lib/postgresql/data`. It's a predefined path set by the creators of the image.

So, when we create the `volumeMount`, we're essentially telling Kubernetes, "Take our persistent storage and make it appear at the exact spot inside the container where `PostgreSQL` is expecting to find its database files."

You've got a handle on all the components. Go ahead and save the file and apply it.

```bash
kubectl apply -f sql-dep.yaml
```

Just like with MinIO, it will take a moment for the node to download the `postgres:latest` image and start the container.


## Case Study
> What kubectl command will you use to check the status of your new `PostgreSQL` pod?

```bash
kubectl get pods
```
That's the command to see a list of all the pods in your current namespace.

```bash
sajid@sajid:~$ kubectl get pods 
NAME                                   READY   STATUS    RESTARTS   AGE
minio-deployment-69849b9879-42cg6      1/1     Running   0          106m 
postgres-deployment-7f6c687f8b-dhl2s   1/1     Running   0          2m35s
```

Kubernetes creates a unique name for each pod by taking the Deployment's name and adding a random string of characters to the end.

In case to get the specific pod status, run the following command with the name of the pod:
```bash
sajid@sajid:~$ kubectl get pod postgres-deployment-7f6c687f8b-dhl2s
NAME                                   READY   STATUS    RESTARTS      AGE
postgres-deployment-7f6c687f8b-dhl2s   1/1     Running   1 (45h ago)   45h
```

In case if you want to specify the database name or other varibles, read the guide to [Set the Environment Variable](../utils/set_env_variable.md).
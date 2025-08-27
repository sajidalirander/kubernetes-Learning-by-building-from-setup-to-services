## PostgreSQL as a Service
Now, for MinIO, we used a `NodePort` service because we wanted to access its web console from our browser (outside the cluster).

> But for a database, do we usually want to expose it directly to the outside world, or just to other applications running inside the cluster?

It's a best practice to keep your database private and only accessible to your applications inside the cluster. For this kind of internal communication, we use the default and most common service type: `ClusterIP`.

A `ClusterIP` service creates a stable, internal IP address that is only reachable from within the Kubernetes cluster. Think of it as a private phone extension that only employees inside the office can dial.

## Create a YAML
Let's create the final blueprint for our PostgreSQL setup.

### First, open the new file in your editor:
```bash
nano postgres-service.yaml
```
### Now, copy and paste this YAML: 

File: [PostgreSQL Service](../config/sql-service.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - protocol: TCP
    port: 5432
    targetPort: 5432
```
This will create the internal `ClusterIP` service for our database.. Take a look at this YAML. Compared to the [MinIO Service YAML](../../minio/config/minio-service.yaml), you'll notice one important line is missing from the spec section.

> What is it, and why do you think we don't need it here?

The missing line is `type: NodePort`. When you don't specify a type in a `Service YAML`, Kubernetes automatically uses the default type, which is `ClusterIP`. This is a convenient shortcut. Since `ClusterIP` is the most common type of service, you only need to specify the type when you want something different, like `NodePort`.

You've got a great handle on this. Go ahead and save the file and apply it to create the service.

```bash
kubectl apply -f sql-service.yaml
```


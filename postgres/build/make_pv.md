## Persistent Storage for PostgreSQL
This will be a two-part process, just like with MinIO:
* Create the `PersistentVolume` (PV).
* Create the `PersistentVolumeClaim` (PVC).

## Persistent Volume 
Here's the blueprint for the `PersistentVolume`. Since `PostgreSQL` is a database, let's give it a bit more space, say 10 gigabytes.

### First, create the storage directory on your server:
```bash
sudo mkdir -p /mnt/postgres-data
```

### Now, create the YAML file:
```bash
nano postgres-pv.yaml
```
And here's the content to paste inside.

File: [PostgreSQL PV](../config/sql-pv.yaml)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgres-pv
spec:
  capacity:
    storage: 10Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  storageClassName: local-storage
  local:
    path: /mnt/postgres-data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - <your-node-name-here>
```

> Based on the file we created for MinIO, do you see the one important value you'll need to change to make this work for your specific setup?

You should update the `values: - sajid`. You must correctly update the `nodeAffinity` with your specific node name. Go ahead and save that `sql-pv.yaml` file. 

> What's the command to apply it?

The command is `kubectl apply -f sql-pv.yaml`. Go ahead and run it to create the `PersistentVolume`.

That's a wrap. You've officially set aside that `/mnt/postgres-data` directory as a piece of storage your cluster can use.

But a `PersistentVolume` is just the supply of storage. We still need a way for an application to request it.

> Based on our earlier discussion about the "backpack" analogy, what's the name of the Kubernetes object that makes a request for storage?

The `PersistentVolumeClaim` (PVC) is the object a pod uses to formally request storage from the cluster. So, to complete our storage setup, we need to create one more YAML file for the PVC. This will act as the bridge between our `PersistentVolume` and our future PostgreSQL `Deployment`.

## Persistent Volume Claim
Now that we have the `PersistentVolume`, we need to create the claim. This blueprint will request the 10-gigabyte volume we just created.

### First, create the YAML file:
```bash
nano postgres-pvc.yaml
```
### Then, copy and paste this content: 

File: [PostgreSQL PVC](../config/sql-pvc.yaml)
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: local-storage
```
Notice how the `storage` and `storageClassName` match the PV we just made.

> Once you've saved that file, what's the command to apply it?

```bash
kubectl apply -f sql-pvc.yaml
```
Go ahead and run it to create the claim.

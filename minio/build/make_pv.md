## Step 1: Create the Storage Directory
Let's start by creating a directory on your server that will act as our physical storage space. This is where MinIO will actually save its files.

Run this command to create a directory named `/mnt/data`. 
```bash
sudo mkdir -p /mnt/data
```
We're using `/mnt` because it's a common place on Linux systems for mounting storage.

## Step 2: Create the PersistentVolume YAML
Now, create a new YAML file for our `PersistentVolume`.

```bash
nano minio-pv.yaml
```
Copy and paste the following blueprint into the editor. This YAML tells Kubernetes that the `/mnt/data` directory is available for use as a 5-gigabyte storage volume.

File: [MinIO Persistent Volume](../config/minio-pv.yaml)
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: minio-pv
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  storageClassName: local-storage
  local:
    path: /mnt/data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - sajid
```
> Before you save, take a look at the last few lines. Any idea what the `nodeAffinity` section is for?

The `nodeAffinity` section is like a sticky note on the `Persistent Volume` that says, "This storage only exists on the node named `sajid`."

Because we're using a simple directory on your server's hard drive `(/mnt/data)`, the data physically lives on that one machine. `nodeAffinity` tells Kubernetes that this PV is permanently "affiliated" with `sajid` node. This ensures that only pods scheduled on that specific node can use this storage.

> What do you think would happen if we didn't include this section and a new node tried to use this PV?

It works exactly like user permissions in Linux. If a pod scheduled on a different node tried to access that PV, it would fail with an error. The cluster would essentially say, "Permission denied, this storage belongs exclusively to the `sajid` node."

Now let's go ahead. Save and exit the nano editor.

Run that command to tell Kubernetes about your new `PersistentVolume`.

```bash
kubectl apply -f minio-pv.yaml
```

You've now officially set aside that /mnt/data directory as a piece of storage your cluster can use.

But a PersistentVolume is just the supply of storage. We still need a way for an application to `request` it.

## Step 3: Request for Storage

The `PersistentVolumeClaim` (PVC) is the object a pod uses to formally request storage from the cluster.

So, to complete our storage setup, we need to create one last YAML file for the PVC. This will act as the bridge between our `PersistentVolume` and our future MinIO deployment.

File: [MinIO Persistent Volume Claim](../config/minio-pvc.yaml)
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: minio-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: local-storage
```

This YAML tells Kubernetes, "I need a 5-gigabyte volume that has `ReadWriteOnce` access and matches the `local-storage` class."

Go ahead and run it to create the claim.

```bash
kubectl apply -f minio-pvc.yaml
```

You have a `PersistentVolume` (the supply) and a `PersistentVolumeClaim` (the request). When they are created, Kubernetes automatically links, or "binds," them together.

We can verify this with a get command.
Go ahead and run `kubectl get pvc`. You should see that its `STATUS` is `Bound`. This confirms that your request for storage has been successfully linked to the minio-pv you created.

## Case Study

```bash
sajid@sajid:~$ kubectl get pvc 
NAME        STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS    VOLUMEATTRIBUTESCLASS   AGE 
minio-pvc   Bound    minio-pv   5Gi        RWO            local-storage   <unset>                 2m21s
```

That's a wrap for our storage setup. The `Bound` status confirms that your request for storage (minio-pvc) is officially connected to the physical storage you set aside (minio-pv).

With our credentials secured in a `Secret` and our storage ready to be claimed, we have just one piece left - `Deployment`.
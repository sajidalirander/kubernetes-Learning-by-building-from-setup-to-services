We need a blueprint that tells Kubernetes how to run the MinIO pods. In Kubernetes, that blueprint is called a Deployment.

A `Deployment` is like a manager for your pods. You tell it:
* I want to run the `minio/minio` container image.
* Make sure one replica is always running.
* Pass it the credentials from `minio-secret`.
* Attach the storage from `minio-pvc` to it.

The Deployment then takes care of the rest. If the pod crashes, the Deployment will automatically create a new one to replace it.

Let's create the YAML for the MinIO Deployment.

This file is the most complex one yet, but you'll see it's built from concepts we've already discussed. It tells Kubernetes how to run the `MinIO` pod, how to connect it to our `Secret`, and how to attach our `PersistentVolumeClaim`.

First, create the new file in your editor:

```bash
nano minio-deployment.yaml
```
Now, copy and paste this blueprint into the editor. Take a moment to read through it and see how the pieces connect.

File: [MinIO Deployment](../config/minio-dep.yaml)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: minio-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
      - name: minio
        image: minio/minio:latest
        command:
        - /bin/bash
        - -c
        - minio server /data --console-address :9090
        env:
        - name: MINIO_ROOT_USER
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: MINIO_ROOT_USER
        - name: MINIO_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: minio-secret
              key: MINIO_ROOT_PASSWORD
        ports:
        - containerPort: 9000
        - containerPort: 9090
        volumeMounts:
        - name: minio-storage
          mountPath: /data
      volumes:
      - name: minio-storage
        persistentVolumeClaim:
          claimName: minio-pvc
```

This file introduces a few new concepts, but one of the most important is the relationship between `volumes` and `volumeMounts`.

> Based on the YAML, what do you think is the difference between those two sections?

Let's use a simple analogy to make the distinction crystal clear:
* `volumes`: This section is like declaring which backpack you're bringing into the pod. It says, "This pod has access to a source of storage, and we'll call it minio-storage." It defines the storage that is available to the pod as a whole.
* `volumeMounts`: This section is for a specific container inside the pod. It's like unpacking the backpack and putting its contents on a desk. It says, "Take that backpack named minio-storage and make its contents accessible at the `/data` directory inside this container."

So, a pod has volumes, but a container has volume mounts.

> What do you think would happen if we defined a `volume` in our pod but forgot to add the `volumeMounts` section inside the container?

The volume would be attached to the pod, but since we didn't mount it, the container wouldn't know it's there. It would be like having the backpack in the pod but leaving it zipped up in a corner, completely inaccessible. The container would just use its own empty `/data` directory instead.

Go ahead, save the file, and apply it.

```bash
kubectl apply -f minio-deployment.yaml
```

You've just handed the blueprint for `MinIO` to your cluster's manager. The `Deployment` will now start the process of creating the pod.

This can take a minute or two as it has to download the minio/minio container image.

> What command would you use to check the status of your running pods and see if the MinIO pod is up and running?

When you run `kubectl get` without specifying a namespace, it automatically looks in the default namespace. Go ahead and run:

```bash
kubectl get pods
```

## Case Study
```bash
sajid@sajid:~$ kubectl get pods 
NAME                                READY   STATUS    RESTARTS   AGE 
minio-deployment-69849b9879-42cg6   0/1     Pending   0          7m11s
```

That's a very common status to see when a pod is first created. The `Pending` status means Kubernetes has accepted your `Deployment`, but it hasn't been able to start the container on a node yet.

To figure out why it's pending, we need to ask Kubernetes for more details about the pod. The command for this is `kubectl describe`. This command works on a specific object, so you always need to give it the full name.

Get the pod description:

```bash
kubectl describe pod minio-deployment-69849b9879-42cg6
```
The command needs to know what kind of object you're describing.

Think of it like this: in a school, there might be a student and a teacher both named "Alex." To know which one you're talking about, you'd say "Alex the student" or "Alex the teacher."

It's the same in Kubernetes. We need to tell describe what kind of object it's looking for. The right and singluar object name is `pod` here. 

The description of the minio-deployment pod is as follows: 

```bash
The container creation is failed. 
Events:   
Type     Reason            Age                   From               Message   
----     ------            ----                  ----               -------   
Warning  FailedScheduling  11m                   default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.   Warning  FailedScheduling  110s (x2 over 6m50s)  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling
```

The Events section tells us the story of `taint`. Read the [whole story and resolve](../utils/taint.md) the issue. 

You've successfully:
* Created a Secret to hold the credentials.
* Set up Persistent Storage so the data won't be lost.
* Created a Deployment to run the application.
* There's just one last step. Even though the pod is running, we can't access it from outside the cluster yet. We need to create a Kubernetes Service to expose it.
## Decode the error
Let's look at the key message: 1 node(s) had untolerated taint `{node-role.kubernetes.io/control-plane: }`.

This is Kubernetes's way of telling us about a safety feature. By default, the control-plane node has a `taint` on it.

## Understanding Kubernetes Taints
The system of Taints and Tolerations is how Kubernetes ensures that pods are only scheduled on appropriate nodes.

### Taints: The "No Trespassing" Sign
A Taint is a property you place on a node. It acts as a "repellent" to prevent pods from being scheduled there. Taints have three main effects:
* `NoSchedule`: No new pods will be scheduled on the node unless they have a matching toleration. (This is the one you encountered).
* `PreferNoSchedule`: The system will try to avoid placing pods on this node, but it's not a strict rule.
* `NoExecute`: This is the strongest. It will evict any pods that are already running on the node if they don't have a matching toleration.

### Tolerations: The "Permission Slip"
A Toleration is a property you place on a pod. It's like a special permission slip that allows a pod to be scheduled on a node with a matching taint.

The control-plane pods you saw earlier (etcd, kube-apiserver, etc.) all have a toleration built-in for that control-plane taint. That's why they were allowed to run on `sajid` node from the beginning. Our MinIO pod, however, didn't have this permission slip, so it was rejected.

So, you can see we had two ways to solve our problem:
* Remove the Taint from the node (the method we are going to use). This is like taking down the "No Trespassing" sign so anyone can enter.
* Add a Toleration to our MinIO pod's YAML. This would have been like giving our pod the special permission slip to enter the restricted area.

## Remove the Taint from node
A `taint` is like a "No Trespassing" sign that prevents normal application pods from being scheduled there. This protects the important control-plane components from being overwhelmed by user applications.

So, the scheduler is saying, "I can't place your MinIO pod here because this node is reserved for control-plane duties."

In our small, single-node cluster, the control-plane node can pull double duty. We just need to give it permission to run regular workloads. We can do this by removing the "No Trespassing" sign—the taint. The command to do that is `kubectl taint nodes`. 

Given that, and the taint information from the error message, how would you construct the full command to remove that specific taint from `sajid` node?

A taint has three parts: the key, the value, and the effect. The error message from kubectl describe gives us the whole thing:
```bash
node-role.kubernetes.io/control-plane:NoSchedule
```
Here, `NoSchedule` is the effect. It's what tells the scheduler not to place pods there.

With this information, the full format of the command is:
```bash
kubectl taint nodes <node-name> <taint-key>:<taint-effect>-
```
The `minus` sign at the very end is the key to removing the taint. Therefore, 
```bash
kubectl taint nodes sajid node-role.kubernetes.io/control-plane:NoSchedule-
```
Let's break it down:
* `kubectl taint nodes sajid`: "I want to change the taints on the node named sajid."
* `node-role.kubernetes.io/control-plane`: This is the key of the taint.
* `:NoSchedule`: This is the effect of the taint.
* `-`: This final minus sign is what tells the command to remove the taint.


Go ahead and run that command. Once it's done, check the status of your pods again with `kubectl get pods`. The scheduler should now be able to place your MinIO pod on the node.

## Case study

```bash
sajid@sajid:~$ kubectl taint nodes sajid node-role.kubernetes.io/control-plane:NoSchedule- 
node/sajid untainted 
sajid@sajid:~$ kubectl get pods 
NAME                                READY   STATUS              RESTARTS   AGE 
minio-deployment-69849b9879-42cg6   0/1     ContainerCreating   0          25m
```

The `node/sajid untainted` message confirms you've successfully removed the "No Trespassing" sign, and the pod's status immediately changed from `Pending` to `ContainerCreating`.

`ContainerCreating` means the scheduler has placed the pod on your node, and now your node is in the process of downloading the `minio/minio` image and starting the container. This can take a minute or two.

Run `kubectl get pods` again in a little while. What's the final STATUS you expect to see when it's ready?

```bash
sajid@sajid:~$ kubectl get pods 
NAME                                READY   STATUS    RESTARTS   AGE 
minio-deployment-69849b9879-42cg6   1/1     Running   0          36m
```

That's a wrap. Your MinIO pod is now officially running.

## Content of Pods
The pods you see with `kubectl get pods` are only the ones in the default namespace. 

To see all the pods, including the system ones you just created (like CoreDNS and Flannel), run this command:

```bash
kubectl get pods --all-namespaces
# or for short
kubectl get pods -A
```

It will give you the first real look at all the components that make up your running cluster.

```bash
sajid@sajid:~$ kubectl get pods -A 
NAMESPACE      NAME                            READY   STATUS    RESTARTS   AGE 
kube-flannel   kube-flannel-ds-r7j7t           1/1     Running   0          5m56s 
kube-system    coredns-55cb58b774-l67km        1/1     Running   0          26m 
kube-system    coredns-55cb58b774-tkn6k        1/1     Running   0          26m 
kube-system    etcd-sajid                      1/1     Running   8          26m 
kube-system    kube-apiserver-sajid            1/1     Running   11         26m 
kube-system    kube-controller-manager-sajid   1/1     Running   0          26m 
kube-system    kube-proxy-fnpzx                1/1     Running   0          26m 
kube-system    kube-scheduler-sajid            1/1     Running   13         26m
```

### Control Plane Pods
These pods, all in the kube-system namespace, make up the brains of your cluster:
* `etcd`: The cluster's database, storing all its configuration and state.
* `kube-apiserver`: The front door to your cluster. kubectl talks to this.
* `kube-controller-manager`: The "thermostat" that watches the cluster and makes sure reality matches your desired state.
* `kube-scheduler`: Decides which node a new pod should run on.

### Add-on Pods
These are pods that provide extra cluster-level services:
* `coredns`: The cluster's internal DNS service, so pods can find each other by name.
* `kube-proxy`: A networking component on every node that helps route traffic.
* `kube-flannel`: The pod network you installed.

> Based on the pods you saw running on your node a moment ago (like etcd, kube-apiserver, kube-scheduler), which role is your current node playing?

Because it's running all those core services in the kube-system namespace—especially the etcd database and the kube-apiserver—we know it's a control-plane node.

> You've got a great understanding of the architecture now. Shall we try deploying your very first application to your cluster?
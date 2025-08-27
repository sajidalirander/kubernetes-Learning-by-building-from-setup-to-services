## Installation of CNI Plugins
There are many CNI plugins available, but a great one to start with is `Flannel`. It's known for being simple and easy to set up.

To install it, we just need to apply its configuration file to our cluster using `kubectl`.

Here's the command:
```bash
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

Run that command, and then let's check the status of the nodes again with `kubectl get nodes`. It might take a minute or two for everything to start up and turn green. What do you see this time?

When you ran that `kubectl apply` command, you told your cluster to download and run the Flannel CNI (Container Network Interface). Flannel immediately created a set of pods that established an overlay network. This network acts like a virtual layer on top of your existing server network, allowing all the pods to communicate with each other, no matter which node they're on.

Once that network was up, the Kubernetes components on your control-plane node could finally talk to each other and pass their health checks. That's what caused the status to flip from `NotReady` to `Ready`.


## Cash Study
```bash
sajid@sajid:~$ kubectl get nodes 
NAME    STATUS   ROLES           AGE   VERSION 
sajid   Ready    control-plane   20m   v1.30.14
```

Your single-node Kubernetes cluster is now fully operational and ready for action.
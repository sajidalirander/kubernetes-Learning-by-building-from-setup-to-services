## Kubernetes Initialization
We're going to run the `kubeadm init` command. To do this correctly, we need to give it one important piece of information: an IP address range for the pods to use.

Kubernetes needs a dedicated network for its pods, and we have to tell it which block of IP addresses to reserve for them. We'll use `10.244.0.0/16`, which is a standard range used by a popular networking add-on called Flannel that we'll install later.

Here is the command we'll use:
```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

Go ahead and run that command. It will take a few minutes to complete. It will run a series of checks on your system and then start downloading the necessary container images for the control plane.

When it's finished, you should see a message that says `"Your Kubernetes control-plane has initialized successfully!"`.


## Case study
```bash
sajid@sajid:~$ sudo kubeadm init --pod-network-cidr=10.244.0.0/16 
[mark-control-plane] Marking the node sajid as control-plane by adding the labels: [node-role.kubernetes.io/control-plane node.kubernetes.io/exclude-from-external-load-balancers] 
Your Kubernetes control-plane has initialized successfully! 
To start using your cluster, you need to run the following as a regular user:   
mkdir -p $HOME/.kube   
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config   
sudo chown $(id -u):$(id -g) $HOME/.kube/config 
Alternatively, if you are the root user, you can run:   
export KUBECONFIG=/etc/kubernetes/admin.conf 
You should now deploy a pod network to the cluster. 
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:   https://kubernetes.io/docs/concepts/cluster-administration/addons/ 
Then you can join any number of worker nodes by running the following on each as root: kubeadm join 192.168.10.117:6443 
```

Now, looking at the successful output, kubeadm gives us three important commands as next steps.
* `mkdir -p $HOME/.kube` creates the `.kube` directory in your home folder.
* `sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config` copies the administrative configuration file into that new directory.
* `sudo chown $(id -u):$(id -g) $HOME/.kube/config` changes who owns the file. It's a key security step. Right now, the config file is owned by the `root` user because we used sudo to copy it.

> Any idea why we need to change the ownership from `root` to our own regular user?

It's definitely a permissions issue. If we didn't change the ownership, our regular user (`sajid`) wouldn't have the right to modify or even read that file easily.

Let's think one step further. When you run `kubectl`, it runs as you (the regular user, `sajid`) and looks for its configuration file in your home directory (`/home/sajid/.kube/config`).

If that file were still owned by `root`, your regular user wouldn't have permission to read it, and kubectl would fail. By changing the owner to your user, you're giving kubectl the key it needs to access the cluster.

You've got a great handle on this. Let's run these three commands you've just broken down to get kubectl working.

With those commands, you've essentially given your user account the "keys to the kingdom." Your kubectl command is now fully configured and ready to manage your new cluster. So, we've created the control plane and set up our command-line tool. 

>What's the one last thing kubeadm told us we need to do to make the cluster fully functional?

Even though the control plane is running, the nodes can't communicate with each other yet. To do that, we need to install a `Pod Network Add-on`.

`kubectl get nodes` gives us a status report on those servers/nodes. 

> Given that we haven't installed the pod network yet, do you think the node's status will be `"Ready"` or something else?

```bash
sajid@sajid:~$ kubectl get nodes 
NAME    STATUS     ROLES           AGE   VERSION 
sajid   NotReady   control-plane   18m   v1.30.14
```

Since the pod network isn't installed, the different Kubernetes components can't fully communicate, so the node can't pass its health checks. As a result, its status will be `NotReady`.

Your node is `NotReady` because it's missing the crucial pod network. Let's fix it in next step.
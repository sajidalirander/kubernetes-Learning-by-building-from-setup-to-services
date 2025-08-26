We're going to run the `kubeadm init` command. To do this correctly, we need to give it one important piece of information: an IP address range for the pods to use.

Kubernetes needs a dedicated network for its pods, and we have to tell it which block of IP addresses to reserve for them. We'll use `10.244.0.0/16`, which is a standard range used by a popular networking add-on called Flannel that we'll install later.

Here is the command we'll use:
```bash
sudo kubeadm init --pod-network-cidr=10.244.0.0/16
```

Go ahead and run that command. It will take a few minutes to complete. It will run a series of checks on your system and then start downloading the necessary container images for the control plane.

When it's finished, you should see a message that says `"Your Kubernetes control-plane has initialized successfully!"`.
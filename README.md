# Kubernetes learning by building from setup to services
Building a complete, stateful application stack from scratch.

## Step 0: Compatibility criteria
Before we install the main Kubernetes components, it's smart to confirm that your server meets the minimum requirements.

A Kubernetes cluster needs at least one control-plane node (the brains 🧠 of the operation) and usually one or more worker nodes (where your applications will run). The control-plane node has slightly higher requirements.

Follow the instructions at [STEP 0](./setup/step0.md).

## Step 1: Prepare Your Node and Install Containerd
The very first step is to prepare your server (which we'll call a "node") by installing a container runtime.

Kubernetes is a container orchestrator, which means it doesn't run containers itself. Instead, it tells a container runtime what to do. The most common runtime used with Kubernetes today is containerd.

This step ensures your system has the necessary software to run containers and is configured correctly for Kubernetes. We'll use a standard Ubuntu/Debian setup for this guide.

Follow the instructions at [STEP 1](./setup/step1.md).


## Step 2: Check for and Remove Old Installations
Ensuring a clean slate before a big installation like this can prevent a lot of headaches later. It's always best practice to check for and remove any old or incomplete installations.

Let's do this methodically. We'll first search for the main Kubernetes components and then, if we find any, we'll remove them.

Follow the instructions at [STEP 2](./setup/step2.md).


## Step 3: Install Kubernetes Tools
We're going to install the same three tools we removed in `step 2` (kubeadm, kubelet, and kubectl) by getting the latest stable versions.

Follow the instructions at [STEP 3](./setup/step3.md).

So far, we've installed the necessary Kubernetes tools (kubeadm, kubelet, and kubectl), and we've put a hold on them to prevent accidental upgrades.

Now, we're ready to initialize the cluster. 


## Step 4: Initialize the Kubernetes Control Plane
This is the big step where we actually create the cluster. We'll use the kubeadm tool to set up all the necessary components for the control plane—the brain of your cluster.

Follow the instructions at [STEP 4](./setup/step4.md).

## Step 5: Install a Pod Network Add-on
To get our node into a `Ready` state, we need to install a CNI (Container Network Interface) plugin. This plugin is responsible for creating a virtual network that allows pods to communicate with each other across the cluster.

Follow the instructions at [STEP 5](./setup/step5.md).

## Congratulations! You Have a Working Cluster!
You have successfully:
* Prepared a Linux server.
* Installed and configured a container runtime (containerd).
* Installed the Kubernetes command-line tools.
* Initialized a control plane with kubeadm.
* Deployed a pod network to make it all functional.

## What's Next?
Now that the infrastructure is built, you can start using it. 

Getting the terms cluster and node straight is key to understanding Kubernetes. Read [Chapter 0](./leason/ch0.md) to get an understanding. 

A great next step is to explore the cluster/node/server to see what's running under the hood.

When you run `kubectl get nodes`, we will get the running node. In my case, it is `sajid`. 

To explore the built node, follow the guide at [Chapter 1](./leason/ch1.md)


## Deploying Stateful Applications
Deploying applications like a database (PostgreSQL) and an object store (MinIO) is a fantastic next step because it introduces a new, important concept: `persistent data`.

Unlike a simple web server, these applications need to save data permanently. We'll need to tell Kubernetes how to do that.

Here's how we can tackle it:
* First, we'll quickly discuss Persistent Volumes—how Kubernetes saves data even if a pod restarts. Read the concept at [Chapter 2](./leason/ch2.md).
* Then, we'll deploy MinIO, the object storage server. Read the concept at [Chapter 3](./leason/ch3.md).
* Finally, we'll deploy PostgreSQL, the database. Read the concept at [Chapter 4](./leason/ch4.md).
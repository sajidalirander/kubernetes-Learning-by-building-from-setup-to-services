# Kubernetes learning by building from setup to services
Building a complete, stateful application stack from scratch.

### Step 0: Compatibility criteria
Before we install the main Kubernetes components, it's smart to confirm that your server meets the minimum requirements.

A Kubernetes cluster needs at least one control-plane node (the brains 🧠 of the operation) and usually one or more worker nodes (where your applications will run). The control-plane node has slightly higher requirements.

Follow the instructions at [STEP 0](./step0.md).

### Step 1: Prepare Your Node and Install Containerd
The very first step is to prepare your server (which we'll call a "node") by installing a container runtime.

Kubernetes is a container orchestrator, which means it doesn't run containers itself. Instead, it tells a container runtime what to do. The most common runtime used with Kubernetes today is containerd.

This step ensures your system has the necessary software to run containers and is configured correctly for Kubernetes. We'll use a standard Ubuntu/Debian setup for this guide.

Follow the instructions at [STEP 1](./step1.md).


### Step 2: Check for and Remove Old Installations
Ensuring a clean slate before a big installation like this can prevent a lot of headaches later. It's always best practice to check for and remove any old or incomplete installations.

Let's do this methodically. We'll first search for the main Kubernetes components and then, if we find any, we'll remove them.

Follow the instructions at [STEP 2](./step2.md).
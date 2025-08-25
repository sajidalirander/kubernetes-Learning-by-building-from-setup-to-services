# Kubernetes-Learning-by-building
Building a complete, stateful application stack from scratch.

### Step 1: Prepare Your Node and Install Containerd
The very first step is to prepare your server (which we'll call a "node") by installing a container runtime.

Kubernetes is a container orchestrator, which means it doesn't run containers itself. Instead, it tells a container runtime what to do. The most common runtime used with Kubernetes today is containerd.

This step ensures your system has the necessary software to run containers and is configured correctly for Kubernetes. We'll use a standard Ubuntu/Debian setup for this guide.

Follow the instructions at [STEP 1](./step1.md).


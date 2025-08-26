## 1. Prepare for the New Installation

First, let's add the official Google Cloud public signing key and the Kubernetes apt repository to your system. This ensures that the packages you download are authentic.

```bash
# Update apt and install dependencies
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# Add the Kubernetes package repository's public GPG key
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add the Kubernetes apt repository
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
## 2. Install kubelet, kubeadm, and kubectl

Now that your system trusts the new repository, you can install the tools. After we install them, we'll place an `apt-mark` hold on them.

The `apt-mark` hold command is like putting a `"Do Not Touch"` sign on a package. We do this to prevent the packages from being accidentally changed or updated during a routine system upgrade (like sudo apt-get upgrade).

In Kubernetes, this is critical because you need all the components in your cluster to be running the exact same version. An accidental upgrade on one node could cause it to stop communicating correctly with the others, leading to instability.

So, by putting a hold on them right after installation, we're locking in their version for stability.

let's run the final commands for this step.

```bash
# Update package list now that the new repository is added
sudo apt-get update

# Install the three tools
sudo apt-get install -y kubelet kubeadm kubectl

# Place the packages on hold
sudo apt-mark hold kubelet kubeadm kubectl
```
NOTE: We can remove the hold with `apt-mark unhold` or using a flag `--allow-change-held-packages` to remove them as we did in [step 2](./step2.md).

You noticed that the repository we added is for version 1.30, which is a recent stable release (until August 25, 2025). 

Choosing a Kubernetes version involves a bit of a trade-off:

* Latest Version (like `1.32`): You get the newest features, but it might have undiscovered bugs and fewer community resources available since it's brand new.
* Recent Stable Version (like `1.30`): This version is well-tested, widely used, and has a lot of community support and documentation. It's often the recommended choice for reliability.

For our learning purposes, sticking with the `stable v1.30` is a solid and reliable choice.

Once you've run these, we'll be ready to initialize your cluster. 
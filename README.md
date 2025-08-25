# Kubernetes-Learning-by-building
Building a complete, stateful application stack from scratch.

### Step 1: Prepare Your Node and Install Containerd
The very first step is to prepare your server (which we'll call a "node") by installing a container runtime.

Kubernetes is a container orchestrator, which means it doesn't run containers itself. Instead, it tells a container runtime what to do. The most common runtime used with Kubernetes today is containerd.

This step ensures your system has the necessary software to run containers and is configured correctly for Kubernetes. We'll use a standard Ubuntu/Debian setup for this guide.

1. Prepare the System

First, run these commands to prepare your system's networking and package manager. This enables required kernel modules and makes sure traffic is correctly routed for Kubernetes.

```bash
# Enable bridged traffic for Kubernetes networking
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Set system configurations for Kubernetes networking
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# Apply the new settings without a reboot
sudo sysctl --system
```

2. Install containerd

Next, we'll install the containerd software itself.

```bash
# Update your package list and install dependencies
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Add Docker's official GPG key and repository (it's a reliable source for containerd)
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list again and install containerd
sudo apt-get update
sudo apt-get install -y containerd.io
```

3. Configure containerd

Finally, we need to create a configuration file for containerd and make one important change. Kubernetes works best when its components and the container runtime use the same method for managing resources, called a "cgroup driver". We'll set containerd to use the systemd driver.

```bash
# Create the default configuration file
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

# Set the cgroup driver to systemd
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml

# Restart and enable the containerd service to apply the changes
sudo systemctl restart containerd
sudo systemctl enable containerd
```

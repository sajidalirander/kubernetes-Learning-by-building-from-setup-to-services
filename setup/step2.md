## 1. Check for Existing Components

The three main command-line tools for Kubernetes are kubeadm, kubelet, and kubectl. Let's see if your system knows where to find them. We'll also check for common configuration directories.

Please run this block of commands and share the output with me.

```bash
# Check for the main Kubernetes binaries
which kubeadm kubelet kubectl

# Check for the main Kubernetes configuration directory
ls /etc/kubernetes/

# Check for the user's kubeconfig directory
ls ~/.kube/
```

These commands will either show you the path to the file/directory or give you an error saying it can't be found, which is exactly what we want to see for a clean system.

## 2. Case study

### a. The main Kubernetes binaries
```bash
sajid@sajid:~$ which kubeadm kubelet kubectl 
/usr/bin/kubeadm /usr/bin/kubelet /usr/bin/kubectl 
```
The first command found kubeadm, kubelet, and kubectl in `/usr/bin/`. This means the software packages are installed on my system.

To avoid any conflicts with a new installation, our best move is to remove those old packages.

You can do this with a purge command, which is a bit stronger than a regular remove because it also deletes any system-wide configuration files associated with the packages.

> Could you run this command to clean everything up?
```bash
# This will completely remove the three main Kubernetes packages
sudo apt-get purge -y kubeadm kubelet kubectl
```

After you run it, let's double-check that they're gone by running the first check command one more time: `which kubeadm kubelet kubectl`. 

> What does it show now?

If the same case, you are unable to remove the packages due to an error, such as: 
```bash
E: Held packages were changed and -y was used without --allow-change-held-packages.
```
In Linux package management, a held package is one that's been marked to prevent it from being automatically updated, installed, or removed. This is often done to prevent accidental changes to critical software.

Adding `--allow-change-held-packages` to our command will tell the package manager that we intentionally want to remove these `"held"` packages.

Go ahead and give that a try. 

> What's the output when you run the modified command?
```bash
sudo apt-get purge -y kubeadm kubelet kubectl --allow-change-held-packages
```
Let's check that they're gone by running: `which kubeadm kubelet kubectl`.
This time, the `which` command returning nothing confirms that the old packages are gone and we have a perfectly clean slate. 

You have a helpful tip: Use `sudo apt autoremove`. This command will clean up a few leftover packages (conntrack, cri-tools, kubernetes-cni) that were installed as dependencies. It's a good housekeeping step.

### (b) The main Kubernetes configuration and the user's kubeconfig directory
The next two commands couldn't find the `/etc/kubernetes/` or `~/.kube/` directories. This means a Kubernetes cluster has likely never been configured or initialized.
```bash
sajid@sajid:~$ sudo ls /etc/kubernetes/ 
ls: cannot access '/etc/kubernetes/': No such file or directory 

sajid@sajid:~$ sudo ls ~/.kube/ 
ls: cannot access '/home/sajid/.kube/': No such file or directory
```

Your system is now completely clean of any old Kubernetes components. We have a fresh slate to work from.

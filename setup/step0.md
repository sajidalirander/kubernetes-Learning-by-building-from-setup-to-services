## System Requirements
We'll need to check three main things:

Operating System (OS)
CPU Cores
RAM (Memory)
Let's start by gathering that information from your server. 

> Could you run the commands below in your terminal and look at the output?

```bash
# To check your Linux distribution and version
cat /etc/os-release

# To check the number of CPU cores
nproc

# To check the amount of available RAM (in human-readable format)
free -h
```

The official Kubernetes documentation recommends the following minimum requirements for a single control-plane node:
* `OS`: A compatible Linux distribution (like Ubuntu 20.04+, Debian 11+, etc.)
* `CPU`: At least 2 cores
* `RAM`: At least 2 GiB

> Based on these requirements and the output you get, do you think your server is ready for Kubernetes?

> Now that if you confirmed your server is up to the task, are you ready for the next step?
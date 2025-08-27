# Create the MinIO Secret

We'll start by securely storing your ID and password. In Kubernetes, we never put sensitive information like passwords directly into our application's configuration. Instead, we use a special object called a `Secret`.

Think of a `Secret` as a small, secure vault within your cluster, designed specifically for holding sensitive data like passwords, API keys, or tokens.

We can create this secret with a single `kubectl` command. This command will create a new secret named `minio-secret` and store your ID and password inside it.

```bash
kubectl create secret generic minio-secret \
  --from-literal=MINIO_ROOT_USER='admin' \
  --from-literal=MINIO_ROOT_PASSWORD='admin123'
```

Wait!! Is it good idea to create everything using terminal command? Can we do it using a script so that any modification can be handle easily?

So here we are. A core concept in modern infrastructure called `"Declarative vs. Imperative"` management.

* `Imperative` (terminal command): Using commands like `kubectl create secret` is like giving direct, one-time orders. You tell Kubernetes how to do something. It's great for learning and quick tasks.
* `Declarative` (file script): Writing a script or a `YAML` file is like giving a blueprint or a final goal. You tell Kubernetes what you want the end result to look like, and Kubernetes figures out how to make it happen.

The declarative approach (using files) is more practical and professional for several reasons:
* `Version Control`: You can save your files in Git, track changes, and collaborate with a team.
* `Repeatability`: You can reliably create the same setup in different environments (development, staging, production).
* `Readability`: It's much easier to understand the state of your system by reading a file than by looking through command history.

So, how about we switch to that method? We can create our MinIO deployment using a YAML file. Would you like to start by creating the YAML for the Secret we just made?

## YAML: The Blueprint for Kubernetes
YAML (which stands for "YAML Ain't Markup Language") is a simple, human-readable data format. Kubernetes uses YAML files as blueprints to define the desired state of any object in the cluster, whether it's a Secret, a Deployment, or a Service.

Here's the YAML blueprint for the minio-secret we were about to create. Take a look and see if you can figure out what each part does:

File: [MinIO Secret](../config/minio-secret.yaml)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
type: Opaque
data:
  MINIO_ROOT_USER: YWRtaW4=
  MINIO_ROOT_PASSWORD: YWRtaW4xMjM=
```

There's one tricky part in there. The values for the user and password look like random characters. 

> Any idea why they aren't in plain text?

They're a type of encoding called Base64. Encoding is like translating a message into a different alphabet. It makes the data safe for transport over networks but can be easily translated back. Learn more about [encoding your own ID and password](../utils/base64_encoding.md).

> Why do you think Kubernetes requires the Secret's data to be encoded this way?

The main reason Kubernetes uses Base64 is to handle special characters. Passwords and keys can sometimes contain characters that aren't compatible with the YAML format or certain network protocols.

By encoding the data in Base64, we convert it into a simple, universally safe set of characters. This ensures the data is transmitted and stored without being corrupted.

### Step 1: Create the YAML File
You can create YAML files in any text editor, right in your current working directory on the server. We'll use a common command-line editor called `nano`. It's simple and straightforward.

First, we'll create the file and open it for editing. Learn more about [naming the file](../utils/naming_file.md).
```bash
nano minio-secret.yaml
```
This will open a new, blank file in the nano editor.

### Step 2: Add the Content
Now, copy the YAML content [MinIO Secret](../config/minio-secret.yaml) and paste it into the nano editor window.

### Step 3: Save and Exit
To save the file in nano:
* Press `Ctrl + X` to exit.
* It will ask you if you want to save. Press `Y` for Yes.
* It will confirm the file name. Just press `Enter`.

> Alternative, press `Ctrl + o`, confirm file name by pressing `Enter`, and 'Ctrl+x` to exit.

### Step 4: Create the Secret
Once that's done, you'll be back at your regular command prompt. 

> Now, how do you think we tell Kubernetes to read this file and create the secret object?

The command to create things in Kubernetes is indeed `kubectl create`, but we can also use a more versatile command called `kubectl apply`.

The `apply` command tells Kubernetes: "Look at this file and make sure the cluster matches it." If the object doesn't exist, it will be created. If it already exists and you've changed the file, it will be updated. It's a powerful and safe command to use. 

```bash
# make sure you have the correct file path
kubectl apply -f minio-secret.yaml
```
We use a special character, or "flag," to tell the command what kind of input we're providing. In this case, the flag to specify a filename is `-f`.

That command tells kubectl to apply the configuration found in `(-f)` the file `minio-secret.yaml`.

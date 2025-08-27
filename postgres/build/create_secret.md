## Creating PostgreSQL Secret
Just like with MinIO, we need to provide a username and password. The official `PostgreSQL` container image looks for these specific secret keys: `POSTGRES_USER` and `POSTGRES_PASSWORD`.

Here is the YAML. 

File: [PostgreSQL Secret](../config/sql-secret.yaml)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
type: Opaque
data:
  POSTGRES_USER: # Add Base64-encoded username here
  POSTGRES_PASSWORD: # Add Base64-encoded password here
```
## Case Study
> What are the two plain-text values we need to encode to complete this file?

```bash
sajid@sajid:~$ echo -n 'admin123' | base64 
YWRtaW4xMjM= 
sajid@sajid:~$ echo -n 'admin@admin.com' | base64 
YWRtaW5AYWRtaW4uY29t
```

Use your desire username and password to correctly encode. Now you're ready to create the `sql-secret.yaml` file.

> What are the three steps you'll follow to create, edit, and save the file using the `nano` editor? 

```bash
nano sql-secret.yaml
```
Copy and paste the content. After editing `ctrl+o`,`enter` and `ctrl+x`. You've got the `nano` workflow down.

> Now that the file is saved, what's the command to apply it to the cluster?

```bash
kubectl apply -f sql-secret.yaml
```
Go ahead and apply it. The secret is created and securely stored.
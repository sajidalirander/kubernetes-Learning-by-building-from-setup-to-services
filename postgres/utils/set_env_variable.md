## Configuring the environment variables
The official PostgreSQL container image is designed to be configured with environment variables, just like you did with the user and password.

The specific environment variable to set a default database name is `POSTGRES_DB`.

Knowing that, how would you modify the `env: section` in your [Postgres Deployment](../config/sql-dep.yaml) file to create the name of database (for example; `mock_data`) when the container starts?

We need to add a new item to the env list. Just like with the user and password, we need to put it inside a `- name: and value:` block as:
```yaml
- name: POSTGRES_DB
  value: mock_data
```

## Structure of ENV Section
The trick is that the `env: section` is a list of variables. Each item in the list starts with a hyphen `(-)` and has its own name and value (or valueFrom).

Here's how the complete `env: section` should look with all three variables:

File: [PostgreSQL Deployment](../config/sql-dep.yaml)
```yaml
env:
- name: POSTGRES_USER
  valueFrom:
    secretKeyRef:
      name: postgres-secret
      key: POSTGRES_USER
- name: POSTGRES_PASSWORD
  valueFrom:
    secretKeyRef:
      name: postgres-secret
      key: POSTGRES_PASSWORD
- name: POSTGRES_DB
  value: inspection_mock
```

Notice how each `-` introduces a new, self-contained block. Go ahead and open your [PostgreSQL Deployment File](../config/sql-dep.yaml) and add that third block for `POSTGRES_DB`. Once you've saved it, you'll need to apply the changes. 

> What command will you use to do that?

```bash
kubectl apply -f sql-dep.yaml
```

That's the command to apply the changes to your deployment. Go ahead and run it. Because the deployment already exists, `kubectl` will be smart enough to just update it with your changes instead of creating a new one.


## Case Study
```bash
sajid@sajid:~$ kubectl apply -f sql-dep.yaml  
deployment.apps/postgres-deployment configured 
```
The configured message shows that your change was applied successfully, and Kubernetes automatically created a new pod with the correct database name. You've now deployed a database with a custom name. Check the status again with the following command. Note that the pod name has changed for postgres-deployment. 

```bash
sajid@sajid:~$ kubectl get pods 
NAME                                   READY   STATUS    RESTARTS   AGE 
minio-deployment-69849b9879-42cg6      1/1     Running   0          115m 
postgres-deployment-5c564d6968-pntvd   1/1     Running   0          6s
```
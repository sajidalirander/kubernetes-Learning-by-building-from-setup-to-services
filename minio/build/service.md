## You've successfully:
* Created a `Secret` to hold the credentials.
* Set up `Persistent Storage` so the data won't be lost.
* Created a `Deployment` to run the application.

There's just one last step. Even though the pod is running, we can't access it from outside the cluster yet. We need to create a `Kubernetes Service` to expose it.

## Deployment v/s Service 
A Deployment's job is to run the pods inside the cluster. We need a different kind of object to expose them to the outside world.

Think in a way that you wanted to connect to an endpoint like `localhost:30627`. It can be use outside the kubernetes environment such as python integrity or web browser. 

Take a look at available options below:
* `NodePort`: Exposes the service on a static port on each node's IP.
* `ClusterIP`: Exposes the service on an internal IP, only reachable from within the cluster.

> Which of these two seems like the right fit for making our MinIO service accessible from a web browser?

A `NodePort` service is the perfect choice here. It will open up a specific high-numbered port on your server (the "node") and forward any traffic that arrives on that port to your MinIO pod.

This will give us a stable endpoint that we can access from our web browser, exactly like the `localhost:30627` for example.

## Creating YAML 
First, open a new file in your editor:
```bash
nano minio-service.yaml
```

Now, copy and paste this blueprint. It defines a `NodePort` service that listens on port `30627` on your server and forwards traffic to port `9090` on your MinIO pod, which is the port for the web console.

File: [MinIO Service](../config/minio-seervice.yaml)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: minio-service
spec:
  type: NodePort
  ports:
    - port: 9090
      targetPort: 9090
      nodePort: 30627
  selector:
    app: minio
```

There's a new and very important piece in this file: the `selector`.

> Based on how it's used here, what do you think its job is?

The selector is the mechanism that connects a `Service` to a `Deployment`.

Think of it like this:
* In our [MinIO Deployment](../config/minio-dep.yaml), we put a label on our pods that says `app: minio`.
* Now, in our [MinIO Service](../config/minio-seervice.yaml), the `selector` says, "I'm looking for any pod with the `app: minio` label."

This is how the `Service` knows which pods to send traffic to. It's a simple but powerful way to link different Kubernetes objects together.

You've got all the pieces. Go ahead and save the file and apply it.

```bash
kubectl apply -f minio-service.yaml 
```

You've now exposed your MinIO deployment to the outside world. Let's do a quick check to see our new service. 

> What `kubectl get` command would you use to see the details of your service?

Go ahead and run `kubectl get service`. The abbreviation `svc` is an even shorter can also be used. You'll see your minio-service and the port it's available on.

## Case Study
```bash
sajid@sajid:~$ kubectl get service 
NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE 
kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP          2d20h minio-service   NodePort    10.102.127.190   <none>        9090:30627/TCP   98s
```

That's a wrap. You've officially deployed and exposed your MinIO service. The output shows that your minio-service is up and running. Take a look at the PORT(S) column. Learn more about the [Ports and Network Flow](../utils/learn_ports.md). 

> Can you guess what address you'd put in your web browser to access the MinIO console?

```yaml
http://localhost:30627
```

Since your browser is running on the same machine as your Kubernetes node, `localhost` will work perfectly. If you were accessing it from another computer, you'd just replace `localhost` with your `server's IP address`.

Go ahead and open that address in your browser. You should see the MinIO login screen. Use the credentials you chose (admin / admin123 in this turorial) to log in.

You've successfully deployed and exposed MinIO. Now for the final test: go to your web browser and try to access the MinIO console.

> If you want to access using other machine what IP you should use. Should it be `10.102.127.190` as mentioned here? 
```bash
sajid@sajid:~$ kubectl get service 
NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE 
kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP          2d20h 
minio-service   NodePort    10.102.127.190   <none>        9090:30627/TCP   98s
```

The IP address `10.102.127.190` is the ClusterIP. Think of it as an internal office extension. It's a virtual IP address that only works inside the Kubernetes cluster. Pods within the cluster can use that IP to talk to the MinIO service, but you can't access it from the outside. So, if you want to connect from another machine, you'd need a different IP address.

To access your MinIO console from another machine on the same network, you'd use your server's actual IP address. Check your service IP address using the command below: 
```bash
ifconfig
```
Check `eth` for LAN or `wlo` for WIFI. Use that IP instead of `localhost`. 

You've successfully deployed a stateful application with persistent storage and exposed it to your network. This is a huge milestone.
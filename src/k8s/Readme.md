PS C:\tmp\fgtest\fgtestsvc\src> minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

PS C:\tmp\fgtest\fgtestsvc\src> ^C
PS C:\tmp\fgtest\fgtestsvc\src> minikube image load fgtest:latest
PS C:\tmp\fgtest\fgtestsvc\src> cd c:\tmp\fgtest\fgtestsvc\src && kubectl apply -f k8s/manifests.yaml
configmap/fgtest-config created
secret/fgtest-secrets created
deployment.apps/fgtest created
service/fgtest-service created
ingress.networking.k8s.io/fgtest-ingress created
PS C:\tmp\fgtest\fgtestsvc\src> kubectl get pods 
NAME                     READY   STATUS    RESTARTS   AGE
fgtest-58fbbb664-lkc8z   1/1     Running   0          38s     
PS C:\tmp\fgtest\fgtestsvc\src> minikube addons enable ingress

💡  ingress is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
💡  After the addon is enabled, please run "minikube tunnel" and your ingress resources would be available at "127.0.0.1"   
    ▪ Using image registry.k8s.io/ingress-nginx/controller:v1.11.3
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.4
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.4.4
🔎  Verifying ingress addon...
🌟  The 'ingress' addon is enabled
PS C:\tmp\fgtest\fgtestsvc\src> kubectl get all,ingress
NAME                         READY   STATUS    RESTARTS   AGE
pod/fgtest-58fbbb664-lkc8z   1/1     Running   0          2m56s

NAME                     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/fgtest-service   ClusterIP   10.104.217.210   <none>        80/TCP    2m56s
service/kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP   7h59m

NAME                     READY   UP-TO-DATE   AVAILABLE   AGE 
deployment.apps/fgtest   1/1     1            1           2m56s

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/fgtest-58fbbb664   1         1         1       2m56s

NAME                                       CLASS    HOSTS   ADDRESS        PORTS   AGE
ingress.networking.k8s.io/fgtest-ingress   <none>   *       192.168.49.2   80      2m56s
PS C:\tmp\fgtest\fgtestsvc\src> curl http://192.168.49.2/     
curl: (28) Failed to connect to 192.168.49.2 port 80 after 21046 ms: Could not connect to server
  RESTARTS   AGE
ingress-nginx-admission-create-92tr5        0/1     Completed   0          3m1s
  RESTARTS   AGE
ingress-nginx-admission-create-92tr5        0/1     Completed   0          3m1s
ingress-nginx-admission-patch-4bx2q         0/1     Completed   1        RESTARTS   AGE
ingress-nginx-admission-create-92tr5        0/1     Completed   0          3m1s       
ingress-nginx-admission-patch-4bx2q         0/1     Completed   1        RESTARTS   AGE
  RESTARTS   AGE
  RESTARTS   AGE
  RESTARTS   AGE
  RESTARTS   AGE
  RESTARTS   AGE
  RESTARTS   AGE
  RESTARTS   AGE
ingress-nginx-admission-create-92tr5        0/1     Completed   0          3m1s
ingress-nginx-admission-patch-4bx2q         0/1     Completed   1          3m1s
ingress-nginx-controller-56d7c84fd4-tf8kg   1/1     Running     0          3m1s
PS C:\tmp\fgtest\fgtestsvc\src> curl http://localhost:8080/     
{"detail":"Not Found"}
PS C:\tmp\fgtest\fgtestsvc\src> curl http://localhost:8080/stock-prices
{"symbol":"MSFT","ndays":7,"closing_prices":[{"date":"2025-04-16","closing_price":371.61},{"date":"2025-04-15","closing_price":385.73},{"date":"2025-04-14","closing_price":387.81},{"date":"2025-04-11","closing_price":388.45},{"date":"2025-04-10","closing_price":381.35},{"date":"2025-04-09","closing_price":390.49},{"date":"2025-04-08","closing_price":354.56}],"average_closing_price":380.00000000000006}
PS C:\tmp\fgtest\fgtestsvc\src> ^C
PS C:\tmp\fgtest\fgtestsvc\src> kubectl apply -f c:\tmp\fgtest\fgtestsvc\src\k8s\manifests.yaml
configmap/fgtest-config unchanged
secret/fgtest-secrets unchanged
deployment.apps/fgtest unchanged
service/fgtest-service unchanged
Warning: path /(.*) cannot be used with pathType Prefix
ingress.networking.k8s.io/fgtest-ingress configured
PS C:\tmp\fgtest\fgtestsvc\src> kubectl apply -f c:\tmp\fgtest\fgtestsvc\src\k8s\manifests.yaml
configmap/fgtest-config unchanged
secret/fgtest-secrets unchanged
deployment.apps/fgtest unchanged
service/fgtest-service unchanged
ingress.networking.k8s.io/fgtest-ingress configured
PS C:\tmp\fgtest\fgtestsvc\src> kubectl get ingress             
NAME             CLASS    HOSTS   ADDRESS        PORTS   AGE
fgtest-ingress   <none>   *       192.168.49.2   80      14m    
PS C:\tmp\fgtest\fgtestsvc\src> curl http://192.168.49.2/stock-prices
curl: (28) Failed to connect to 192.168.49.2 port 80 after 21013 ms: Could not connect to server
PS C:\tmp\fgtest\fgtestsvc\src> kubectl get all -n ingress-nginx

NAME                                            READY   STATUS      RESTARTS   AGE
pod/ingress-nginx-admission-create-92tr5        0/1     Completed   0          14m
pod/ingress-nginx-admission-patch-4bx2q         0/1     Completed   1          14m
pod/ingress-nginx-controller-56d7c84fd4-tf8kg   1/1     Running     0          14m

NAME                                         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
service/ingress-nginx-controller             NodePort    10.106.89.27   <none>        80:32620/TCP,443:30325/TCP   14m
service/ingress-nginx-controller-admission   ClusterIP   10.98.64.199   <none>        443/TCP                      14m

NAME                                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ingress-nginx-controller   1/1     1            
1           14m

NAME                                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/ingress-nginx-controller-56d7c84fd4   1         
1         1       14m

NAME                                       STATUS     COMPLETIONS   DURATION   AGE
job.batch/ingress-nginx-admission-create   Complete   1/1           13s        14m
job.batch/ingress-nginx-admission-patch    Complete   1/1           14s        14m
PS C:\tmp\fgtest\fgtestsvc\src> minikube ip                     
192.168.49.2
PS C:\tmp\fgtest\fgtestsvc\src> curl http://192.168.49.2:32620/stock-prices
curl: (28) Failed to connect to 192.168.49.2 port 32620 after 21040 ms: Could not connect to server
PS C:\tmp\fgtest\fgtestsvc\src> kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
PS C:\tmp\fgtest\fgtestsvc\src> kubectl apply -f c:\tmp\fgtest\fgtestsvc\src\k8s\manifests.yaml && kubectl get ingress
configmap/fgtest-config unchanged
secret/fgtest-secrets unchanged
deployment.apps/fgtest unchanged
service/fgtest-service unchanged
ingress.networking.k8s.io/fgtest-ingress configured
NAME             CLASS    HOSTS   ADDRESS        PORTS   AGE
fgtest-ingress   <none>   *       192.168.49.2   80      18m
PS C:\tmp\fgtest\fgtestsvc\src> curl http://localhost/stock-prices
{"symbol":"MSFT","ndays":7,"closing_prices":[{"date":"2025-04-16","closing_price":371.61},{"date":"2025-04-15","closing_price":385.73},{"date":"2025-04-14","closing_price":387.81},{"date":"2025-04-11","closing_price":388.45},{"date":"2025-04-10","closing_price":381.35},{"date":"2025-04-09","closing_price":390.49},{"date":"2025-04-08","closing_price":354.56}],"average_closing_price":380.00000000000006}

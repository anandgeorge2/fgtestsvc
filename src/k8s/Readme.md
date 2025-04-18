
# Build (All instructions are tested and working in Windows 11 home edition with docker desktop and minikube)

Location of the code is:
https://github.com/anandgeorge2/fgtestsvc.git

## To build 
```bash
git clone https://github.com/anandgeorge2/fgtestsvc.git
cd fgtestsvc\src
```

Install docker desktop and run the below command in the above directory:
```bash
docker build -t fgtest:latest .
```

## Optional: Tag with version if needed
```bash
docker build -t fgtest:v1.0.0-$(date +%Y%m%d) .
```

## Prebuilt docker image location
```bash
docker pull anandgeorge2/fgtest1:v1
```

# Deploy 

1. Install and start minikube 
2. Navigate to k8s directory:
```bash
cd fgtestsvc\src\k8s
```
3. Replace secret value to the correct base64 version of the API key. Check the email for the value.
4. Apply kubernetes manifests:
```bash
kubectl apply -f manifests.yaml
```
5. Test the service:
```bash
curl localhost/stock-prices
```

The output should look like below:

```bash
PS C:\Users\sourc> curl localhost/stock-prices


StatusCode        : 200
StatusDescription : OK
Content           : {"symbol":"MSFT","ndays":7,"closing_prices":[{"date":"2025-04-17","closing_price":367.78},{"date":"20
                    25-04-16","closing_price":371.61},{"date":"2025-04-15","closing_price":385.73},{"date":"2025-04-14"..
                    .
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Access-Control-Allow-Origin: *
                    Access-Control-Allow-Credentials: true
                    Access-Control-Allow-Methods: GET, PUT, POST, DELETE, PATCH, OPTIONS
                    Access-Control-Al...
Forms             : {}
Headers           : {[Connection, keep-alive], [Access-Control-Allow-Origin, *], [Access-Control-Allow-Credentials,
                    true], [Access-Control-Allow-Methods, GET, PUT, POST, DELETE, PATCH, OPTIONS]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 403
```
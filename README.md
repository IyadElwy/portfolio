# Interactive Portfolio Website with built-in Live Terminal
![portfolio](https://github.com/user-attachments/assets/8a41a2ae-5e8e-48b7-a7fb-47ae9e1a528b)


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-api
  labels:
    app: portfolio-api
spec:
  replicas: 1
  selector:
    matchLabels:
      app: portfolio-api
  template:
    metadata:
      labels:
        app: portfolio-api
    spec:
      containers:
        - name: portfolio-api
          image: iyadelwy/portfolio-api-image:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 5003
          resources:
            limits:
              memory: "100Mi"
              cpu: "0.50"
          readinessProbe:
            httpGet:
              path: /health
              port: 5003
              httpHeaders:
                - name: host
                  value: portfolio-vm
            initialDelaySeconds: 2
            periodSeconds: 5
            timeoutSeconds: 20
          livenessProbe:
            httpGet:
              path: "/health"
              port: 5003
            initialDelaySeconds: 5
            periodSeconds: 60
            timeoutSeconds: 20
            failureThreshold: 1
      restartPolicy: Always

---
apiVersion: v1
kind: Service
metadata:
  name: portfolio-api
  labels:
    app: portfolio-api
spec:
  type: ClusterIP
  ports:
    - port: 5003
      targetPort: 5003
      protocol: TCP
  selector:
    app: portfolio-api
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-vm
  labels:
    app: portfolio-vm
spec:
  replicas: 3
  selector:
    matchLabels:
      app: portfolio-vm
  template:
    metadata:
      labels:
        app: portfolio-vm
    spec:
      containers:
        - name: portfolio-vm
          image: iyadelwy/portfolio-vm-image:latest
          imagePullPolicy: Always
          resources:
            limits:
              memory: "100Mi"
              cpu: "0.50"
          readinessProbe:
            httpGet:
              path: /health
              port: 5003
            initialDelaySeconds: 2
            periodSeconds: 5
            timeoutSeconds: 20
            failureThreshold: 1
          livenessProbe:
            httpGet:
              path: "/health"
              port: 5003
            initialDelaySeconds: 5
            periodSeconds: 60
            timeoutSeconds: 20
            failureThreshold: 1
      restartPolicy: Always

---
apiVersion: v1
kind: Service
metadata:
  name: portfolio-vm
  labels:
    app: portfolio-vm
spec:
  type: ClusterIP
  ports:
    - port: 5003
      targetPort: 5003
      protocol: TCP
  selector:
    app: portfolio-vm
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: portfolio-api
spec:
  ingressClassName: nginx
  rules:
    - host: portfolio.iyadelwy.xyz
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: portfolio-api
                port:
                  number: 5003
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: airflow-worker-pod-access
rules:
  - apiGroups:
      - ""
    resources:
      - pods
    verbs:
      - create
      - list
      - get
      - patch
      - watch
      - delete
  - apiGroups:
      - ""
    resources:
      - pods/log
    verbs:
      - get
  - apiGroups:
      - ""
    resources:
      - pods/exec
    verbs:
      - create
      - get
  - apiGroups:
      - ""
    resources:
      - events
    verbs:
      - list
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: airflow-pod-launcher-rolebinding
subjects:
  - kind: ServiceAccount
    name: airflow-worker
    namespace: airflow
roleRef:
  kind: Role
  name: airflow-worker-pod-access
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: movie-processing-temp-pvc
spec:
  resources:
    requests:
      storage: 100Mi
  accessModes:
    - ReadWriteOnce
  storageClassName: "longhorn"

```
# Distributed Messaging System

## Overview
This project implements a distributed messaging system where messages are passed through a chain of servers running in Kubernetes pods. A message originating from a client is passed through server0 → server1 → server2 → server3, with each server forwarding the message to the next one in the chain.

## System Architecture
The system consists of:
- 1 Client application
- 4 Server applications (server0 through server3)
- Each component runs in its own Kubernetes pod
- Messages are passed using TCP sockets
- Each server forwards received messages to the next server in the chain

## Prerequisites
- Minikube installed and running
- kubectl configured to work with Minikube
- Python 3.x installed in the pods
- Docker installed

## Setup Instructions

1. Start Minikube:
```bash
minikube start
```

2. Build the Docker Image:
```bash
eval $(minikube docker-env)


docker build -t shan-3b -f container/Dockerfile .
```

3. Deploy the Kubernetes Resources:
```bash
# Create the service
kubectl apply -f container/shan-service.yaml

# Create the StatefulSet
kubectl apply -f container/shan-sset.yaml
```

4. Wait for all pods to be ready:
```bash
kubectl get pods -w
```

## Running the System

Start the servers in the following order:

1. On shan-sset-3 (last server):
```bash
kubectl exec -it shan-sset-3 -- /bin/bash
python3 /shan-dist-sys/dms/src/server3.py -l 3527
```

2. On shan-sset-2:
```bash
kubectl exec -it shan-sset-2 -- /bin/bash
python3 /shan-dist-sys/dms/src/server2.py -l 3526 -n shan-sset-3.shan-svc.default.svc.cluster.local:3527
```

3. On shan-sset-1:
```bash
kubectl exec -it shan-sset-1 -- /bin/bash
python3 /shan-dist-sys/dms/src/server1.py -l 3524 -n shan-sset-2.shan-svc.default.svc.cluster.local:3526
```

4. On shan-sset-0:
```bash
kubectl exec -it shan-sset-0 -- /bin/bash
python3 /shan-dist-sys/dms/src/server0.py -l 3525 -n shan-sset-1.shan-svc.default.svc.cluster.local:3524
```

5. Run the client (can be run from any pod):
```bash
python3 /shan-dist-sys/dms/src/client.py -c shan-sset-0.shan-svc.default.svc.cluster.local:3525
```

## Message Flow
1. Client sends a message to server0 (port 3525)
2. server0 forwards to server1 (port 3524)
3. server1 forwards to server2 (port 3526)
4. server2 forwards to server3 (port 3527)
5. server3 receives and displays the final message

## Implementation Details
- Each server uses TCP sockets for communication
- Messages are encoded in UTF-8 format
- Each server prints received messages and forwarding status
- The client can send multiple messages until interrupted






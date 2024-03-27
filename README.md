# ClusteApp
<p align="center">
  <img src="https://github.com/computational-chemical-biology/NAPviewer/blob/master/api/static/img/clusterapp-logo.png?raw=true" alt="AP logo"/>
</p>

ClusterApp: Just another clustering app. Cluster app is a popular dynamic clustering app, using QIIME2.

### Installation

```bash
git clone https://github.com/computational-chemical-biology/ClusterApp
```

### Build & Launch

```bash
make build
```
Launch
```bash
make server
```

### Use local install on jupyter

Access the docker container

```bash
docker run -it -p 8888:8888 -v "$PWD":/ClusterApp clusterapp
```

Inside the container, run jupyter

```bash
jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root
```


=======
# ClusteApp
<p align="center">
  <img src="https://github.com/HanselVinicius/ClusterApp/blob/master/api/static/img/clusterapp-logo.png" alt="AP logo"/>
</p>

ClusterApp: Just another clustering app. Cluster app is a popular dynamic clustering app, using QIIME2.

### Installation

```bash
git clone https://github.com/computational-chemical-biology/ClusterApp
```

### Build & Launch

```bash
make build
```
Launch
```bash
make server
```

### Use local install on jupyter

Access the docker container

```bash
docker run -it -p 8888:8888 -v "$PWD":/ClusterApp clusterapp
```

Inside the container, run jupyter

```bash
jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root
```


>>>>>>> 30f84fafe008e2ee1bb6b2a05b88cf11e0442a95

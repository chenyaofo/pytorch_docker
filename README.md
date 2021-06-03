# PyTorch Docker Images for Deep Learning Research

## Introduction

This [images](https://hub.docker.com/r/chenyaofo/pytorch) are built with PyTorch and some common used deep learning library.

We have installed the following packages via apt
```
git
wget
vim
htop
openssh-server
graphviz
```

and following packages via pypi
```
cython
ipdb
tb-nightly
graphviz
scipy
pycocotools
torch
torchvision
nvidia-dali
```

### Get Started

The available tags are
```
1.8.1-py38-cu102
1.8.1-py38-cu102-dali
1.8.1-py38-cu111
1.8.1-py38-cu111-dali
```

You can pull the image from DockerHub using

```
docker pull chenyaofo/pytorch:1.8.1-py38-cu102
```

If you are in China, you can using the baidubce to accelerate the pulling
```
mirror.baidubce.com/chenyaofo/pytorch:1.8.1-py38-cu102
```
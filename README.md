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
```

and following packages via pypi
```
tb-nightly
ipdb
scipy
scikit-learn
pandas
torch
torchvision
nvidia-dali
```

and following packages via conda:
```
pycocotools
graphviz
```

### Get Started

The available tags are
```
1.9.0-py38-cu102
1.9.0-py38-cu102-dali
1.9.0-py38-cu111
1.9.0-py38-cu111-dali
```

You can pull the image from DockerHub using

```
docker pull chenyaofo/pytorch:1.9.0-py38-cu111
```

If you are in China, you can using the baidubce to accelerate the pulling
```
mirror.baidubce.com/chenyaofo/pytorch:1.9.0-py38-cu111
```
or using aliyun
```
registry.cn-guangzhou.aliyuncs.com/chenyaofo/pytorch:1.9.0-py38-cu111
```
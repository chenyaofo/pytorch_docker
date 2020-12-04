FROM nvidia/cuda:11.1-base-ubuntu20.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH
RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    GIT_CLONE="git clone --depth 10" && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse' > /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse' >> /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse' >> /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse' >> /etc/apt/sources.list && \
    echo 'deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse' >> /etc/apt/sources.list && \
    cat /etc/apt/sources.list && \
    rm -rf /var/lib/apt/lists/* \
           /etc/apt/sources.list.d/cuda.list \
           /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL htop wget bzip2 graphviz git openssh-server vim && \
    apt-get clean

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

RUN PIP_INSTALL="/opt/conda/bin/pip --no-cache-dir install --upgrade" && \
    /opt/conda/bin/pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    $PIP_INSTALL ipdb tb-nightly ipython graphviz scipy numpy scikit-learn pandas matplotlib jupyter && \
    $PIP_INSTALL torch==1.7.0+cu110 torchvision==0.8.1+cu110 torchaudio==0.7.0 -f https://download.pytorch.org/whl/torch_stable.html && \
    $PIP_INSTALL --extra-index-url https://developer.download.nvidia.com/compute/redist nvidia-dali-cuda110

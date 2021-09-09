FROM nvidia/cuda:11.4.1-base-ubuntu20.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    PATH=/opt/conda/bin:$PATH \
    TZ=Asia/Shanghai

RUN APT_INSTALL="apt-get install -y --no-install-recommends" && \
    GIT_CLONE="git clone --depth 10" && \
    cat /etc/apt/sources.list && \
    rm -rf /var/lib/apt/lists/* \
           /etc/apt/sources.list.d/cuda.list \
           /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive $APT_INSTALL tzdata git wget vim htop openssh-server && \
    apt-get clean

RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo ${TZ} > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

RUN wget --quiet https://github.com/conda-forge/miniforge/releases/download/4.10.3-5/Mambaforge-4.10.3-5-Linux-x86_64.sh -O ~/installer.sh && \
    /bin/bash ~/installer.sh -b -p /opt/conda && \
    rm ~/installer.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    CONDA_INSTALL="/opt/conda/bin/mamba install --freeze-installed -y" && \
    $CONDA_INSTALL python=3.8 && \
    /opt/conda/bin/conda clean -afy

RUN CONDA_INSTALL="/opt/conda/bin/mamba install --freeze-installed -y" && \
    $CONDA_INSTALL -c pytorch pytorch==1.9.0 torchvision==0.10.0 torchaudio==0.9.0 cudatoolkit=11.1

RUN CONDA_INSTALL="/opt/conda/bin/mamba install --freeze-installed -y" && \
    $CONDA_INSTALL -c conda-forge pycocotools graphviz ipdb scipy scikit-learn pandas  && \
    echo 'Conda Install Done!'

RUN PIP_INSTALL="/opt/conda/bin/pip --no-cache-dir install --upgrade" && \
    $PIP_INSTALL tb-nightly  && \
    $PIP_INSTALL --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-cuda110 && \
    echo 'PIP Install Done!'

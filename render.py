import os
import copy
from posixpath import join
from jinja2 import Template
import yaml

CUDA_VERSION_MAPPING = {
    "10.2": "10.2",
    "11.0": "11.0.3",
    "11.1": "11.1.1",
    "11.2": "11.2.2",
    "11.3": "11.3.1",
    "11.4": "11.4.1"
}

PYTORCH_VERSION_2_VISION_VERSION = {
    "1.10.0": "0.11.1",
    "1.9.0": "0.10.0",
    "1.8.0": "0.9.0",
    "1.7.1": "0.8.2",
    "1.7.0": "0.8.0",
    "1.6.0": "0.7.0",
    "1.5.1": "0.6.1",
    "1.5.0": "0.6.0",
}

PYTORCH_VERSION_2_AUDIO_VERSION = {
    "1.10.0": "0.10.0",
    "1.9.0": "0.9.0",
    "1.8.0": "0.8.0",
    "1.7.1": "0.7.2",
    "1.7.0": "0.7.0",
}

PYTORCH_VERSION_2_CUDA_VERSION = {
    "1.10.0": ["10.2", "11.3"],
    "1.9.0": ["10.2", "11.1"],
    "1.8.0": ["10.2", "11.1"],
    "1.7.1": ["10.2", "11.0"],
    "1.7.0": ["10.2", "11.0"],
    "1.6.0": ["10.2", ],
    "1.5.1": ["10.2", ],
    "1.5.0": ["10.2", ],
}


def config2dockerfile(config, tag=None):
    assert config["CUDA_VERSION"] in CUDA_VERSION_MAPPING.keys()
    assert config["PYTORCH_VERSION"] in PYTORCH_VERSION_2_VISION_VERSION.keys()
    assert config["PYTHON_VERSION"] in ["3.6", "3.7", "3.8", "3.9"]

    if config["PYTORCH_VERSION"] not in PYTORCH_VERSION_2_AUDIO_VERSION.keys():
        config["IS_INSTALL_TORCHAUDIO"] = False

    config['UBUNTU_VERSION'] = "18.04" if "10." in config["CUDA_VERSION"] else "20.04"
    config["CUDA_VERSION"] = CUDA_VERSION_MAPPING[config["CUDA_VERSION"]]
    config["TORCHVISION_VERSION"] = PYTORCH_VERSION_2_VISION_VERSION[config["PYTORCH_VERSION"]]
    if config["IS_INSTALL_TORCHAUDIO"]:
        config["TORCHAUDIO_VERSION"] = PYTORCH_VERSION_2_AUDIO_VERSION[config["PYTORCH_VERSION"]]

    pytorch_cuda_versions = PYTORCH_VERSION_2_CUDA_VERSION[config["PYTORCH_VERSION"]]
    config["PYTORCH_CUDA_VERSION"] = ""
    for v in pytorch_cuda_versions:
        if "10." in config["CUDA_VERSION"]:
            if "10." in v:
                config["PYTORCH_CUDA_VERSION"] = v
        elif "10." not in v:
            config["PYTORCH_CUDA_VERSION"] = v
    if not config["PYTORCH_CUDA_VERSION"]:
        raise ValueError(f'''Can not find cuda version {config["CUDA_VERSION"]} for pytorch {config["PYTORCH_VERSION"]}''')

    if tag is None:
        tag = f'''{config["PYTORCH_VERSION"]}-py{config["PYTHON_VERSION"].replace(".","")}-cu{config["PYTORCH_CUDA_VERSION"].replace(".","")}{'-dali' if config["IS_INSTALL_DALI"] else ''}'''

    extra_pytorch_find_url = "-f https://download.pytorch.org/whl/torch_stable.html"

    config["EXTRA_PYTORCH_FIND_URL"] = extra_pytorch_find_url
    if config["CUDA_VERSION"] != "10.2":
        config["PYTORCH_VERSION"] += "+cu"+config["PYTORCH_CUDA_VERSION"].replace(".", "")
        config["TORCHVISION_VERSION"] += "+cu"+config["PYTORCH_CUDA_VERSION"].replace(".", "")

    config["DALI"] = "nvidia-dali-cuda102" if "10." in config["CUDA_VERSION"] else "nvidia-dali-cuda110"

    rendered_content = Template(open('Dockerfile.template').read(), trim_blocks=True).render(**config)
    # print(rendered_content)

    path = os.path.join(os.path.join("dockerfile", f"Dockerfile-{tag}"))
    with open(path, "w") as f:
        f.write(rendered_content)
    return tag


prefix = '''name: PyTorch Docker Image CI
on:
  push:
    tags:
    - v*
jobs:'''

if __name__ == "__main__":
    with open("config.yaml", "r") as f:
        config = yaml.load(f.read())
    os.system("rm -rf dockerfile")
    os.makedirs("dockerfile", exist_ok=True)
    jobs = []
    for pytorch_version in ["1.7.0", "1.8.0", "1.9.0", "1.10.0"]:
        for cuda_version in ["10.2", "11.4"]:
            for is_install_dali in [True]:
                c = copy.deepcopy(config)
                c["PYTORCH_VERSION"] = pytorch_version
                c["CUDA_VERSION"] = cuda_version
                c["IS_INSTALL_DALI"] = is_install_dali
                jobs.append(config2dockerfile(c))

    with open(".github/workflows/dockerimage.yaml", "w") as workflows:
        workflows.write(prefix)
        for job in jobs:
            build_vars = dict(
                JOB_NAME="Dockerfile-"+job.replace(".", "_"),
                IMAGE_NAME="pytorch",
                IMAGE_TAG=job,
                dockerfile=os.path.join(os.path.join("dockerfile", f"Dockerfile-{job}")),
                workspace='workspace',
            )
            rendered_content = Template(open('github-action.template').read(), trim_blocks=True).render(**build_vars)

            workflows.write(f"\n{rendered_content}\n")

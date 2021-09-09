import os
from jinja2 import Template
import yaml


with open("config.yaml", "r") as f:
    config = yaml.load(f.read())
print(config)

CUDA_VERSION_MAPPING = {
    "10.2": "10.2",
    "11.0": "11.0.3",
    "11.1": "11.1.1",
    "11.2": "11.2.2",
    "11.3": "11.3.1",
    "11.4": "11.4.1"
}

PYTORCH_VERSION_2_VISION_VERSION = {
    "1.9.0": "0.10.0",
    "1.8.0": "0.9.0",
    "1.7.1": "0.8.2",
    "1.7.0": "0.8.0",
    "1.6.0": "0.7.0",
    "1.5.1": "0.6.1",
    "1.5.0": "0.6.0",
}

PYTORCH_VERSION_2_AUDIO_VERSION = {
    "1.9.0": "0.9.0",
    "1.8.0": "0.8.0",
    "1.7.1": "0.7.2",
    "1.7.0": "0.7.0",
}

PYTORCH_VERSION_2_CUDA_VERSION = {
    "1.9.0": ["10.2", "11.1"],
    "1.8.0": ["10.2", "11.1"],
    "1.7.1": ["10.2", "11.0"],
    "1.7.0": ["10.2", "11.0"],
    "1.6.0": ["10.2", ],
    "1.5.1": ["10.2", ],
    "1.5.0": ["10.2", ],
}

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

config["DALI"] = "nvidia-dali-cuda102" if "10." in config["CUDA_VERSION"] else "nvidia-dali-cuda110"

rendered_content = Template(open('Dockerfile.template').read(), trim_blocks=True).render(**config)
print(rendered_content)

with open(os.path.join("Dockerfile"), "w") as f:
    f.write(rendered_content)


print(f'''git tag docker-build-{config["PYTORCH_VERSION"]}-cu{config["PYTORCH_CUDA_VERSION"].replace(".","")}\
{'-dali' if config["IS_INSTALL_DALI"] else ''} && git push --tags''')

# cuda_versions = ['10.2', '11.4.1']
# miniconda_version = 'py38_4.9.2'
# py_version, *_ = miniconda_version.split("_")

# torch_base_version = "1.9.0"

# prefix = '''
# name: PyTorch Docker Image CI
# on:
#   push:
#     tags:
#     - v*

# jobs:
# '''
# with open(".github/workflows/dockerimage.yaml", "w") as workflows:
#     workflows.write(prefix+"\n")
#     for cuda_version in cuda_versions:
#         for use_dali in [False, True]:
#             build_vars = dict(
#                 cuda_version=cuda_version,
#                 ubuntu_version='18.04' if cuda_version == "10.2" else '20.04',
#                 apt_packages=' '.join([
#                     'git',
#                     'wget',
#                     'vim',
#                     'htop',
#                     'openssh-server',
#                     'graphviz',
#                 ]),
#                 miniconda_version=miniconda_version,
#                 pip_package=' '.join([
#                     'cython',
#                     'ipdb',
#                     'tb-nightly',
#                     'graphviz',
#                     'scipy',
#                 ]),
#                 conda_packages=[
#                     ('pycocotools', 'conda-forge'),
#                 ],
#                 torch_version=torch_base_version + '+' + ('cu102' if cuda_version == "10.2" else 'cu111'),
#                 torchvision_version='0.10.0' + '+' + ('cu102' if cuda_version == "10.2" else 'cu111'),
#                 dali_package=None if not use_dali else 'nvidia-dali-cuda102' if cuda_version == "10.2" else 'nvidia-dali-cuda110'
#             )
#             rendered_content = Template(open('Dockerfile.template').read(), trim_blocks=True).render(**build_vars)

#             cuda_abbr = 'cu102' if cuda_version == "10.2" else 'cu111'
#             has_dali_name = '-dali' if use_dali else ''

#             Dockerfile = f'Dockerfile.pytorch-{py_version}-{cuda_abbr}{has_dali_name}'
#             with open(os.path.join("docker", Dockerfile), "w") as f:
#                 f.write(rendered_content)

#             build_vars = dict(
#                 job_name=Dockerfile.replace(".", "-"),
#                 image_name="pytorch",
#                 image_tag=f"{torch_base_version}-{py_version}-{cuda_abbr}{has_dali_name}",
#                 dockerfile=os.path.join("docker", Dockerfile),
#                 workspace='workspace',
#             )
#             rendered_content = Template(open('github_action.template').read(), trim_blocks=True).render(**build_vars)

#             workflows.write(f"\n{rendered_content}\n")

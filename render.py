import os
from jinja2 import Template

cuda_versions = ['10.2', '11.3.0']
miniconda_version = 'py38_4.9.2'
py_version, *_ = miniconda_version.split("_")

torch_base_version = "1.8.1"

prefix = '''
name: PyTorch Docker Image CI
on:
  push:
    tags:
    - v*

jobs:
'''
with open(".github/workflows/dockerimage.yaml", "w") as workflows:
    workflows.write(prefix+"\n")
    for cuda_version in cuda_versions:
        for use_dali in [False, True]:
            build_vars = dict(
                cuda_version=cuda_version,
                ubuntu_version='18.04' if cuda_version == "10.2" else '20.04',
                apt_packages=' '.join([
                    'git',
                    'wget',
                    'vim',
                    'htop',
                    'openssh-server',
                ]),
                miniconda_version='py38_4.9.2',
                pip_package=' '.join([
                    'tb-nightly',
                ]),
                conda_packages=[
                    ('pycocotools', 'conda-forge'),
                    ('ipdb', 'conda-forge'),
                    ('graphviz', 'anaconda'),
                    ('scipy', 'anaconda'),
                ],
                torch_version=torch_base_version + '+' + ('cu102' if cuda_version == "10.2" else 'cu111'),
                torchvision_version='0.9.1' + '+' + ('cu102' if cuda_version == "10.2" else 'cu111'),
                dali_package=None if not use_dali else 'nvidia-dali-cuda100' if cuda_version == "10.2" else 'nvidia-dali-cuda110'
            )
            rendered_content = Template(open('Dockerfile.template').read(), trim_blocks=True).render(**build_vars)

            cuda_abbr = 'cu102' if cuda_version == "10.2" else 'cu111'
            has_dali_name = '-dali' if use_dali else ''

            Dockerfile = f'Dockerfile.pytorch-{py_version}-{cuda_abbr}{has_dali_name}'
            with open(os.path.join("docker", Dockerfile), "w") as f:
                f.write(rendered_content)

            build_vars = dict(
                job_name=Dockerfile.replace(".", "-"),
                image_name="pytorch",
                image_tag=f"{torch_base_version}-{py_version}-{cuda_abbr}{has_dali_name}",
                dockerfile=os.path.join("docker", Dockerfile),
                workspace='workspace',
            )
            rendered_content = Template(open('github_action.template').read(), trim_blocks=True).render(**build_vars)

            workflows.write(f"\n{rendered_content}\n")

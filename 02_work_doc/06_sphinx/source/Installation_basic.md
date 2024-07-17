
(InstalltionBasic)=
## How to install?

### Step by step
We will first guide you through the process how to install `Wissenplattform` Django app.

1. creating an virtual python environment
2. clone `wissenplattform` GitHub repository
3. install wissenplattform and its dependencies

We will guide you through the process now.
```shell
# create fresh python environment with conda
python -m venv ~/pyVenvs/wissensplattform
# activate your environment
source ~/pyVenvs/webCDocuTest/bin/activate
# clone wissenplattform repository (you can also use SSH if you prefer)
# the option "--recurse-submodules" is needed to load submodules
git clone --recurse-submodules https://gitXXXX TODO
# change into wissenplattform folder
cd webcentral   XXX adapt after restructure

# install pip requirements
pip install -e '.'
```

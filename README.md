# cepack

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/empm?logo=python)
![PyPI - Version](https://img.shields.io/pypi/v/empm?logo=pypi)
![Codecov](https://img.shields.io/codecov/c/github/paopaozhi/empm?logo=codecov)
![PyPI - License](https://img.shields.io/pypi/l/empm?logo=apache)

嵌入式包管理器

## 支持命令

|命令|描述|
|---|---|
|install|读取toml文件，安装库|
|add|添加库|
|remove|删除库|

## 开发指南

### 安装依赖

```shell
pip install -r requirements.txt
pip install pipreqs
```

> 使用pipreqs生成依赖列表
> 使用到了新的包需要使用`pipreqs . --force`重新生成依赖列表

### 本地安装

```shell
pip install --editable .
```

---
sidebar_position: 1
title: 概述
---

# empm

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/empm?logo=python)
![PyPI - Version](https://img.shields.io/pypi/v/empm?logo=pypi)
![Codecov](https://img.shields.io/codecov/c/github/paopaozhi/empm?logo=codecov)
![PyPI - License](https://img.shields.io/pypi/l/empm?logo=apache)

灵感来源于，pip和cargo这两个包管理工具，在嵌入式开发中，总是需要自己处理各种包，并且需要将其嵌入到自己的工程中，这就会可能会导致一个简单的demo工程变得非常庞大，在python和rust开发中，我们总是可以使用优秀的包管理器管理包，但是，在嵌入式中并没有一个让我中意的包管理器，所以，该项目应于而生。

empm，帮助嵌入式软件工程师完成关于包的管理，让其专注在逻辑代码的实现。

## 支持命令

目前支持的功能还很少，但是，新功能正在紧张的开发中。

|命令|描述|
|---|---|
|add|添加库|
|home|GUI管理界面|
|install|读取toml文件，安装库|
|remove|删除库|

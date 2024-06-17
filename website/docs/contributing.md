---
sidebar_position: 3
title: 贡献指南
---

# 贡献指南

## 获取代码

```shell
git clone https://github.com/paopaozhi/empm.git
cd empm
```

## 搭建开发环境

> 不论使用哪种虚拟环境，都非常建议建立虚拟开发环境以隔离其他开发环境，避免依赖冲突

### 使用conda（强烈推荐）

```shell
conda create -n empm python=3.9
conda activate empm
pip install -r requirements.txt
```

### 使用venv

> 注意：该开发环境搭建，未进行测试，使用时请检查

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 依赖管理

```shell
pip install pipreqs
```

使用pipreqs生成依赖列表

使用到了新的包需要使用`pipreqs . --force`重新生成依赖列表

## 本地开发安装

```shell
pip install --editable .
```

## 运行测试

```shell
pytest test --cov . --cov-report=html
```
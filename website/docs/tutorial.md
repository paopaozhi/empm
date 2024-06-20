---
sidebar_position: 2
title: 使用教程
---

# 使用教程

本教程通过一个例程引导你，使用 **empm** 管理你开发中的包。

## 开始

首先，需要通过PYPI安装empm：

```shell
pip install empm
```

然后，假设我们的项目结构如下：

<!-- TODO:需要补充一个示例项目的目录结构 -->
```shell
```

需要在项目的根目录创建一个`empm.toml`文件，通过这个文件管理项目中使用的包，现在的项目结构如下：

<!-- TODO:需要补充一个创建好管理文件的示例项目的目录结构 -->
```shell
```

接下来，在这个示例中添加一个`lvgl`的软件包：

1. 在`empm.toml`文件中添加如下代码：

    ```toml
    [dependencies]
    lvgl = {url = "https://github.com/lvgl/lvgl", version = "v9.1.0"}
    ```

2. 运行安装依赖命令`empm install`

这样子，lvgl的包就会自动下载并且安装在你项目的`lib/`目录下，现在的项目目录结构应该为：

```shell
```

接下来，我们讲解一个配置的`empm.toml`文件：

看到第一个节点是`dependencies`，这是个必须的，

接下来是表示每一个依赖包的信息：

```toml
<依赖包名> = {url = <仓库的链接>, version = <对应的release包版本>}
```

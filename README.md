Copyright (c) 2025 nameisname
This software is licensed under the GNU General Public License v3.0.

# 进程管理任务系统

## 项目目标
设计一个以进程为中心的任务管理系统，解决任务管理中截止期限不合理、工作记忆上限等问题。通过对进程的CRUD操作，帮助用户更有效地管理任务。

## 主要功能
- **进程管理**: 
  - 创建、更新、删除和查询进程。
  - 进程属性包括：名字、状态（运行中、搁置中、阻塞中）、优先级（高中低）、详细信息和日志。
- **属性管理**:
  - 修改进程的名字、状态、优先级、详细信息和日志。
  - 查询进程的历史日志。
- **查询功能**:
  - 根据优先级和运行状态查询进程。

## 预期技术栈
- **后端**: 使用Python和FastAPI框架。
- **数据库**: 使用SQLAlchemy链接SQLite。
- **前端**: 使用HTML、CSS和JavaScript。

## 参考的开源项目
目前没有指定参考的开源项目，但可以根据需求选择合适的项目进行参考。

# 如何快速部署本项目

首先将本项目的文件都解压，记录下解压后的文件夹路径

打开cmd，输入以下命令，检查是否有python
```cmd
python --version
```
如果没有python环境，可以参照下面的教程搭建python环境
参见 https://www.runoob.com/python3/python3-install.html

以我为例，我的路径是F:\ProcessManagement，后面所有的文件都是在这个文件夹下
所以后面所有的“文件夹路径”都替换成 F:\ProcessManagement

在cmd里面，输入
```cmd
pip install -r 文件夹路径\requirements.txt
```
非魔法可以使用
```cmd
pip install -r 文件夹路径\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
所以我的输入是
```
pip install -r F:\ProcessManagement\requirements.txt
```
等待完成


然后编写一个ps1脚本
先新建一个txt文件，复制下面的内容，更换里面的文件夹路径
写好了把后缀改成.ps1
```
$url = "http://localhost:8000/"
Start-Process $url
cd 文件夹路径
python main.py
```
完成后鼠标右键ps1文件
点击菜单中的“使用Powershell运行”
等一会就加载出来了

## 注意事项
如果打开之后等了一会还是显示无法加载
可以将ps1脚本拖入Powershell中运行

如果显示不允许运行
用管理员身份打开powershell，运行这句话
```
Set-ExecutionPolicy RemoteSigned
```
然后输入Y
再重新打开

## 为ps1建立快捷方式
在快捷方式中填写
```
powershell.exe -ExecutionPolicy Bypass -File "完整路径\脚本名.ps1"
```
可以使用build\icons\icon.ico作为快捷方式的图标
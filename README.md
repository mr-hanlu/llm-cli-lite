# llm-cli-lite

一个轻量的命令行工具，通过自然语言生成终端命令，允许用户查看和修改 JSON 配置文件（如 API 密钥、模型名称等），并通过自然语言查询调用 LLM（如 ollama 或 openai_api）生成命令。

## 安装

方法一：
``` bash
pip install llm-cli-lite
```
方法二：
``` bash
# 克隆或下载项目仓库：
git clone https://github.com/mr-hanlu/llm-cli-lite.git
cd llm-cli-lite

# （可选）创建并激活虚拟环境：
conda create -n llm-cli-lite python=3.12
conda activate llm-cli-lite

# 安装工具及其依赖：
pip install .

# 这会将 llm-cli 安装为可编辑模式。如果需要开发模式（修改代码无需重新安装）可用：
pip install -e .
```

**将安装的环境添加到系统环境变量，这样可以全局使用**：`YOU_PATH\llm-cli-lite\Scripts`

**验证安装：**
``` bash
llm-cli --help
```

**config.json 配置文件保存在路径 `~/.llm-cli-lite/config.json` 中**

## 功能特性

显示帮助消息：llm-cli --help

查看配置：使用 llm-cli -l 列出所有配置项。

修改配置：支持设置 API 密钥、模型名称、基础 URL 等，例如 llm-cli --api_key "your-key"。

模型选择：支持 ollama 和 openai_api 模型，通过 -m 参数切换。

自然语言查询：输入自然语言描述（如 llm-cli "列出当前目录文件"），生成相应终端命令。

## 添加新功能

新命令：在 llm_cli_lite/\_\_main__.py 中添加新的 argparse 命令。

新模型支持：扩展 openai_api_fun.py 或添加新模型接口。

配置字段：在 config.json 中添加新字段并更新命令行参数。


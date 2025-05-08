from openai import OpenAI
from typing import Generator
import os
import json
import time


def create_chat_completion(base_url: str, api_key: str, model_name: str, prompt: str,
                           stream: bool = False, temperature: float = 0.5, top_p: float = 0.9) -> Generator[
    str, None, None]:
    """
    创建聊天完成的函数封装

    参数:
        base_url: API基础URL
        api_key: API密钥
        model_name: 模型名称
        prompt: 用户提示
        stream: 是否流式输出
        temperature: 温度参数
        top_p: top_p参数

    返回:
        生成器，逐个返回token
    """

    client = OpenAI(base_url=base_url, api_key=api_key)

    # 判断终端系统
    if os.name == "nt":  # Windows
        terminal = "CMD"
    elif os.name == "posix":  # Linux, macOS, etc.
        terminal = "Linux"
    else:
        terminal = "Unknown OS"

    system_prompt = f"""
    你是一个命令行ai助手，请提供最相关的{terminal}终端命令
    输出格式为：

    命令: <command>
    解释: <explanation>

    命令一定要准确，<command>的输出一定要能直接运行，不要有额外的符号。
    不要有编造，如果提问不相关，直接回答"无法根据您的请求提供命令。"
    解释要尽量简短，不要有额外的输出。
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        stream=stream
    )

    for chunk in response:
        yield chunk.choices[0].delta.content or ""


def llm_client(config_path: str, query: str):
    """LLM客户端函数

    参数:
        config_path: 配置文件路径
        query: 用户查询
    """
    # 读取配置文件
    with open(config_path, "r") as f:
        config = json.load(f)

    # 使用openai_api
    if config["is_openai_api"]:
        models = "openai_api"
    else:
        models = "ollama"

    base_url = config["models"][models]["base_url"]
    name = config["models"][models]["model_name"]
    api_key = config["models"][models]["api_key"]

    # 开始循环聊天
    for token in create_chat_completion(
            base_url=base_url,
            api_key=api_key,
            model_name=name,
            prompt=query,
            stream=True
    ):
        print(token, end="", flush=True)


# 示例用法
if __name__ == "__main__":
    # 直接调用函数示例
    base_url = "https://api-inference.modelscope.cn/v1"
    api_key = "3ce9e4e5-f3c6-4fee-aa2a-6e2342c70505"
    model_name = "Qwen/Qwen2.5-7B-Instruct"

    while True:
        prompt = input("> ")

        for token in create_chat_completion(
                base_url=base_url,
                api_key=api_key,
                model_name=model_name,
                prompt=prompt,
                stream=True
        ):
            print(token, end="", flush=True)

        print()
        print()
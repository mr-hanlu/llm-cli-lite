from openai import OpenAI
from typing import Generator
import os
import json


class ChatCompletionClient:
    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name
        self.max_tokens = 2048
        self.temperature = 0.5
        self.top_k = 20
        self.top_p = 0.9

        # 判断终端系统
        if os.name == "nt":  # Windows
            terminal = "CMD"
        elif os.name == "posix":  # Linux, macOS, etc.
            terminal = "Linux"
        else:
            terminal = "Unknown OS"

        system = f"""
        你是一个命令行ai助手，请提供最相关的{terminal}终端命令
        输出格式为：
        
        命令: <command>
        解释: <explanation>
        
        命令一定要准确，<command>的输出一定要能直接运行，不要有额外的符号。
        不要有编造，如果提问不相关，直接回答“无法根据您的请求提供命令。”
        解释要尽量简短，不要有额外的输出。
        """

        self.system = [{
            "role": "system",
            # "content": "你是小天，由hanlu开发，是一个ai助手。"
            "content": system,
        }]

    def get_models(self) -> list:
        """获取可用的模型列表"""
        models = self.client.models.list()
        return [model.id for model in models.data]

    def create_chat_completion(self, prompt: str, stream: bool = False) -> Generator[str, None, None]:
        # 纯文本问答
        message = self.system + [{"role": "user", "content": prompt}]

        """创建聊天完成"""
        out = self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            # max_tokens=self.max_tokens,
            temperature=self.temperature,
            # top_k=self.top_k,
            top_p=self.top_p,
            stream=stream
        )
        answer = ""
        for chunk in out:
            answer_chunk = (chunk.choices[0].delta.content or "")
            answer += answer_chunk
            # print(answer_chunk, end="")
            yield answer_chunk

    def set_model(self, model_name: str):
        """设置模型名称"""
        self.model_name = model_name

    def set_params(self, max_tokens: int = 200, temperature: float = 0.5, top_p: float = 0.7):
        """设置请求参数"""
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p


from functools import lru_cache


@lru_cache(maxsize=1)
def get_client(base_url, api_key, model_name):
    return ChatCompletionClient(base_url=base_url, api_key=api_key, model_name=model_name)


def llm_client(config_path: str, query: str):
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

    # client = ChatCompletionClient(
    #     base_url=base_url,
    #     api_key=api_key,
    #     model_name=name
    # )
    client = get_client(base_url, api_key, name)

    # 开始循环聊天
    for token in client.create_chat_completion(prompt=query, stream=True):
        print(token, end="", flush=True)



# 示例用法
if __name__ == "__main__":

    while True:
        quary = input("> ")
        llm_client("./config.json", query=quary)

    # client = ChatCompletionClient(
    #     # base_url="http://192.168.0.113:8000/v1",  # wsl下ifconfig获取ip
    #     # base_url="http://localhost:8000/v1",  # localhost访问
    #     base_url="https://api-inference.modelscope.cn/v1",  # localhost访问
    #     # base_url="http://127.0.0.1:8000/v1",
    #     api_key="3ce9e4e5-f3c6-4fee-aa2a-6e2342c70505",
    #     # model_name="RolmOCR/",
    #     model_name="Qwen/Qwen2.5-7B-Instruct"
    # )
    #
    # # 获取可用模型列表
    # # models = client.get_models()
    # # print("可用模型:", models)
    #
    # while True:
    #     prompt = input("> ")
    #
    #     # 开始循环聊天
    #     for token in client.create_chat_completion(prompt=prompt, stream=True):
    #         print(token, end="", flush=True)
    #
    #     print()
    #     print()

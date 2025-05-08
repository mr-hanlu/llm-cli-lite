import argparse
import json
import os
import shutil
from rich.console import Console
from rich.table import Table
# from openai_api import llm_client
from .openai_api_fun import llm_client
import importlib.resources

# 用户配置文件路径
CONFIG_PATH = os.path.expanduser("~/.llm-cli-lite/config.json")

def get_example_config():
    """Read config.example.json from package resources."""
    with importlib.resources.open_text("llm_cli_lite", "config.example.json") as f:
        return json.load(f)

def ensure_config_exists():
    """Ensure config.json exists in user directory, copy from example if needed."""
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        example_config = get_example_config()
        with open(CONFIG_PATH, "w") as f:
            json.dump(example_config, f, indent=4)

def load_config():
    """Load configuration from JSON file, return default if not exists or invalid."""
    ensure_config_exists()
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    """Save configuration to JSON file."""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def list_config(config, console):
    """List all configuration settings in a table."""
    table = Table(title="Configuration Settings")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")

    def flatten_dict(d, parent_key=""):
        """Flatten nested dictionary for display."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key))
            else:
                items.append((new_key, str(v)))
        return items

    for key, value in flatten_dict(config):
        table.add_row(key, value)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="LLM CLI Tool")

    # Config subcommand
    # parser = subparsers.add_parser("config", help="Manage configuration")
    parser.add_argument("query", nargs="?", default=None, help="查询的问题")

    parser.add_argument("-l", "--list", action="store_true", help="列出所有配置设置")

    parser.add_argument("-m", "--models", choices=["ollama", "openai_api"],
                        help="选择使用的模型 ollama/openai_api，默认openai_api")
    parser.add_argument("-k", "--api_key", help="设置api_key")
    parser.add_argument("-u", "--base_url", help="设置openai_api的base_url")
    parser.add_argument("-n", "--model_name", help="设置模型名字")

    args = parser.parse_args()

    console = Console()

    if args.list:
        # List all config settings
        config = load_config()
        list_config(config, console)
    elif args.query is not None:
        try:
            llm_client(CONFIG_PATH, query=args.query)
        except Exception as e:  # 捕获其他可能的异常
            print(f"Error: Request failed. Reason: {str(e)}")

    else:
        # Modify config settings
        config = load_config()

        modified = False

        if args.models == "openai_api":
            config["is_openai_api"] = True
            modified = True
        elif args.models == "ollama":
            config["is_openai_api"] = False
            modified = True

        # 为true，则配置openai_api。否则配置ollama
        is_openai_api = config["is_openai_api"]
        if is_openai_api:
            models = "openai_api"
        else:
            models = "ollama"

        if args.api_key:
            config["models"][models]["api_key"] = args.api_key
            modified = True
        if args.model_name:
            config["models"][models]["model_name"] = args.model_name
            modified = True
        if args.base_url:
            config["models"][models]["base_url"] = args.base_url
            modified = True
        if modified:
            save_config(config)
            console.print(f"[bold green]Configuration updated successfully.[/bold green]")
        else:
            console.print("[bold red]Error: No configuration options provided.[/bold red]")
            parser.print_help()


if __name__ == "__main__":
    main()

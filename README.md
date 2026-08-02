# opencode-python-mcp
The repo aims to run a python mcp server for opencode agent

## Python MCP
Make sure python version is greater than 3.10

1. Setup python mcp package

    ```
    python3 -m venv ~/.py3
    source ~/.py3/bin/activate
    pip3 install mcp
    ```

2. Run mcp server

    ```
    nohup python3 server.py > server.log 2>&1 & disown
    pgrep -f server.py
    ```

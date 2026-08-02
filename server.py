from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# 1. 创建 Server 实例
server = Server("my-custom-tools")

# 2. 注册工具列表
@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
	return [
		types.Tool(
			name="add",
			description="计算两个数字的和",
			inputSchema={
				"type": "object",
				"properties": {
					"a": {"type": "number", "description": "第一个加数"},
					"b": {"type": "number", "description": "第二个加数"},
				},
				"required": ["a", "b"],
			},
		),
		types.Tool(
			name="get_weather",
			description="查询指定城市的模拟天气",
			inputSchema={
				"type": "object",
				"properties": {
					"city": {"type": "string", "description": "城市名称"},
				},
				"required": ["city"],
			},
		),
		types.Tool(
			name="format_markdown_table",
			description="将 JSON 数据格式化为 Markdown 表格",
			inputSchema={
				"type": "object",
				"properties": {
					"data": {
						"type": "array",
						"items": {"type": "object"},
						"description": "要格式化的数据数组",
					},
					"headers": {
						"type": "array",
						"items": {"type": "string"},
						"description": "表头字段名列表",
					},
				},
				"required": ["data", "headers"],
			},
		),
	]

# 3. 实现工具调用逻辑
@server.call_tool()
async def handle_call_tool(
	name: str, arguments: dict
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
	if name == "add":
		result = arguments["a"] + arguments["b"]
		return [types.TextContent(type="text", text=str(result))]
	elif name == "get_weather":
		city = arguments.get("city", "北京")
		weather = f"模拟天气：{city}，天气晴朗，25°C"
		return [types.TextContent(type="text", text=weather)]
	elif name == "format_markdown_table":
		data = arguments.get("data", [])
		headers = arguments.get("headers", [])
		header_line = "| " + " | ".join(headers) + " |"
		separator = "| " + " | ".join(["---"] * len(headers)) + " |"
		rows = []
		for row in data:
			rows.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
		md = "\n".join([header_line, separator] + rows)
		return [types.TextContent(type="text", text=md)]
	else:
		return [types.TextContent(type="text", text="Unknown tool")]

# 4. 启动 Server
async def main():
	async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
		await server.run(
			read_stream,
			write_stream,
			InitializationOptions(
				server_name="my-custom-tools",
				server_version="0.1.0",
				capabilities=server.get_capabilities(
					notification_options=NotificationOptions(),
					experimental_capabilities={},
				),
			),
		)

if __name__ == "__main__":
	import asyncio
	asyncio.run(main())
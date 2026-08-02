from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# 1. 创建 Server 实例
server = Server("python-mcp-server")

# 2. 注册工具列表 (使用 low-level 注册 API)
async def handle_list_tools(
	ctx, params: types.PaginatedRequestParams | None
) -> types.ListToolsResult:
	tools = [
		types.Tool(
			name="add",
			description="计算两个数字的和",
			input_schema={
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
			input_schema={
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
			input_schema={
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
	return types.ListToolsResult(tools=tools)

# 注册工具列表请求处理器
server.add_request_handler("tools/list", types.PaginatedRequestParams, handle_list_tools)

# 3. 实现工具调用逻辑 (tools/call 请求处理器)
async def handle_call_tool(
	ctx, params: types.CallToolRequestParams
) -> types.CallToolResult:
	name = params.name
	arguments = params.arguments or {}

	if name == "add":
		result = arguments.get("a", 0) + arguments.get("b", 0)
		content = [types.TextContent(type="text", text=str(result))]
		return types.CallToolResult(content=content)

	elif name == "get_weather":
		city = arguments.get("city", "北京")
		weather = f"模拟天气：{city} 天气晴朗 25°C"
		content = [types.TextContent(type="text", text=weather)]
		return types.CallToolResult(content=content)

	elif name == "format_markdown_table":
		data = arguments.get("data", []) or []
		headers = arguments.get("headers", []) or []
		if not data or not headers:
			return types.CallToolResult(content=[types.TextContent(type="text", text="(空数据)")])

		header_line = "| " + " | ".join(headers) + " |"
		separator = "| " + " | ".join(["---"] * len(headers)) + " |"
		rows = []
		for row in data:
			rows.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
		md = "\n".join([header_line, separator] + rows)
		return types.CallToolResult(content=[types.TextContent(type="text", text=md)])

	else:
		return types.CallToolResult(content=[types.TextContent(type="text", text=f"Unknown tool: {name}")])

# 注册 tools/call 处理器
server.add_request_handler("tools/call", types.CallToolRequestParams, handle_call_tool)

# 4. 启动 Server
async def main():
	async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
		await server.run(
			read_stream,
			write_stream,
			InitializationOptions(
				server_name="python-mcp-server",
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
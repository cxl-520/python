"""
纯原生Python实现Pytest测试MCP服务（无需fast-mcp）
功能：运行Pytest、读取Excel测试数据、解析测试报告
启动后地址：http://localhost:8000
"""
import http.server
import json
import subprocess
import os
import openpyxl
from urllib.parse import urlparse, parse_qs

# ========== 核心工具函数（和之前一致） ==========
def run_pytest(test_path: str, args: list = ["-v", "-s", "--html=report.html"]) -> dict:
    """运行Pytest测试用例，返回结构化结果"""
    try:
        cmd = ["python", "-m", "pytest"] + args + [test_path]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=os.getcwd()
        )
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "command": " ".join(cmd),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "report_path": os.path.join(os.getcwd(), "report.html")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def read_test_excel(file_path: str, sheet_name: str = "Sheet1") -> dict:
    """读取Excel测试数据"""
    try:
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"文件不存在：{file_path}"}

        wb = openpyxl.load_workbook(file_path, data_only=True)
        sheet = wb[sheet_name]
        headers = [cell.value for cell in sheet[1]]
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(dict(zip(headers, row)))

        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_pytest_failure(report_path: str = "report.html") -> dict:
    """解析Pytest HTML报告"""
    try:
        if not os.path.exists(report_path):
            return {"status": "error", "message": f"报告不存在：{report_path}"}

        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        fail_count = content.count('class="failed"')
        error_msg = content.split('class="error"')[-1].split('</div>')[0] if 'class="error"' in content else "无具体错误信息"

        return {
            "status": "success",
            "fail_count": fail_count,
            "error_msg": error_msg,
            "suggestion": "1. 检查测试数据格式 2. 核对DDT参数传递 3. 确认Excel路径正确性"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ========== MCP服务请求处理器 ==========
class PytestMCPServer(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        """处理AI的POST请求"""
        # 读取请求数据
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        request_data = json.loads(post_data)

        # 路由：根据工具名调用对应函数
        response = {}
        tool_name = request_data.get("tool")
        params = request_data.get("params", {})

        if tool_name == "run_pytest":
            response = run_pytest(
                test_path=params.get("test_path"),
                args=params.get("args", ["-v", "-s", "--html=report.html"])
            )
        elif tool_name == "read_test_excel":
            response = read_test_excel(
                file_path=params.get("file_path"),
                sheet_name=params.get("sheet_name", "Sheet1")
            )
        elif tool_name == "analyze_pytest_failure":
            response = analyze_pytest_failure(
                report_path=params.get("report_path", "report.html")
            )
        else:
            response = {"status": "error", "message": f"未知工具：{tool_name}"}

        # 返回响应
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))

# ========== 启动MCP服务 ==========
if __name__ == "__main__":
    server_address = ('localhost', 9999)
    httpd = http.server.HTTPServer(server_address, PytestMCPServer)
    print("=== Pytest MCP服务启动（纯原生Python）===")
    print(f"服务地址：http://{server_address[0]}:{server_address[1]}")
    print("可用工具：run_pytest / read_test_excel / analyze_pytest_failure")
    print("按Z停止服务")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print("\n=== MCP服务已停止 ===")
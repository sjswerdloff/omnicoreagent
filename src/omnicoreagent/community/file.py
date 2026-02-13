import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from omnicoreagent.core.tools.local_tools_registry import Tool
from omnicoreagent.utils.log import logger

class FileRead:
    def get_tool(self) -> Tool:
        return Tool(
            name="file_read",
            description="Read the contents of a file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "start_line": {"type": "integer"},
                    "end_line": {"type": "integer"},
                },
                "required": ["file_path"],
            },
            function=self._read,
        )

    async def _read(self, file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> Dict[str, Any]:
        try:
            path = Path(file_path)
            if not path.exists():
                return {"status": "error", "data": None, "message": "File not found"}
            
            content = path.read_text(encoding='utf-8')
            
            if start_line is not None and end_line is not None:
                lines = content.splitlines()
                # 1-based indexing for user friendliness maybe? or 0-based? 
                # Let's stick to 0-based for internal consistency, or match standard `view_file`.
                # Logic from legacy tool was: uses slice.
                content = "\n".join(lines[start_line:end_line])
            
            return {
                "status": "success",
                "data": content,
                "message": f"Read file {file_path}"
            }
        except Exception as e:
            return {"status": "error", "data": None, "message": str(e)}

class FileWrite:
    def get_tool(self) -> Tool:
        return Tool(
            name="file_write",
            description="Write content to a file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"},
                    "overwrite": {"type": "boolean", "default": False},
                },
                "required": ["file_path", "content"],
            },
            function=self._write,
        )

    async def _write(self, file_path: str, content: str, overwrite: bool = False) -> Dict[str, Any]:
        try:
            path = Path(file_path)
            if path.exists() and not overwrite:
                return {"status": "error", "data": None, "message": "File exists and overwrite is False"}
            
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            
            return {
                "status": "success",
                "data": {"path": str(path)},
                "message": f"Wrote to {file_path}"
            }
        except Exception as e:
            return {"status": "error", "data": None, "message": str(e)}

class FileList:
    def get_tool(self) -> Tool:
        return Tool(
            name="file_list",
            description="List files in a directory.",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory_path": {"type": "string"},
                },
                "required": ["directory_path"],
            },
            function=self._list,
        )

    async def _list(self, directory_path: str) -> Dict[str, Any]:
        try:
            path = Path(directory_path)
            if not path.exists() or not path.is_dir():
                return {"status": "error", "data": None, "message": "Directory not found"}
            
            files = [str(p.name) for p in path.iterdir()]
            return {
                "status": "success",
                "data": files,
                "message": f"Found {len(files)} items in {directory_path}"
            }
        except Exception as e:
             return {"status": "error", "data": None, "message": str(e)}

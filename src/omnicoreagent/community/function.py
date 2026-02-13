from dataclasses import dataclass
from functools import partial
from importlib.metadata import version
from typing import Any, Callable, Dict, List, Literal, Optional, Sequence, Type, TypeVar, get_type_hints
from dataclasses import dataclass

from docstring_parser import parse
from packaging.version import Version
from pydantic import BaseModel, Field, validate_call

from omnicoreagent.utils.log import log_debug, log_error, log_exception, log_warning

T = TypeVar("T")

def get_entrypoint_docstring(entrypoint: Callable) -> str:
    from inspect import getdoc
    if isinstance(entrypoint, partial):
        return str(entrypoint)
    docstring = getdoc(entrypoint) or ""
    parsed_doc = parse(docstring)
    lines = []
    if parsed_doc.short_description:
        lines.append(parsed_doc.short_description)
    if parsed_doc.long_description:
        lines.extend(parsed_doc.long_description.split("\n"))
    return "\n".join(lines)

@dataclass
class UserInputField:
    name: str
    field_type: Type
    description: Optional[str] = None
    value: Optional[Any] = None

class Function(BaseModel):
    """Model for storing functions that can be called by an agent."""
    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(
        default_factory=lambda: {"type": "object", "properties": {}, "required": []},
        description="JSON Schema object describing function parameters",
    )
    strict: Optional[bool] = None
    entrypoint: Optional[Callable] = None
    
    # Minimal fields for feature parity with @tool
    show_result: bool = False
    
    # Fields used for parsing but not execution
    requires_user_input: Optional[bool] = None
    user_input_fields: Optional[List[str]] = None
    user_input_schema: Optional[List[UserInputField]] = None

    # Agno Legacy fields (kept for compatibility with existing decorators but unused)
    requires_confirmation: Optional[bool] = None
    external_execution: Optional[bool] = None
    stop_after_tool_call: bool = False
    add_instructions: bool = False
    instructions: Optional[str] = None
    pre_hook: Optional[Callable] = None
    post_hook: Optional[Callable] = None
    tool_hooks: Optional[List[Callable]] = None
    cache_results: bool = False
    cache_dir: Optional[str] = None
    cache_ttl: int = 3600

    @classmethod
    def from_callable(cls, c: Callable, name: Optional[str] = None, strict: bool = False) -> "Function":
        from inspect import getdoc, signature
        from omnicoreagent.utils.json_schema import get_json_schema

        function_name = name or c.__name__
        parameters = {"type": "object", "properties": {}, "required": []}
        
        try:
            sig = signature(c)
            type_hints = get_type_hints(c)
            
            # Simple cleanup of type hints
            excluded = {"self", "agent", "team", "run_context", "images", "videos", "audios", "files"}
            
            param_type_hints = {
                name: type_hints.get(name)
                for name in sig.parameters
                if name != "return" and name not in excluded
            }

            param_descriptions = {}
            if docstring := getdoc(c):
                parsed_doc = parse(docstring)
                if parsed_doc.params:
                    for param in parsed_doc.params:
                        p_desc = f"({param.type_name}) {param.description}" if param.type_name else param.description
                        param_descriptions[param.arg_name] = p_desc

            parameters = get_json_schema(
                type_hints=param_type_hints, 
                param_descriptions=param_descriptions, 
                strict=strict
            )
            
            # Set required fields
            if strict:
                 parameters["required"] = list(parameters["properties"].keys())
            else:
                 parameters["required"] = [
                    name for name, param in sig.parameters.items()
                    if param.default == param.empty and name not in excluded
                 ]

        except Exception as e:
            log_warning(f"Could not parse args for {function_name}: {e}")

        entrypoint = cls._wrap_callable(c)
        return cls(
            name=function_name,
            description=get_entrypoint_docstring(entrypoint=c),
            parameters=parameters,
            entrypoint=entrypoint,
        )

    def process_entrypoint(self, strict: bool = False):
        # Kept for compatibility if called explicitly, but effectively a no-op if created via from_callable
        pass

    @staticmethod
    def _wrap_callable(func: Callable) -> Callable:
        from inspect import isasyncgenfunction, iscoroutinefunction
        
        # Don't wrap unless robust pydantic version
        # Simplification: Just return the func if we don't want validation overhead or strict checks
        # But keeping it for safety
        try:
            return validate_call(func, config=dict(arbitrary_types_allowed=True))
        except Exception:
            return func

@dataclass
class ToolResult:
    content: Optional[str] = None
    images: Optional[List[Any]] = None
    videos: Optional[List[Any]] = None
    audios: Optional[List[Any]] = None
    files: Optional[List[Any]] = None


from collections import OrderedDict
from inspect import iscoroutinefunction
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

from omnicoreagent.community.function import Function
from omnicoreagent.core.tools.local_tools_registry import Tool
from omnicoreagent.utils.log import log_debug, log_error, log_warning, logger


class Toolkit:
    _requires_connect: bool = False

    def __init__(
        self,
        name: str = "toolkit",
        tools: Sequence[Union[Callable[..., Any], Function]] = [],
        # Legacy Agno params kept for signature compatibility but mostly ignored
        async_tools: Optional[Sequence[tuple[Callable[..., Any], str]]] = None,
        instructions: Optional[str] = None,
        add_instructions: bool = False,
        include_tools: Optional[list[str]] = None,
        exclude_tools: Optional[list[str]] = None,
        **kwargs,
    ):
        """Initialize a new Toolkit (Simplified for OmniCoreAgent)."""
        self.name: str = name
        self.tools: Sequence[Union[Callable[..., Any], Function]] = tools
        self.functions: Dict[str, Function] = OrderedDict()
        self.include_tools = include_tools
        self.exclude_tools = exclude_tools

        # Register tools
        if self.tools:
            self._register_tools()

    def _register_tools(self) -> None:
        for tool in self.tools:
            self.register(tool)

    def register(self, function: Union[Callable[..., Any], Function], name: Optional[str] = None) -> None:
        try:
            if isinstance(function, Function):
                 # Already a Function object
                 f = function
            else:
                # Create Function from callable
                tool_name = name or function.__name__
                if self.include_tools and tool_name not in self.include_tools:
                    return
                if self.exclude_tools and tool_name in self.exclude_tools:
                    return
                
                f = Function.from_callable(function, name=tool_name)

            self.functions[f.name] = f
            log_debug(f"Function: {f.name} registered with {self.name}")

        except Exception as e:
            log_warning(f"Failed to create Function for: {function}: {e}")

    def get_tools(self) -> List[Tool]:
        """Return a list of Tool objects compatible with OmniCoreAgent."""
        tools = []
        for func_name, func in self.functions.items():
            if func.entrypoint:
                tools.append(
                    Tool(
                        name=func.name,
                        description=func.description or "",
                        inputSchema=func.parameters,
                        # Pass the entrypoint directly. 
                        # Function.entrypoint is already wrapped via validate_call 
                        # or raw callable if validation failed/skipped
                        function=func.entrypoint, 
                    )
                )
        return tools
    
    # Compatibility properties/methods that might be called by legacy code
    @property
    def requires_connect(self) -> bool:
        return self._requires_connect
    
    def connect(self) -> None:
        pass
        
    def close(self) -> None:
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.name} functions={list(self.functions.keys())}>"

    def __str__(self):
        return self.__repr__()

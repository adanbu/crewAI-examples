from typing import Any, Type
from pydantic import BaseModel, Field
from pathlib import Path
from crewai_tools import  BaseTool
import os

class ListDirectoriesInDirectorySchema(BaseModel):
    """Input for ListDirectoriesInDirectoryTool."""
    root_directory_path: str = Field(
        ..., description="The path of the root_directory to list directories of."
    )

class ListDirectoriesInDirectoryTool(BaseTool):
    name: str = "List Directories in Directory"
    description: str = "A tool that returns a list of directories in a given root directory."
    args_schema: Type[BaseModel] = ListDirectoriesInDirectorySchema

    def _run(self, root_directory_path: str, **kwargs: Any) -> Any:
        try:
            # List only directories inside the given path
            directories = [d for d in os.listdir(root_directory_path) if os.path.isdir(os.path.join(root_directory_path, d))]
            if directories:
                return f"Directories inside {root_directory_path} are {directories}"
            else:
                print(f"No directories found in '{root_directory_path}'.")
        except FileNotFoundError:
            print(f"The path '{root_directory_path}' does not exist.")
        except PermissionError:
            print(f"Permission denied to access '{root_directory_path}'.")
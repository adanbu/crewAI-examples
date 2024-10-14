from typing import Any, Optional, Type
from pydantic import BaseModel, Field
from crewai_tools import RagTool
import json
import shutil
from pathlib import Path
from crewai_tools import JSONSearchTool, BaseTool



#is there a need for this?
class LearnLandingPageOptionsSchema(BaseModel):
    """Input for LearnLandingPageOptionsTool."""
    pass  # No input needed for this tool


class LearnLandingPageOptionsTool(BaseTool):
    name: str = "Learn the templates at your disposal"
    description: str = "A tool that provides available landing page templates."
    args_schema: Type[BaseModel] = LearnLandingPageOptionsSchema

    def _run(self, **kwargs: Any) -> Any:
        
        templates = json.load(open("config/templates.json"))
        return json.dumps(templates, indent=2)


 
class CopyLandingPageTemplateSchema(BaseModel):
    """Input for CopyLandingPageTemplateTool."""
    landing_page_template: str = Field(
        ..., description="The name of the landing page template to copy to the project folder."
    )

class CopyLandingPageTemplateTool(BaseTool):
    name: str = "Copy Landing Page Template"
    description: str = "A tool that copies a landing page template to the project folder."
    args_schema: Type[BaseModel] = CopyLandingPageTemplateSchema

    def _run(self, landing_page_template: str, **kwargs: Any) -> Any:
        source_path = Path(f"templates/{landing_page_template}")
        destination_path = Path(f"workdir/{landing_page_template}")
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, destination_path)
        return f"Template copied to {landing_page_template} and ready to be modified."

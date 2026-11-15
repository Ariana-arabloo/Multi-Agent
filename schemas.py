from pydantic import BaseModel, Field
from typing import List

class ProgrammerOutput(BaseModel):
    code: str = Field(description="The main source code of the program")
    language: str = Field(description="Programming language name (e.g., python)")
    explanation: str = Field(description="A short explanation of how the code works")

class TesterOutput(BaseModel):
    is_passed: bool = Field(description="Indicates if the code works without issues")
    bugs_found: List[str] = Field(description="List of errors or bugs found in the code")
    feedback: str = Field(description="Suggestions for improving the code")
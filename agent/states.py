from pydantic import BaseModel,Field,ConfigDict
from typing import Annotated, TypedDict

class State(TypedDict):
    userInput:str
    plan:str
    architect:str
    implementation_list_len:int
    implementation_list_idx:int
    
# For Plan
class Files(BaseModel):
    path:Annotated[str,Field("The dedicated path of fileto be created or modified.")]
    purpose:Annotated[str,Field("The purpose of the file i.e 'Main Application Logic','data processing module','styling file'")]
class PlannerSchema(BaseModel):
    name:Annotated[str,Field(description="The name of app that we have to build.")]
    description:Annotated[str,Field(description="A oneline description of the app. Example: A web app for managing the ToDo list of a person.")]
    techStack:Annotated[str,Field(description="The Tech stack needed to build the app. Example Python, Reacct, flask, Javascript etc.")]
    features:Annotated[list[str], Field(description="A lsit of features that are needed in the app. e.g. 'user suthentication', 'data visualization' etc.")]
    files:Annotated[list[Files],Field(description='The list of files tp bbe created including its path and purpose.')]

# For Architecture
class ImplementationTask(BaseModel):
    path:Annotated[str,Field(description="The path of file that is modified")]
    detail:Annotated[str,Field(description="A detailed description of the task to be performed on the file, e.g. 'add user authentication', 'implement data processing logic', etc")]
class ArchitectSchema(BaseModel):
    implementation:Annotated[list[ImplementationTask],Field(description="The detailed description of list of tasks needed to implemented.")]

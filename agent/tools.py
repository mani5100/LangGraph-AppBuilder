from pathlib import Path
from typing import Tuple
import subprocess
from langchain_core.tools import tool
SAFE_PATH=Path.cwd()/"generatedProject"

def check_safe_path(path: str) -> Path:
    root = SAFE_PATH.resolve()
    p_in = Path(path)
    if p_in.anchor:
        p_in = Path(*p_in.parts[1:])
    p = (root / p_in).resolve()
    if p == root or root in p.parents:
        return p
    raise ValueError("Attempt to write outside project root")

@tool
def write_file(path:str,content):
    """Write content in the specified path within the project root."""
    p=check_safe_path(path)
    p.parent.mkdir(exist_ok=True,parents=True)
    with open(p,"w",encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"

@tool
def read_file(path:str):
    """Read content from the specified path within the project root."""
    p=check_safe_path(path)
    if not p.exists():
        return ""
    with open(p,"r",encoding="utf-8") as f:
        return f.read()
    
@tool
def get_working_directory():
    """This return the current working directory"""
    return str(SAFE_PATH)
@tool
def list_dir(dir_path:str=".")->str:
    """This will return the list of all the files present in the specified directory."""
    p=check_safe_path(dir_path)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files=[]
    for f in p.glob("*/**"):
        if f.is_file():
            file=str(f.relative_to(SAFE_PATH))
            files.append(file)
    if files:
        return "\n".join(files)
    else:
        return "No Files Found"
    
@tool
def run_cmd(cmd:str,cwd:str=None,timeout=30)-> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    if cwd:
        cwd_dir=check_safe_path(cwd)
    else:
        cwd_dir=SAFE_PATH
    response=subprocess.run(
        cmd,
        shell=True,
        cwd=cwd_dir,
        timeout=timeout,
        text=True,
        capture_output=True)
    return response.returncode,response.stdout,response.stderr
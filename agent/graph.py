from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,SystemMessage
from langgraph.graph import StateGraph,START,END
from typing import Literal
from prompts import *
from states import *
from tools import *
from langgraph.prebuilt import create_react_agent
load_dotenv()

        
model=ChatOpenAI(model="gpt-4o")
Tools=[write_file,read_file,get_working_directory,list_dir,run_cmd]
def planner_agent(state:State)->State:
    prompt=planning_prompt(state['userInput'])
    response=model.with_structured_output(PlannerSchema).invoke(prompt)
    return {
        'plan':response
    }
def architect_agent(state:State)->State:
    prompt=architect_prompt(state['plan'])
    response=model.with_structured_output(ArchitectSchema).invoke(prompt)
    return {
        'architect':response,
        "implementation_list_len":len(response.implementation)
    }
def coder_agent(state:State)->State:
    current_task=state["architect"].implementation[state["implementation_list_idx"]]
    existing_content = read_file.invoke(current_task.path)
    human_message=f"""
        File: {current_task.detail}\n
        Task: {current_task.path}\n
        Existing Content: {existing_content} 
        use tools assigned to you to read and write to the file. 
    """
    messages=[
        SystemMessage(content=coder_prompt()),
        HumanMessage(content=human_message)
    ]
    
    agent=create_react_agent(
        model=model,
        tools=Tools
    )
    agent.invoke({"messages":messages})
    return{
        "implementation_list_idx":state["implementation_list_idx"]+1
    }
def router(state:State)->Literal["uncompleted","completed"]:
    if state['implementation_list_idx']<state['implementation_list_len']:
        return "uncompleted"
    else:
        return "completed"

graph=StateGraph(State)
graph.add_node("planner_agent",planner_agent)
graph.add_node("architect_agent",architect_agent)
graph.add_node("coder_agent",coder_agent)
graph.add_edge(START,"planner_agent")
graph.add_edge("planner_agent","architect_agent")
graph.add_edge("architect_agent","coder_agent")
graph.add_conditional_edges("coder_agent",router,{"uncompleted":"coder_agent",'completed':END})
agent=graph.compile()
agent.invoke({
    "userInput":"""
    Create a basic Calculator Website using HTML, Bootstrap CDN and JS. After Completing each file read and check paths and make sure that the scripts are properly working. Don't incllude any pngs.
    make sure that the script and style paths in main files are correctly linked.
    """,
    "implementation_list_idx":0
})
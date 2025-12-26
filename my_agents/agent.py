from google.adk.agents import Agent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
#from google.adk.tools.google_search_tool import google_search //this works for only gemini llm
from google.adk.tools.google_search_agent_tool import GoogleSearchAgentTool


import os

# create default llm
def create_model()->LiteLlm:
    return LiteLlm(
    model= os.getenv("MODEL_NAME", "qwen2.5:7b-instruct"),
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

# create agents
# create google search tool
google_search = GoogleSearchAgentTool(
    agent=Agent(
    name="google_search",
    model=create_model(),
    description="A tool to search the web for relevant information.",
    instruction="Use this tool to search for information on the web to assist with study planning and research tasks.",
))
# planner_research_agent
planner_research_agent = Agent(
    name="planner_research_agent",
    model=create_model(),
    description="A planner agent to plan and research for a given studytask.",
    instruction="""
        You are a planning and research agent. 
        Your task is to create a detailed plan for the given study task and conduct research using the provided tools. 
        
        Follow these steps:
        1. Analyze the study task and break it down into smaller sub-tasks.
        2. Create a step-by-step plan to accomplish the study task.
        3. Use the Google Search tool to gather relevant information for each sub-task.
        4. Compile the research findings and integrate them into the plan.
        Ensure that your plan is clear, concise, and actionable.
        """,     
    tools=[google_search],
    output_key="research_output",
)
# content_agent
content_agent = Agent(
    name="content_agent",
    model=create_model(),
    description="A study content creation agent to generate study materials based on the research_output.",
    instruction="""
        You are a study content creation agent.    
        Use the following research and plan from the previous agent:
        {{planner_research_agent.research_output}}
        Your task is to generate comprehensive study materials.
        Follow these steps:
        1. Review the research output thoroughly.
        2. Organize the information into logical sections or chapters.
        3. Create detailed explanations, examples, and summaries for each section.
        4. Ensure that the content is clear, engaging, and easy to understand.
        5. Format the content appropriately for study materials.
        """,
    output_key="content_output",
)
# quiz_agent
quiz_agent = Agent(
    name="quiz_agent",
    model=create_model(),
    description="A quiz generation agent to create quizzes based on the content_output.",
    instruction="""
        You are a quiz generation agent.
        The original study task was: {{planner_research_agent.research_output}}
        Use the following study content from the previous agent:
        {{content_agent.content_output}}
        Your task is to generate quizzes based on the study content.
        Follow these steps:
        1. Review the content output thoroughly.
        2. Identify key concepts and important information.
        3. Create a variety of question types (multiple choice, true/false) to test understanding.
        4. Ensure that the questions are clear and unambiguous.
        5. Get the correct answers and explanations for each question but do not provide the answers to the user.
        """,
    output_key="quiz_output",
)
# reviewer_agent
reviewer_agent = Agent(
    name="reviewer_agent",
    model=create_model(),
    description="Checks if plan and quizzes cover the original request and suggests tweaks.",
    instruction="""
        You are a reviewer agent.
        The original study task was the users request.
        Use the following plan and quizzes from the previous agents:
        Plan:
        {{planner_research_agent.research_output}}
        Content:
        {{content_agent.content_output}}
        Quizzes:
        {{quiz_agent.quiz_output}}
        Your task is to review the plan and quizzes and suggest potential tweaks or modifications to the plan and quizzes.
        
        Follow these steps:
        1. Review the original study task, plan, and quizzes.
        2. Identify any gaps or areas that need improvement.
        3. Suggest potential tweaks or modifications to the plan and quizzes.
        4. Ensure that the suggestions are clear and actionable.    
        """,
    output_key="review_output",
)

#root_agent
root_agent = SequentialAgent(
    name="root_agent",
    description="Orchestrates the study task in a sequential manner by coordinating other agents.",
    
    sub_agents=[
        planner_research_agent,
        content_agent,
        quiz_agent,
        reviewer_agent,
    ],
    
)
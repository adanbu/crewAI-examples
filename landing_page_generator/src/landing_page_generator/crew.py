from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.template_tools import CopyLandingPageTemplateTool,LearnLandingPageOptionsTool
from tools.directory_tools import ListDirectoriesInDirectoryTool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, DirectoryReadTool, FileWriterTool, FileReadTool,JSONSearchTool

from dotenv import load_dotenv
load_dotenv()

@CrewBase
class ExpandIdeaCrew:
     """ExpandIdea crew"""
     agents_config = 'config/agents.yaml'
     tasks_config = 'config/tasks.yaml'
     
     @agent
     def senior_idea_analyst_agent(self) -> Agent:
        return Agent(
             config=self.agents_config['senior_idea_analyst'],
             allow_delegation=False,
             tools=[
               SerperDevTool(),
               ScrapeWebsiteTool()],
             verbose=True
        )
    
     @agent
     def senior_strategist_agent(self) -> Agent:
        return Agent(
             config=self.agents_config['senior_strategist'],
             allow_delegation=False,
             tools=[
               SerperDevTool(),
               ScrapeWebsiteTool()],
             verbose=True
        )
     
     @task
     def expand_idea(self) -> Task: 
        return Task(
            config=self.tasks_config['expand_idea_task'],
            agent=self.senior_idea_analyst_agent(),
        )
     
     @task
     def refine_idea(self) -> Task: 
        return Task(
            config=self.tasks_config['refine_idea_task'],
            agent=self.senior_strategist_agent(),
        )
     
     @crew
     def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            output_log_file='output1.log'
        )

@CrewBase
class ChooseTemplateCrew:
     """ChooseTemplate crew"""
     agents_config = 'config/agents.yaml'
     tasks_config = 'config/tasks.yaml'

     @agent
     def senior_react_engineer_agent(self) -> Agent:
        return Agent(
             config=self.agents_config['senior_react_engineer'],
             allow_delegation=False,
             tools=[
              
              LearnLandingPageOptionsTool(),
              CopyLandingPageTemplateTool(),
              FileWriterTool(),
              FileReadTool(),
               DirectoryReadTool(),
               ListDirectoriesInDirectoryTool()
              ],
             verbose=True
        )
     
     @agent
     def senior_react_engineer_helper1_agent(self) -> Agent:
        return Agent(
             config=self.agents_config['senior_react_engineer'],
             allow_delegation=False,
             tools=[
               ListDirectoriesInDirectoryTool()
              ],
             verbose=True
        )
     
     @agent
     def senior_react_engineer_helper2_agent(self) -> Agent:
        return Agent(
             config=self.agents_config['senior_react_engineer'],
             allow_delegation=False,
             tools=[
                DirectoryReadTool()
              ],
             verbose=True
        )
     
     @task
     def choose_template(self) -> Task: 
        return Task(
            config=self.tasks_config['choose_template_task'],
            agent=self.senior_react_engineer_agent(),
        )
   
     @task
     def copy_template(self) -> Task: 
        return Task(
            config=self.tasks_config['copy_template_task'],
            agent=self.senior_react_engineer_agent(),
        )
     
     @task
     def choose_relevant_directories(self) -> Task: 
        return Task(
            config=self.tasks_config['choose_relevant_directories_task'],
            agent=self.senior_react_engineer_helper1_agent(),
        )
      
     
     @task
     def choose_components_to_update(self) -> Task: 
        return Task(
            config=self.tasks_config['choose_components_to_update_task'],
            agent=self.senior_react_engineer_helper2_agent(),
        )
     
   #   @task
   #   def update_page(self) -> Task: 
   #      return Task(
   #          config=self.tasks_config['update_page_task'],
   #          agent=self.senior_react_engineer_agent(),
   #      )
     
     @crew
     def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            output_log_file='output2.log'
        )
     
     
@CrewBase
class CreateContentCrew:
     """CreateContent crew"""
     agents_config = 'config/agents.yaml'
     tasks_config = 'config/tasks.yaml'
     
   
     
     @agent
     def senior_content_editor_agent(self) -> Agent:
        return Agent(
             config=self.agents_config['senior_content_editor'],
             allow_delegation=False,
             tools=[
               ],
             verbose=True
        )
     
     @agent
     def senior_react_engineer_agent(self) -> Agent:
        return Agent(
             config=self.agents_config['senior_react_engineer'],
             allow_delegation=False,
             tools=[
              FileWriterTool(),
              FileReadTool(),
              DirectoryReadTool()
              ],
             verbose=True
        )
     
     @task
     def create_content(self) -> Task: 
        return Task(
            config=self.tasks_config['create_component_content_task'],
            agent=self.senior_content_editor_agent(),
        )
     
     @task
     def update_component(self) -> Task: 
        return Task(
            config=self.tasks_config['update_component_task'],
            agent=self.senior_content_editor_agent(),
        )
     
     @task
     def write_updated_component(self) -> Task: 
        return Task(
            config=self.tasks_config['write_updated_component_task'],
            agent=self.senior_react_engineer_agent(),
        )
     
   #   @task
   #   def qa_component(self) -> Task: 
   #      return Task(
   #          config=self.tasks_config['qa_component_task'],
   #          agent=self.senior_content_editor_agent(),
   #      )
     
     @crew
     def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
            output_log_file='output3.log'
        )
import shutil
import sys
from crew import ExpandIdeaCrew, ChooseTemplateCrew, CreateContentCrew
from textwrap import dedent
import os
import json
import ast

def runExpandIdeaCrew(idea):
  inputs1 = {
        "idea": str(idea)
  }
  expanded_idead_path = 'expanded_idea.txt'

  if not os.path.exists(expanded_idead_path) or not os.path.getsize(expanded_idead_path) > 0:
    
    expanded_idea= ExpandIdeaCrew().crew().kickoff(inputs=inputs1)
    print("kicked off first crew")

    try:
      with open('expanded_idea.txt', 'w') as f:
        print(str(expanded_idea), file=f)
    except Exception as e:
        print(f"An error occurred: {e}")

  
  with open('expanded_idea.txt', 'r') as f:
    expanded_idea = str(f.read())

  return expanded_idea

def runChooseTemplateCrew(expanded_idea):
   
    inputs2={
        "idea": expanded_idea
    }
    
    components_json_path = 'components.json'

    if not os.path.exists(components_json_path) or os.path.getsize(components_json_path) == 0:
      components = ChooseTemplateCrew().crew().kickoff(inputs=inputs2)
      print("Kicked off second crew")
      components= str(components)
      print(components)
      components = components.replace("\n", "").replace(" ",
                                                       "").replace("```","").replace("\\", "")
      print(components)
      # Convert the string to a Python list
      try:
        components_paths_list = ast.literal_eval(components)  # Safely parse the string
      except Exception as e:
        print(f"Error parsing the string: {e}")
        components_paths_list = []                                                             
      try:
        # Save the components as JSON
        with open(components_json_path, 'w') as f:
          json.dump(components_paths_list, f, indent=4)
      except Exception as e:
          print(f"An error occurred: {e}")
    
    try:
      # Load the components from JSON
      with open(components_json_path, 'r') as f:
        components_paths_list = json.load(f)
    except Exception as e:
        print(f"An error occurred while reading: {e}")
    
    return components_paths_list


def runCreateContentCrewWrapper(components_paths_list, expanded_idea):
  # for component in components:
    component_path=components_paths_list[0]
    file_content = open(component_path,  "r").read()
    runCreateContentCrew(component_path, expanded_idea, file_content)

def runCreateContentCrew(component_path, expanded_idea, file_content):
    inputs3={
        "component_path": component_path,
        "expanded_idea": expanded_idea,
        "file_content": file_content
    }

    CreateContentCrew().crew().kickoff(inputs=inputs3)

#remove idea as parameter
def run(idea):
    expanded_idea= runExpandIdeaCrew(idea)
    components_paths_list = runChooseTemplateCrew(expanded_idea)
    runCreateContentCrewWrapper(components_paths_list, expanded_idea)
    exit(0)

# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         'query': 'What is last years revenue',
#         'company_stock': 'AMZN',
#     }
#     try:
#         ().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")
    
if __name__ == "__main__":
    print("Welcome to Idea Generator")
    print(dedent("""
    ! YOU MUST FORK THIS BEFORE USING IT !
    """))

    print(dedent("""
      Disclaimer: This will use gpt-4 unless you changed it 
      not to, and by doing so it will cost you money (~2-9 USD).
      The full run might take around ~10-45m. Enjoy your time back.\n\n
    """
  ))
    idea = input("# Describe what is your idea:\n\n")
  
    if not os.path.exists("./workdir"):
        os.mkdir("./workdir")

    if len(os.listdir('./templates')) == 0:
        print(
            dedent("""
                !!! NO TEMPLATES FOUND !!!
                ! YOU MUST FORK THIS BEFORE USING IT !
      
                Templates are not included as they are Tailwind templates. 
                Place Tailwind individual template folders in `./templates`, 
                if you have a license you can download them at
                https://tailwindui.com/templates, their references are at
                `config/templates.json`.
      
                This was not tested this with other templates, 
                prompts in `tasks.py` might require some changes 
                for that to work.
      
                !!! STOPPING EXECUTION !!!
                """)
        )
        exit()

    # crew = LandingPageCrew(idea)
    # crew.run()
    run(idea)
    zip_file = "workdir"
    shutil.make_archive(zip_file, 'zip', 'workdir')
    shutil.rmtree('workdir')
    print("\n\n")
    print("==========================================")
    print("DONE!")
    print(f"You can download the project at ./{zip_file}.zip")
    print("==========================================")

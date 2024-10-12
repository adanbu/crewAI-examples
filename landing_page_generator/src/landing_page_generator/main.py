import shutil
import sys
from crew import ExpandIdeaCrew, ChooseTemplateCrew, CreateContentCrew
from textwrap import dedent
import os
import json

def runExpandIdeaCrew(idea):
    inputs1 = {
        "idea": str(idea)
    }
    expanded_idea= ExpandIdeaCrew().crew().kickoff(inputs=inputs1)
    print("kicked off first crew, expanded idea is:")
    print(expanded_idea)

#remove idea as parameter
def run(idea):
    inputs1 = {
        "idea": str(idea)
    }
    expanded_idea= ExpandIdeaCrew().crew().kickoff(inputs=inputs1)
    print("kicked off first crew")

    inputs2={
        "idea": expanded_idea
    }
    #isnt chosen_template supposed to be in the inputs as well?
    components= ChooseTemplateCrew().crew().kickoff(inputs=inputs2)
    print("kicked off second crew")
    components = components.replace("\n", "").replace(" ",
                                                      "").replace("```", "")
    components = json.loads(components)
    for component in components:
      file_content = open(
        f"./workdir/{component.split('./')[-1]}",
        "r"
      ).read()

    inputs3={
        "components": components,
        "expanded_idea": expanded_idea,
        "file_content": file_content
    }
    CreateContentCrew().crew().kickoff(inputs=inputs3)

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

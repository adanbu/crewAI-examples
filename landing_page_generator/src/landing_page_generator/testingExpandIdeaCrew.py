from crew import ExpandIdeaCrew
from textwrap import dedent


def runExpandIdeaCrew(idea):
    inputs1 = {
        "idea": str(idea)
    }
    expanded_idea= ExpandIdeaCrew().crew().kickoff(inputs=inputs1)
    print("kicked off first crew, expanded idea is:")
    print(expanded_idea)

if __name__ == "__main__":
   
    idea = input("# Describe what is your idea:\n\n")
    runExpandIdeaCrew(idea)
    
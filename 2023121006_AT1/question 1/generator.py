
import argparse
import pytest
import json
import random

def generate(pfsa: dict[str, dict[str, float]], word_count: int) -> str:
    """Generates a string of `word_count` number of words based on PFSA."""
    current_state = "*"  # Start from the initial state
    random_words = []  # List to store generated words
    ans=[]
    for _ in range(word_count):
        # Access the dictionary for the current state
        next_states = pfsa[current_state] #dict "*":next_states


        # Select the next state based on transition probabilities
        probable = random.choices(list(next_states.keys()), weights=list(next_states.values()))[0] #takes element out of list
       # print("---",probable) #single completely random

    
        while(probable[-1]!="*"):  ##probable is most probable word ,word[-1]=="*" end of dict corresponding it
            #print("word probable:",probable)
            
            current_state=probable
            next_states=pfsa[current_state] # probale:{ next_states }

            probable = random.choices(list(next_states.keys()), weights=list(next_states.values()))[0]
            

        #print(",,,",probable[:-1])  # exclue * from end
        ans.append(probable[:-1]) #(probable[:-1]) ,exclue * from end
        current_state="*"
    return " ".join(ans)  #join with " " between words


def main():
    """
    The command for running is `python generator.py text.json 5`. This will
    generate a file `text_sample.txt` which has 5 randomly sampled words.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    parser.add_argument("count", type=int, help="Sample size to gen")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        data = json.load(file)
        output = generate(data, args.count)

    name = args.file.split(".")[0]

    with open(f"{name}_sample.txt", "w") as file:
        file.write(output)


if __name__ == "__main__":
    main()


DICTIONARIES = [
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"c": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
]
STRINGS = [
    "a",
    "a a a a a",
    "",
    "cat cat cat cat",
]
COUNT = [1, 5, 0, 4]

COMBINED = [(d, s, c) for d, (s, c) in zip(DICTIONARIES, zip(STRINGS, COUNT))]


@pytest.mark.parametrize("pfsa, string, count", COMBINED)
def test_output_match(pfsa, string, count):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = generate(pfsa, count)
    assert result == string


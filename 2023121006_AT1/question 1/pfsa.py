

import argparse
import pytest
import json



def assignprob(dic): ##after making count of path ->converts prob = count/total

    if len(dic["*"])==0:  #null string handle// ""
        return {"*":{}}

    
    for x,y in dic.items():
        tot=0
        for ii in y:
            tot+=y[ii]
        #found tot paths
        for ii in y:
            y[ii]=round(y[ii]/tot,2)  #prob ,round to 3 decimal
        
            
    return dic


def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa
    The given example is for the statement "A cat"
    """
    coun={}

    
    
    low=file_str.lower() #lowercase str
    lis=low.split(" ")  #made list "a"  ,"cat" 

    prev=""
    dic={}
    dic["*"]={}
    for ele in lis: ##ele -> each string
        prev=""
        ##print(ele)
        for ind in range(len(ele)):#0->n-1 each char index of curr string
            
            if(ind==0):
                ##print("in zone",ele[ind])
                d={str(ele[0]):1}
                if str(ele[0]) in dic["*"]:
                    d={str(ele[0]):dic["*"][str(ele[0])]+1}#if already present c ,count++
                
                dic["*"].update(d)
                prev+=ele[0]
            else:
                if prev in dic.keys():
                    dd={prev+ele[ind]:1}
                    if prev+ele[ind] in dic[prev].keys():
                        
                        dd={prev+ele[ind]: dic[prev][prev+ele[ind]]+1 }
                    
                    dic[prev].update(dd)
                else:
                    dic[prev]={prev+ele[ind]:1}


                prev+=ele[ind]
            #prin(dic)
        #end of ele for
        if prev in dic.keys():
                dd={prev+"*":1}
                dic[prev].update(dd)
        else:
                dic[prev]={prev+"*":1}
        #dic[prev]={prev+"*":1}
    #end of for

    #tree made ,give their individual prob
        
    
    ###Convert dic having 'count' to 'prob'
    pfsa=assignprob(dic)

    return pfsa



def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    assert result == pfsa
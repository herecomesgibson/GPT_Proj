import sys
import os
import openai
import json
import requests


#basic script for  asking one off questions to chat gpt
#Author: Gibson Olbrys

#OPTIONS -s: specify conduct for the model e.g. you are a helpful assistant, send respnses as though you are a baby, etc(NOTE: only enter the specification for conduct, the script will prompt you to ask a question after)

#TODO 
# add flags for different models or sum'
# sanitize single string input,  i know ';' is breaking it
# create presaved text blocks for specific searches ()


#creat content type and API Key headers
def getheaders():
    with open('Keys/keys.json') as k:
        key_val = json.load(k)["API_KEY"]

    hed = {"Content-Type": "application/json",
           "Authorization": "Bearer " + key_val}
    return hed

# create dict for data to be sent and combine it with headers in a POST request, return JSON obj of response. Checks for a non empty string in system_ins and adds instructions to the req
def sendreq(model, model_url, prompt, system_ins):
    params = { "model": model,
             "messages" : [{ "role": "user", "content": prompt}]
            }
    if system_ins:
        sys_dict = {"role": "system", "content": system_ins}
        params["messages"].insert(0, sys_dict)
    response = requests.post(model_url, headers=getheaders(), json = params)
    return response.json()

#checks for any flags that might be set
def optparse():
    match sys.argv[1]:
        case "-s":
            return (input('system guide accepted, please enter your prompt: '), ' '.join(sys.argv[2:]))
        case _:
            return (' '.join(sys.argv[1:]), "")

def main():
    (prompt, system_ins) = optparse()

    #hardcoded untill there is a reason to change model dynamically
    model = 'gpt-3.5-turbo'
    model_url = "https://api.openai.com/v1/chat/completions"
    response = sendreq(model, model_url, prompt, system_ins)

    print(response["choices"][0]['message']['content'])
    print("\nTotal Toekns used in query: \n" + str(response['usage']['total_tokens']))

if __name__ == "__main__":
    main()
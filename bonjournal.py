import sys
import os
from datetime import date
from datetime import datetime
import glob
import shutil

fg_colors = ["\033[30m","\033[31m","\033[32m","\033[33m","\033[34m","\033[35m","\033[36m","\033[37m"]
fg_color = fg_colors[7];
bg_colors = ["\033[40m","\033[41m","\033[42m","\033[43m","\033[44m","\033[45m","\033[46m","\033[47m"]
bg_color = bg_colors[0];


#globals
prompt = "$ "
response = "> "

#set up log dir
log_path = os.path.dirname(os.path.abspath(__file__))+"\\logs"
if not os.path.exists(log_path):
    os.mkdir(log_path)

#set up journal index
index_path = log_path+"\\index.bji"
if not os.path.exists(index_path):
    open(index_path,'a').close()

#prime screen
os.system("cls")

#print header
print(fg_color+"welcome to BonJournal")

def showHelp():
    print(response+"exit - exits BonJournal")
    print(response+"list - print a list of your journals")
    print(response+"create - create a new journal")
    print(response+"destroy - destroy an existing journal")
    print(response+"show - show journals in explorer")
    print(response+"rename - rename an existing journal")
    print(response+"open - open desired journal")
    print(response+"close - close opened journal")
    print(response+"j - flip backwords through journal")
    print(response+"k - flip forward through journal")
    print(response+"l - create new entry in journal")

def listJournals():
    with open(index_path, 'r') as f:
        journals = f.read().split('\n');
        for journ in journals:
            parts = journ.split('|')
            name = parts[0];
            if name != "":
                bg = int(parts[1])
                fg = int(parts[2])
                print(bg_color+fg_color+response+bg_colors[bg]+fg_colors[fg]+name+bg_color);

    print(bg_color+fg_color+response+"end of list")

def createJournal():
    name_valid=False
    while not name_valid:
        print(response+"Enter \033[1mname\033[22m of new journal")
        name = raw_input(prompt)
        if not os.path.exists(log_path+'\\'+name):
            name_valid=True
        else:
            print(response+bg_colors[1]+fg_colors[7]+"err:"+bg_color+fg_color+" Journal "+name+" already exists.")

    print(response+"Select the \033[1mbackground color\033[22m for your new journal");
    for col in range(len(bg_colors)):
        print(bg_colors[col]+response+str(col)+bg_color)
    
    colorB = int(raw_input(bg_color+prompt))
    print(response+"Select the \033[1mforeground color\033[22m")
    for col in range(len(fg_colors)):
        print(fg_colors[col]+response+str(col))
    colorF = int(raw_input(fg_color+prompt))

    with open(index_path, 'a') as f:
        f.write(name+"|"+str(colorB)+"|"+str(colorF)+'\n')

    os.mkdir(log_path+'\\'+name)
    print(response+"Journal "+bg_colors[colorB]+fg_colors[colorF]+name+fg_color+bg_color+" has been created.")

def destroyJournal(name):
    journPath = log_path+"\\"+name
    if(os.path.exists(journPath)):
        shutil.rmtree(journPath);
    index=""
    found=False
    with open(index_path, 'r') as f:
        journs = f.readlines();
        for line in journs:
            if line.split('|')[0] != name:
                index+=line
            else:
                found=True
    if found:
        os.remove(index_path)
        with open(index_path, 'w') as f:
            f.write(index)
        print(response+bg_colors[2]+fg_colors[7]+"success:"+bg_color+fg_color+" Journal "+name+" has been destroyed")
    else:
        print(response+bg_colors[1]+fg_colors[7]+"err:"+bg_color+fg_color+" Journal "+name+" could not be found")

#main
function=""
while function != "close" and function != "exit":

    #input prompt
    function = raw_input(bg_color+fg_color+prompt)
    parts = function.split(" ")

    #determine command
    if function == "" or parts[0] == 'help' or parts[0] == '?':
        showHelp()
    elif function == "list":
        listJournals()
    elif function == "create":
        createJournal()
    elif parts[0] == "destroy":
        if len(parts) == 1:
            print(response+"usage $ destroy <journal_name>")
        else:
            destroyJournal(parts[1])
    elif function == "show":
        os.system("explorer "+log_path)



#revert to my default theme
os.system('color 0a')
os.system('cls')

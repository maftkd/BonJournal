import sys
import os
from datetime import date
from datetime import datetime
import glob
import shutil
from threading import Thread

fg_colors = ["\033[30m","\033[31m","\033[32m","\033[33m","\033[34m","\033[35m","\033[36m","\033[37m"]
fg_color = fg_colors[7];
bg_colors = ["\033[40m","\033[41m","\033[42m","\033[43m","\033[44m","\033[45m","\033[46m","\033[47m"]
bg_color = bg_colors[0];


#global syntax
prompt = "$ "
response = "> "
key_input = "< "

#get text editor
if len(sys.argv) < 2:
    text_editor="notepad"
else:
    text_editor=sys.argv[1]

#get file explorer
if len(sys.argv) < 3:
    file_browser="explorer"
else:
    file_browser=sys.argv[2]

#get clear command
if file_browser=="explorer":
    clear_command="cls"
else:
    clear_command="clear"

#set up log dir
log_path = os.path.dirname(os.path.abspath(__file__))+"/logs"
if not os.path.exists(log_path):
    os.mkdir(log_path)

#set up journal index
index_path = log_path+"/index.bji"
if not os.path.exists(index_path):
    open(index_path,'a').close()

#prime screen
os.system(clear_command)

#print header
print(fg_color+"welcome to BonJournal")
print(response+"press enter for a list of commands.")

def showHelp():
    print(response+"exit - exits BonJournal")
    print(response+"clear - clears the screen")
    print(response+"list - print a list of your journals")
    print(response+"create - create a new journal")
    print(response+"destroy - destroy an existing journal")
    print(response+"show - show journals in explorer")
    print(response+"write - write a new journal entry")
    print(response+"read - read latest entries from journal")

def listJournals():
    with open(index_path, 'r') as f:
        journals = f.read().split('\n');
        for journ in journals:
            parts = journ.split('|')
            name = parts[0];
            if name != "":
                bg = int(parts[1])
                fg = int(parts[2])
                num_files = len(os.listdir(log_path+'/'+name))
                if num_files>0:
                    num_files -= 1
                print(bg_color+fg_color+response+bg_colors[bg]+fg_colors[fg]+name+bg_color+fg_color+" ("+str(num_files)+")");

    print(bg_color+fg_color+response+"-end of list-")

def createJournal():
    name_valid=False
    while not name_valid:
        print(response+"Enter \033[1mname\033[22m of new journal")
        name = raw_input(prompt)
        if not os.path.exists(log_path+'/'+name):
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

    os.mkdir(log_path+'/'+name)
    print(response+"Journal "+bg_colors[colorB]+fg_colors[colorF]+name+fg_color+bg_color+" has been created.")

def destroyJournal(name):
    journPath = log_path+"/"+name
    if os.path.exists(journPath):
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

def show():
    if file_browser == "explorer":
        os.system(file_browser + " "+log_path.replace('/','\\'))
    else:
        os.system(file_browser + " "+log_path)


def getColors(name):
    with open(index_path, 'r') as f:
        journs = f.readlines()
        for journ in journs:
            parts = journ.split('|')
            if parts[0]==name:
                return (parts[1]+'|'+parts[2])
    return "7|0"

def writeJournal(name):
    journPath = log_path+"/"+name
    if not os.path.exists(journPath):
        print(response+bg_colors[1]+fg_colors[7]+"err:"+bg_color+fg_color+" Journal "+name+" could not be found")
        return
    #determine the next filename
    key_path = journPath+"/keys.bjk"
    if not os.path.exists(key_path):
        open(key_path, 'w').close()
    file_index = "0"
    with open(key_path, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0:
            file_index=str(int(lines[len(lines)-1].split('|')[0])+1)
    #open the file
    file_path = journPath+"/"+file_index+".bj"
    open(file_path, 'w').close()
    t=Thread(target = lambda: os.system(text_editor + " " + file_path))
    t.start()
    #collect keywords
    colors = getColors(name).split('|')
    print(response+"turning a new leaf in "+bg_colors[int(colors[0])]+fg_colors[int(colors[1])]+name+bg_color+fg_color)
    for i in range(3):
        print(response+".")
    print(response+"enter \033[1msearch keys\033[22m for entry followed by \033[1mdone\033[22m")
    key="foo"
    line=file_index
    while key != "done" and key != "":
        key=raw_input(key_input)
        if key != "done" and key != "":
            line += ("|"+key)
    with open(key_path, 'a') as f:
        f.write(line+'\n')
    print(response+"Ok. Search keys have been saved...")

def readJournal(name):
    journPath = log_path+"/"+name
    if not os.path.exists(journPath):
        print(response+bg_colors[1]+fg_colors[7]+"err:"+bg_color+fg_color+" Journal "+name+" could not be found")
        return
    #get list of all .bj's in the journPath
    files=glob.glob(journPath+"/*.bj")
    for file in files:
        file = file.replace('\\','/')
        #print(file)
    colors = getColors(name).split('|')
    print(response+"Opening "+bg_colors[int(colors[0])]+fg_colors[int(colors[1])]+name+bg_color+fg_color+" to latest entry");
    index=len(files)-1
    
    if(index<0):
        print(response+"Nothing here... Write some journals first, and then come back to read them")
        return

    dispJournal(files[index],colors)

    cmd = "foo"
    while cmd != "l" and cmd != "":
        if index==0:
            prev="\033[9mJ for previous\033[29m"
        else:
            prev="J for previous"
        if index==len(files)-1:
            nxt="\033[9mK for next\033[29m"
            print('dbug should be crossing out')
        else:
            nxt="K for next"
        print(response+bg_colors[4]+fg_colors[7]+prev+", "+nxt+", L to leave"+fg_color+bg_color);
        cmd = raw_input(key_input)
        if cmd == "j":
            index-=1;
            if(index<0):
                index=0;
                print(response+"No older entries");
                continue
            dispJournal(files[index],colors)
        elif cmd == "k":
            index += 1;
            if index >= len(files):
                index = len(files)-1;
                print(response+"No newer entries");
                continue
            dispJournal(files[index],colors)


def dispJournal(path,colors):
    os.system(clear_command)
    with open(path, 'r') as f:
        datestr = datetime.fromtimestamp(os.path.getmtime(path)).strftime('%m/%d/%Y %H:%M');
        date = "Date: "+datestr+"\n";
        print(bg_colors[int(colors[0])]+fg_colors[int(colors[1])]+date+f.read()+fg_color+bg_color)


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
        if len(parts) == 1 or parts[1]=="":
            print(response+bg_colors[1]+fg_colors[7]+"err:"+bg_color+fg_color+" usage $ destroy <journal_name>")
        else:
            destroyJournal(parts[1])
    elif function == "show":
        show();
    elif parts[0] == "write":
        if len(parts) == 1:
            print(response+bg_colors[1]+fg_colors[7]+"err:"+bg_color+fg_color+" usage $ write <journal_name>")
        else:
            writeJournal(parts[1])
    elif parts[0] == "read":
        if len(parts) == 1:
            print(response+bg_colors[1]+fg_colors[7]+"err:"+bg_color+fg_color+" usage $ read <journal_name>")
        else:
            readJournal(parts[1])
    elif function == "clear":
        os.system(clear_command)


#revert to my default theme
#os.system('color 0a')
print("\033[0m")
os.system(clear_command)

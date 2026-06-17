Requirements: 

PySide6
watchdog



On Widnows WSL - Ubunto I needed to do the following: 

python3 -m venv venv

source venv/bin/activate


...before I was able to:

pip install -r requirements.txt


To allow execution of run_tests.sh:

chmod +x run_tests.sh

To allow execution of run_parse_debug.sh:

chmod +x run_parse_debug.sh










###########################  Start  ########################### 15.06.2026

First version of the readme file. 

To honor the close-to-gameing flavor of boot.dev, I decided to make a game related project. As I mostly play World of Warcraft, it is about WoW. 

The situation: I have over 20 Characters in retail WoW. To keep track of their progress with Weekly tasks, equipment progression and other different to-dos I have an excel sheet, which I manually update while playing. It's always the same... while in a flow, I forget to update my excel so after a game session I need to login into my different characters and update my excel manually. 

This project should realize a solution, that makes use of existing character information export addons (written by other Authors), extracts relevant information from the exports (typically .txt. files or .csv file, not yet sure which addon I will use), and displays them in a "window"... which might be a locally hosted HTTP static site or a client.

My first step will be to investigate and find a suiting character export tool as well as a good solution for the UI / Dashboard View I want to generate, look at while playing and update. 


###########################  Update 1  ########################### 16.06.2026

I decided to go with the CharacterExport Addon von "Sitttar" which can be found here: https://www.curseforge.com/wow/addons/characterexport It exports strings that can be pasted into .txt files. The export incluides most of the information I'm interested in (and a lot on top to possibly extend the tool in future).

For the frontend layer of my tracker, I picked PySide6 (https://github.com/PySide6-Install/) as I wanted to keep the solution as close to what I learned on boot.dev but still have a frontend I like to look at. PySide6 documentation seems to fit my recuirements and several youtube tutorials can be found, so that I'm confident that I can get something done, that I really like to use afterwards.

Following my investigations, it should be feasibile to use watchdog (https://python-watchdog.readthedocs.io/en/stable/index.html) to automatically update my app when I drop a new .txt file into my import folder. At this point, I do not know yet if this will work as intended and in combination with my PySide6 frontend... but I've seen a filesystemeventhandler which seems to fit my needs. We will see...

As a first architectur draft, I have this beautyful tree for personal orientation: 

midnightchartracker/
│
├── main.py
├── requirements.txt
├── readme.md
├── run_parse_debug.sh
├── run_tests.sh
│
├── import/        
│
├── tests/   
    ├── test_model.py
    ├── test_parser.py
    ├── test_parser_output.py                    
│
├── app/
    ├── model/
    │   ├── character.py
    │   ├── currency.py        
    │
    ├── parser/
    │   ├── txt_parser.py      
    │
    ├── utils/
        └── watcher.py      

(turns out to be super ugly on github... will need to investigate later on how to make it nice. I keep it here for personal orientation never the less)   


The project root folder should only hold the main.py, a requirements.txt, the README.md file and test scripts. Further, it should hold folders to help me structure my additional files. First, there is the import folder, which will be used to drop the character export .txt files I want to parse. The major part of my app will be located in the app folder, which will contain several subfolders. The names I picked are pretty straight forward, so my data models can be found in "model", the parser folder contains the parser to extract data from the source .txt files and utils will contain a watchdog to update data when I drop new character export files into the import folder. Additional utilities will go there too. Last but not least, we have a folder holding my tests.

What is not yet included in the architecture tree above are folders related to the PySide6 frontend, as I'm not yet at the point where I understood what I all need. But certainly, whatever I will need will go to the app folder too.

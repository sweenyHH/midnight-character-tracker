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

###########################  Update 2  ########################### 17.06.2026

I transfered the initial draft versions from the "mct_dev" project folder to the "midnightchartracker" folder and updated git and github. I'm not used to git... and as usual, I screwed up the .gitignore thing so that I now have pycache things on github. Great... Anyway, I guess I need to use it more often. That's why I stop my "dev environment" in mct_dev at this point and from now on, will stick to my "official" project folder. 

So where do we stand? I have the first version of the app running. It is bright as hell as I not yet took care of a dark theme. That will be one of my next steps for sure. 
Further the detail view is kind of raw data import with the first version of progress bars. All ugly, information that one is looking for hard to find. Getting the details view sorted is another planned next step. 

Another important step: I need to split my readme file from the dev diary, which I actually only use to keep track of what I'm doing here... guess not many people want to read this, so I should have a clean readme with brief explanations and important stuff and move the other information to a readme_if_you_are_super_bored file.

For met to not forget where the PySide6 and watchdog input comes from:


Tutorials and sources used for PySide6:

Vids:

Great crash course PySide6  https://www.youtube.com/watch?v=9_NGCpM2r7s
Long tutorial but at least jump points. https://www.youtube.com/watch?v=Z1N9JzNax2k
Playlist with chapters for different parts https://www.youtube.com/playlist?list=PLWLXh53hYMX4JPf860DiZh2DNsn3vbstl
Qt Designer tutorial (maybe later) https://www.youtube.com/watch?v=uzqDnB44qf4

Text / Code:

Well structured PySide6 tutorial https://www.pythonguis.com/pyside6-tutorial/
Documentation https://doc.qt.io/qtforpython-6/tutorials/basictutorial/tablewidget.html

Tutorials and sources used for watchdog:

Vids:

Realtime file and folder monitoring https://www.youtube.com/watch?v=T4xLPnR7W6s
Harder to listen to but useful code examples https://www.youtube.com/watch?v=N1GAFxemtZU
Timestamps, useful code https://www.youtube.com/watch?v=M9CT6MMry0U

Text / Code:

https://www.geeksforgeeks.org/python/create-a-watchdog-in-python-to-look-for-filesystem-changes/
Good step by step tutorial (annoying add popups) https://www.geeksforgeeks.org/python/create-a-watchdog-in-python-to-look-for-filesystem-changes/
Minimal quickstart with code https://python-watchdog.readthedocs.io/en/stable/quickstart.html

###########################  Update 3  ########################### 18.06.2026

I managed to clean up things as planned. So I now have a dark theme for the app, I splited the readme and dev_diary files, I cleaned up my git mess and removed pycache that sneaked in my repository and I moved or better reinstalled venv in the project root (which I installed in the app subfolder by mistake). So things are cleaned up and nice now. 

While testing the app, I noticed that I have a problem with my watchdogs. They were only active on new file creations, but I need them to tackle file changes / new versions of files with the same name, too. 
I seems the issue was caused by my WSL on Windows situation, which forced my to use the PollingObserver. (see https://github.com/gorakhargosh/watchdog/issues/1072 and https://python-watchdog.readthedocs.io/en/stable/api.html?highlight=polling#module-watchdog.observers.polling). So I changed both watcher to use PollingObserver.

The testing still not resulted in what I wanted to see: my app automatically updating when I drop a new file or version of a file in one of my import folders. That was... due to my manual code management. I simply moved a version of my main_window.py to the "official" projectfolder that did not include the update method def _update_ui(self):.

Due to the tinkering with my watchdog, I now have a lot of debug print commands in my main_window.py that I will need to clean later. 

While I came to the conclusion, that I lost a lot of time on the watcher issues sourcing from having WSL on Windows and not a clean Linux environment and thinking about to get a linux system for future work, I realized, that I now build something, that only works on WSL and will probably crash / break on Linux systems, not having a windows filesystem with a source folder to watch and copy files from there to the import folder in the project. I tried to solve this, by implementing "if not os.path.exists" condition into my watcher. 

What I missed again, is to make frequent git commits. Something in me kind of refuses to commit / push code that is not yet done and tested. So even when in my official project folder, I tinker and tinker and don't commit anything. Again, my plan is to do better today, before I learn the hard way why one should frequently commit changes. 

As by now the funcionality in general looks good, the goal for today is to get back to the parser, the main_window and the details_view with the goal to get to a good layout and the information I want to display.
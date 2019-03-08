# BRACKETOLOGY NCAA BRACKET CREATOR with CUSTOM-AI/ML PICK GENERATORS.

version:    0.1.1
author:     Nick Amell
modified:   2019-01-27

--create/compile/run environment: Python 3.6/3.7, Anaconda3 1.7.0, conda v4.4.10, VSCode 1.30.2

### Requirements:
Run the following commands in the terminal (in VSCode, View > Terminal):

pip install -r requirements.txt
conda install python-graphviz

(Note, the latter is for Windows only)

## SECTION-0: Instructions:

1) Install above run environment (instructions see below) SECTION-1 

2) Open VSCode, open folder 'Bracketology'.

3) Open 'makeBracket.py' in VSCode, add any attribute files to 'attributes' folder, link them in 
    'USER-DEFINED DATA CONFIGURED BELOW' sections. SECTION-2

4) In 'makeBracket.py', add any algorithmic heuristics that are required to run custom algorithms.
    These are a list, so can be added in addition to given defaults of rankOnRand and template. SECTION-3

5) Open 'engine' directory, use copy 'templateAlgo.py' as template to create picking algorithm and rename
    it to your own custom name. Include that import path in 'engine.py' in the 'engine' directory at the
    top of the file with other imports. SECTION-4

6) Add custom algorithm picking function call to bottom of 'engine.py' in USER-DEFINED ALGO CONFIGURATION
    section.

7) Once all is modified, run the following commands from the 'Bracketology' folder in the terminal (in VSCode, 
    View > Terminal):

    source activate base
    python makeBracket.py 


## SECTION-1: Installations

    a) Navigate to https://repo.continuum.io/archive/, install "Anaconda3-2018.12-" [OS distribution]
    b) In installer, make sure to select "install VSCode"
    c) Once installed, open Anaconda Navigator.  On the "Home" tab, VSCode should be present.  If not, you'll have to add it.
    d) Click the "Environments" tab on the left.  In the search bar at the top, search and install the following libraries:
        --graphviz (0.10.1)
        --pandas (latest version)
        --numpy (latest version)
    e) Once installed, exit and close Anaconda navigator and open VSCode from your applications/programs search.  (You may also
        open VSCode from Anaconda's "Home" tab directly, by clicking on the "open" button on the VSCode icon.)
    ** From here, follow steps 2-7 above.


## SECTION-2: Attributes

    Attributes are optional, team-specific items of data that can influence your custom picking algorithm. These attributes
    are NOT supplied by the author of this software package but derived or harvested by the users themselves.  Examples of 
    attributes could include a team's winning percentage, a team's road winning percentage, or the like.  These pieces of 
    data are specific to each team - a difference from heuristics which tend to approach matchups in a more general sense.
    
    All attributes should be arranged in a 16 row by 4 column .csv file, as shown by the file 'attribute_template.csv'. 
    Each index corresponds to a single attribute of each team from 'bracket_1.csv'.  For example, the 'East' region, seed '5'
    index would correspond to the 5th seed in the east region from 'bracket_1.csv'.  Each single attribute requires a separate
    .csv file (since .csv files do not allow for tabs, and spreadsheets are not planned on being supported).  

    Each .csv attribute file will be added as a list to the "attfiles" list in 'makeBracket.py'.  The corresponding attribute
    name the user wishes to use will be the same index of the "atts" list.  For example, below, we have 3 attributes we would
    like to add: 'winning percentage', 'road percentage', and 'free throw percentage'.  Assuming we have corresponding .csv 
    files for each, the lists should be initialized as the following:

    atts = ['winning percentage', 'road percentage', 'free throw percentage']
    attfiles = ['winning_percentage.csv', 'road_percentage.csv', 'free_throw_percentage.csv']

    The parser will find those files, located in the "attributes" directory, and import them into the master storage JSON file 
    (a file type for organizing various forms of data). (NOTE: future implementations could generate a SQL_table, a dataframe
    that could act as a database for this sort of information.)


## SECTION-3: Algorithmic heuristics

    Heuristics are optional, matchup-specific items of data that can influence your custom picking algorithm.  These heuristics 
    are NOT supplied by the author of this software package (besides the RandOnRank table) but derived or harvested by the users
    themselves.  Example of a matchup's heuristics could include a normally-distributed percentage chance to win between seed A 
    and seed B.  Unlike attributes, matchups can exist year-to-year regardless of which teams are in specific seeds and regions.

    All heuristics should be arranged in a 16 row by 16 column .csv file, as shown by the 'template.csv' file in the 'heuristics' 
    directory.  Each index corresponds to a seed vs. seed matchup, with the 'row' representing the team of interest and the 'column'
    representing the opponent team.  For example, if a 5th seed faces off against a 12th seed, from the perspective of the 5th seed, 
    the 12th is the opponent.  Therefore, the heuristic value for that matchup would be row 5, column 12.  As expected, there is 
    symmetry to this table from top left to bottom right.  Therefore, row 5 / column 12 (5th seed vs. 12th seed) should have the 
    same heuristic value as row 12 / column 5 (12th seed vs. 5th seed).  

    Each heuristic table is entered into the 'heuristics' list variable in 'makeBracket.py' as shown by the examples of 'randOnRank.csv'
    and 'template.csv'.  To add one's own, copy the 'template.csv' file in the 'heuristics' folder and save the file as your name
    choice and .csv.  These will be added to master storage JSON file.


## SECTION-4: Algorithm implementations

    In the 'engine' directory, one is expected to copy the 'templateAlgo.py' file and save as his or her own '.py' file.  This new
    file will be the heart of the custom picking algorithm.  

    The input variables to the custom algorithm are: teamA, teamB, teamAFull, teamBFull, and heuristic.  
        --teamA/B: [string] name of team; used as variable to set 'winner' (output of algorithm)
        --teamAFull/teamBFull: [object] JSON object that houses seed, region, and any attributes of teamA or teamB.  These can be
                used by the custom algorithm if desired.
        --heuristic: [object/list of lists/matrix] list(s) of lists designed for easy indexing for an algorithm to make matchup 
                decisions and picks.
        --roundNum: rounds 1-6 of games.  Round 1 is first round, 3 is 'Sweet Sixteen' round, 5 is final four games, 6 is finals.

    NOTE: there is currently no support for modifying the master storage JSON file as of yet.  This means that tracking the number of
    algorithmically-picked wins of a team (if an algorithm so chooses to do so) is currently unavailable in version 0.1.x.

    To understand where to access items stored in the master storage JSON file, follow steps 1-4 above (with user-input attributes 
    and heuristics), and run the program with either the 'templateAlgo' or 'rankOnRand'.  Then, go to the 'outputs' directory and
    open the 'bracket_1.json' file.  In VSCode, right click on the opened filed and select 'Format Document'.  The structure of the 
    storage file is shown there.  

    For each match up of teamA and teamB, each team's JSON attribute heirarchy will be supplied by 'teamAFull', and for heuristics,
    each matchup's heuristic table (or tables for multiple heuristics) will be supplied as well.  The following are examples as to 
    how to access various parts of the JSON content:

    --teamA = 'Kentucky'

    --'teamAFull' object (JSON for attributes):
        {"Region": "South", "Seed": "2", "Attributes": {"Winning Percentage": 0.752, "Free Throw Percentage": 0.821}}

        To access Kentucky's free throw percentage, one would make the following call from 'teamAFull':

            ftp = teamAFull["Attributes"]["Free Throw Percentage"]

    --heuristic structure:
        {"Keys": ["randOnRank", "template"], "randOnRank": {"file": "randOnRank.csv", "type": "H2H_table", "array": []} }

        The "array" section of each heuristic holds the head-to-head matchup data.  Note that python is index starting at 0 like
        most programming languages; therefore, a 5th seed vs. 12th seed matchup accessing would be the following:

        win_percentage_of_seedA = heuristic["randOnRank"]["array"][4][11]   # 4 and 11 since 5-1=4 and 12-1=11

    --roundNum: integer values, 1-6
    
                
# Bracketology: an NCAA Bracket Creator as a Custom AI/ML Pick Generator Platform

Latest Version: `0.3.0`, `2021-10-31`

This repo houses a script that allows the user to create python functions that can make picks for the NCAA March Madness tournament. The output of `bracketology.py` are three items:

* The bracket object `bracket_1.json` which houses all of the user-provided attributes, heuristics, and content.
* The bracket image as a png, `NCAABracket.png`.
* The graphviz DOT representation of the bracket object.

## Installation:
1. Install `pip install .` (or `pip install '.'` for zsh).
2. Install `graphviz` for DOT support outside of this python environment. For OSX, use `Homebrew`. For Windows, find the appropriate installation. In both cases, ensure that the path to the `graphviz` module is added to PATH. (`Homebrew` will do this automatically, but you may need to manually add it for Windows.)

## Usage
1. Install above run environment and installations.
2. Test the installation environment by running `python bracketology.py`. There are default configurations that should run regardless of customization or not.
3. Generate the `config/custom/` directory if it does not exist yet.
4. Load all custom content into the directory `config/custom/`. This includes any attribute data and heuristic data. To follow the appropriate templates, use the [attribute_template.csv](config/attribute_template.csv) template to make attribute data sets, and use the [heuristics_template](config/heuristics_template.csv) template to make heuristics data sets. In both cases, take the template and **SAVE AS** your new file. (Do not destroy the actually template files.)
5. Utilize the [template_algorithm.py](config/template_algorithm.py) template to build out your algorithm of choice. You are welcome to create as many helper functions as you choose, however the main function called by the script must match the format.  `template_name` can and _should_ be changed to a name of choice. Recall that you can update this by doing **SAVE AS** on the template file.

```python
def template_name(**kwargs) -> str:
```

6. Ensure all custom files are added to the `config/custom/` directory.
7. Open [config_example.json](config/config_example.json) and **SAVE AS** `config.json`. Move `config.json` to the `config/custom/` directory.
8. Fill out `config.json` with the attributes and heuristics provided. Note that `"name"` does _not_ have to match the file name, so you can fill that in as you wish, following examples below:

```json
{
    "attributes": [
        {
            "name": "name of attribute",
            "path": "config/custom/<attribute_file>"
        }
    ],
    "heuristics": [
        {
            "name": "name of heuristic",
            "path": "config/custom/<heuristic_file>"
        }
    ]
}
```

9. Fill out `config.json` with the algorithm files provided. The key `"algorithm"` will match the processor you wish to ultimately use. If you're looking to include multiple algorithms to test out, you may list them under `"algorithms"`. Ultimately, only one of them will be utilized per run, following examples below:

```json
{
    "algorithm": "single_algorithm_name",
    "algorithms": [
        {
            "name": "single_algorithm_name",
            "function": "script_run"
        }
    ]
}
```

It is of note that, in the example above, `"script_run"` will be the replace `template_name()` as the function name from the template file converted.

10. After things are the way you want them, go ahead and run `python bracketology.py` and evaluate your new algorithms!


## <a name="attributes"></a>Attributes
Attributes are optional, team-specific items of data that can influence your custom picking algorithm. These attributes are NOT supplied by the author of this software package but derived or harvested by the users themselves.  Examples of attributes could include a team's winning percentage, a team's road winning percentage, or the like.  These pieces of data are specific to each team - a difference from heuristics which tend to approach matchups in a more general sense.

All attributes should be arranged in a 16 row by 4 column .csv file, as shown by the file [attribute_template.csv](config/attribute_template.csv). Each index corresponds to a single attribute of each team from `bracket_1.csv`.  For example, the 'East' region, seed '5' index would correspond to the 5th seed in the east region from `bracket_1.csv`.  Each single attribute requires a separate .csv file (since .csv files do not allow for tabs, and spreadsheets are not planned on being supported).  

Each .csv attribute file will be added as a list to the "attribute files" list in `config/custom/config.json`. For example, below, there are 3 attributes we would like to add: _'winning percentage'_, _'road percentage'_, and _'free throw percentage'_.  Assuming we have corresponding .csv files for each, the list should be initialized as the following:

```json
{
    "attributes": [
        {
            "name": "winning percentage",
            "path": "config/custom/winning_percentage.csv"
        },
        {
            "name": "road percentage",
            "path": "config/custom/road_percentage.csv"
        },
        {
            "name": "free throw percentage",
            "path": "config/custom/free_throw_percentage.csv"
        }
    ]
}
```

The parser will find those files, located in the "custom" directory, and import them into the master storage JSON file. (NOTE: future implementations could generate a "SQL-like table", i.e. a data frame that could act as a database for this sort of information.)


## <a name="heuristics"></a>Algorithmic heuristics
Heuristics are optional, matchup-specific items of data that can influence your custom picking algorithm.  These heuristics are NOT supplied by the author of this software package (besides the RandOnRank table) but derived or harvested by the users themselves. Example of a matchup's heuristics could include a normally-distributed percentage chance to win between seed A and seed B.  Unlike attributes, matchups can exist year-to-year regardless of which teams are in specific seeds and regions.

All heuristics should be arranged in a 16 row by 16 column .csv file, as shown by the [template](config/heuristics_template.csv) file in the 'heuristics' directory.  Each index corresponds to a seed vs. seed matchup, with the 'row' representing the team of interest and the 'column' representing the opponent team.  For example, if a 5th seed faces off against a 12th seed, from the perspective of the 5th seed, the 12th is the opponent.  Therefore, the heuristic value for that matchup would be row 5, column 12.  As expected, there is symmetry to this table from top left to bottom right.  Therefore, row 5 / column 12 (5th seed vs. 12th seed) should have the same heuristic value as row 12 / column 5 (12th seed vs. 5th seed).

Each heuristic table is entered into the 'heuristics' list variable in `config/custom/config.json` as shown by the examples of `randOnRank.csv` and `template.csv`. To add one's own, copy the `heuristics_template.csv` file in the 'config' directory and save the file as your name choice and .csv in the `config/custom` directory.  These will be added to master storage JSON file.


## <a name="algorithms"></a>Algorithm implementations

In the 'engine' directory, one is expected to copy the `template_algorithm.py` file and save as their own '.py' file. This new file will be the heart of the custom picking algorithm.  

The input variables to the custom algorithm are: `team_a`, `team_b`, `heuristic`, and `round_num`. All four of these fields are passed to the function as `**kwargs`. See the template to better understand how to utilize these. `team_a` and `team_b` are guaranteed to be required (unless you happen to just want to pick one of them to "win" and ignore the other). Each of these are a dictionary that follow as such:

```python
def template_name(**kwargs) -> str:
    team_a = kwargs.get('team_a')
    team_b = kwargs.get('team_b')
    heuristics = kwargs.get('heuristics')
    round_num = kwargs.get('round_num')
```

One can access the team's name by popping off the top key: `team_a_name = list(team_a.keys())[0]`.

`heuristic` and `round_num` are more optional fields that can help your algorithm. `heuristic` is something you've personally provided, so it's also guaranteed to be included in your algorithm if that's something you've provided to the script. `round_num` can be helpful to an algorithm in more complicated decision-making. For example. if you have different heuristics or algorithms to fire at different rounds of the tournament. Perhaps a simply weighted probability gets you through round 1, but by round 3 (Sweet-Sixteen games), your method of picking has changed. You can use `round_num` to trigger different algorithms in either the `make_pick` function in `engine.py` or in your own custom algorithm.

NOTE: there is currently no support for modifying the master storage JSON file as of yet.  This means that tracking the number of algorithmically-picked wins of a team (if an algorithm so chooses to do so) is currently unavailable in version 0.3.0.

Some examples:

```python
team_a = {'Kentucky': {"Region": "South", "Seed": "2", "Attributes": {"Winning Percentage": 0.752, "Free Throw Percentage": 0.821}}
# To access Kentucky's free throw percentage (or any other team's) programmatically, one would make the following calls from team_a:
team_a_name = list(team_a.keys())[0] # 'Kentucky'
free_throw_percentage = team_a[team_a_name]["Attributes"]
```

```python
# heuristic structure. "H2H_table" is a head-to-head table where the first index refers to the team in question, and the second index refers to the opponent.
heuristic = {"Keys": ["randOnRank", "template"], "randOnRank": {"file": "randOnRank.csv", "type": "H2H_table", "array": []}}

# The "array" section of each heuristic holds the head-to-head matchup data.  Since python indexes at 0, a 5th seed vs. 12th seed matchup accessing would be the following:
win_percentage_of_seed_a = heuristic["randOnRank"]["array"][4][11]   # 4 and 11 since 5-1=4 and 12-1=11

# With the matchup, you could have different percentages of winning for each team depending on heuristic. If by rank probabilities, you could have:
win_percentage_of_seed_a = heuristic["randOnRank"]["array"][4][11]   # (16 - rank) / 16 => (16-5)/16 = about 0.68 chance of winning
win_percentage_of_seed_b = heuristic["randOnRank"]["array"][11][4]   # (16 - rank) / 16 => (16-11)/16 = about 0.32 chance of winning
```

Finally, `round_num` is a simple integer value from 1-6 for each round. Some algorithms, like `randOnRank`, do not use this optional argument.         
# Refactor Progress

## Project
Midnight Character Tracker

---

## Completed

### MainWindow

- Added watcher reload protection
- Added `_reload_running` guard
- Prevents overlapping reload execution
- Removed temporary `time.sleep()` watcher delay

---

### OverviewTab

Refactored from:

```text
set_character()
├── clear layouts
├── delete widgets
├── recreate layouts
├── recreate labels
└── rebuild UI

to:

__init__()
├── create layout once
├── create labels once
├── create widgets once
└── build UI once

set_character()
├── update labels
├── update currency table
├── update NotesWidget
├── update VaultProgressWidget
└── update WeeklyDutiesWidget

Completed: 

Completed:

Removed layout clearing
Removed widget deletion
Removed dynamic layout rebuilding
Added persistent labels
Added persistent Other Currencies label
Added permanent top and bottom layout structure
Fast character switching tested successfully

VaultTab

Refactored from:

set_character()
├── clear grid
├── delete labels
├── recreate labels
├── recreate boxes
└── rebuild entire UI

to:

__init__()
├── create labels once
├── create boxes once
└── build grid once

set_character()
└── update existing box values

Completed:

Added persistent box storage
Added _create_box() helper
Created raid, M+, and delve boxes once
Removed grid clearing
Removed deleteLater()
Removed runtime widget creation
Removed runtime layout rebuilding
Replaced rebuild logic with simple setText() updates
Tested successfully

Current Architecture Notes:

Still To Improve:

reload_all() currently refreshes DetailView using:

self.current_character

after:

self.data_service.load_data()

Future improvement:

load data
find refreshed character
update current_character
refresh DetailView

Planned
Priority 1

RefreshService

Create:

app/services/refresh_service.py


Responsibilities:

refresh_table()
refresh_detail()
full_reload()
Weitere Zeilen anzeigen

Goal:

Centralize refresh logic
Remove duplicate reload paths
Improve debuggability

Priority 2

CharacterTable Optimization

Current behavior:

reload
→ recreate all task checkboxes
→ recreate all cell widgets
Weitere Zeilen anzeigen

Possible future optimization:

build once
update state only
Weitere Zeilen anzeigen

Needs investigation.

Priority 3

Selected Character Refresh

After reload:

self.current_character
Weitere Zeilen anzeigen

should be updated from freshly loaded character data.

Priority 4

UI Polish Pass

Review:

Alignment
Stretch factors
Colors
Spacing
Typography

Deferred until architecture refactor is complete.



# Midnight Character Tracker User Manual

## Introduction

Midnight Character Tracker is a desktop application for managing and tracking World of Warcraft characters.

The application combines imported character data with manually maintained information such as notes, weekly duties, vault progress, and warband tasks.

---

# Getting Started

## Import a Character

First, the data need to be exported from World of Warcraft:

The character data export needs to be done with the Addon CharacterExport , which can be downloaded here: [https://www.curseforge.com/wow/addons/characterexport](https://www.curseforge.com/wow/addons/characterexport)

(The Addon CharacterExport is NOT created or maintained by me! Kudos to the Author Sitttar for his work.)

Recommanded settings for the Addon Export:

Check these boxes: 

- Bags
- Bank
- Character Stats
- Currencies
- Equipment
- Location
- Progress
- Reputations

(checking the other boxes will grow the export significantly while no data is used by Midnight Character Tracker)

To import a character:

1. Start Midnight Character Tracker.
2. Click **Paste Character Data**.
3. Paste a character export.
4. Confirm the import.

The character will appear in the character list.

Existing characters are automatically updated when a new export for the same character is imported.

User-maintained data such as Notes, Weekly Duties, and Vault Progress is preserved during imports.

---

# Character List

The Character List is the application's starting screen.

It provides an overview of all imported characters.

The table displays:

- Character name
- Realm
- Class
- Character level
- Character-specific progress information
- Stored vault progress
- Warband Tasks progress of the character (if warband tasks exist)

To open a character:

1. Select a row.
2. Click the desired character.

---

# Character Detail View

Selecting a character opens the Detail View.

The Detail View contains several tabs that provide different views of the character.

Use the **Back** button to return to the Character List.

---

# Overview Tab

The Overview Tab provides a summary of the selected character.

Information displayed includes:

- Name
- Level
- Race
- Class
- Specialization
- Gold
- Additional currencies

The Overview Tab also contains:

- Notes
- Weekly Duties
- Vault Progress

## Notes

The Notes section allows storing free-form text for a character.

Examples:

- Upgrade plans
- Profession goals
- Raid preparation notes
- Personal reminders

Notes are saved automatically.

## Weekly Duties

Weekly Duties are character-specific checklists.

Use them to track recurring activities that should be completed each week.

Changes are saved automatically.

## Vault Progress

Vault Progress allows recording Great Vault progress directly inside the application.

Three categories are available:

- Raid
- Mythic+
- Delves

Values are saved automatically.

---

# Currencies Tab

The Currencies Tab displays detailed character currency information.

Depending on the imported export, information can include:

- Current amount
- Total limits
- Weekly progression
- Weekly caps

This tab is intended as a quick overview of progression-related currencies.

---

# Vault Tab

The Vault Tab provides a dedicated view of the stored Vault Progress information.

The values shown here are synchronized with the Vault Progress widget on the Overview Tab.

---

# Stats Tab

The Stats Tab displays character statistics and equipment extracted from the imported character data.

Available information depends on the contents of the character export.

---

# Reputation Tab

The Reputation Tab displays reputation information available in the imported export.

This allows quick inspection of important reputation progress and filtering / searching of specific factions.

---

# Debug Tab

The Debug Tab provides a technical view of imported character data.

It is primarily intended for troubleshooting and development purposes.

---

# Warband Tasks

Warband Tasks are shared across all characters.

To open the task list:

1. Click **Warband Tasks**.

Tasks can be:

- Created
- Deleted

Warband Tasks are intended for goals that apply across multiple characters.

Examples:

- Collect a specific item
- Complete an event
- Finish a weekly objective
- Prepare for a new season

A created Task is added to the character list and can be marked as complete by clicking the check box.

---

# Settings

The Settings dialog allows configuration of application options.

Current functionality includes:

- Theme selection
- Number Format selection

Changes are applied immediately.

Further, the settings dialog contains a button to access the applications log files, for easy acces of the log. 
The log provides the author useful information during bug investigations.

---

# Character Deletion

To delete a character:

1. Select the character in the Character List.
2. Choose **Delete Character**.
3. Confirm the deletion.

The imported character file will be removed.

Character deletion cannot be undone. (...but the character can be re-created by importing it again via the paste dialog)

---

# Data Storage

The application stores all data locally on the computer.

This includes:

- Character exports
- Notes
- Weekly Duties
- Vault Progress
- Warband Tasks
- Application settings

No online account is required.

---

# Troubleshooting

## Imported Character Does Not Appear

Verify that the character export was imported successfully and that the import data is complete.

## Notes, Duties, or Vault Progress Seem Missing

Re-open the character and verify that the correct character was selected.

## Application Behaves Unexpectedly

Restart the application and repeat the action.

If the problem persists, create an issue on the project's GitHub page and submit the log file.
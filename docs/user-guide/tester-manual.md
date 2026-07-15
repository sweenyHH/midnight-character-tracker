# Demo Data for Testers

The repository contains demonstration data that allows testing the application without owning or playing World of Warcraft.

Two different types of demo data are provided.

---

# Character Files

Location:

```text
docs/demo-data/char-files/
```

These files represent complete character exports that can be loaded directly by the application.

## How to Use

1. Start Midnight Character Tracker.
2. Open **Settings**.
3. Click **Open Log Folder**.
4. Navigate one level up to the parent folder.
5. Locate the **import** folder.
6. Copy one or more files from:

```text
docs/demo-data/char-files/
```

into the application's **import** folder.
7. Start or restart the application.

The imported characters will appear in the Character List and can be used to test all application functionality.

---

# Parse Files

Location:

```text
docs/demo-data/example-parses/
```

These files are intended for testing the **Paste Character Data** feature.

Unlike the character files above, these files are **not copied into the import folder**.

Instead, their contents are pasted into the application.

## How to Use

1. Open one of the files located in:

```text
docs/demo-data/example-parses/
```

2. Copy the complete contents of the file.
3. Start Midnight Character Tracker.
4. Click **Paste Character Data**.
5. Paste the copied content.
6. Confirm the import.

---

# Parse Files

Files whose names begin with:

"Parse ..."


represent new character exports.

Importing one of these files will create a new character within the application.

Example:

"Parse ExampleCharacter.txt"

creates a new character.

---

# Update Parse Files

Files whose names begin with:

"Update Parse ..."

represent newer exports of an existing character.

These files can be used in two ways:

## Update an Existing Character

If the corresponding character already exists inside the application, importing the update parse will update that character's imported data.

User-maintained data such as Notes, Weekly Duties, and Vault Progress will be preserved.

## Create a Character

If the corresponding character does not yet exist, importing the update parse will create the character.

This allows testers to use update parse files even without first importing the matching character file.

---

# Suggested Test Workflow

A simple test sequence is:

1. Copy one or more files from:

docs/demo-data/char-files/

into the application's import folder.

2. Start the application.

3. Open several characters and explore the available tabs.

4. Create Notes.

5. Update Weekly Duties.

6. Change Vault Progress.

7. Create and complete Warband Tasks.

8. Import one of the files from:

docs/demo-data/example-parses/

using **Paste Character Data**.

9. Verify that the character data updates correctly and that Notes, Weekly Duties, and Vault Progress remain intact.

This workflow covers most of the application's core functionality.
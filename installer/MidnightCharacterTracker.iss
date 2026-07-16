[Setup]
AppName=Midnight Character Tracker
AppVersion=1.0.1
AppPublisher=Malte Maehlmann

SetupIconFile=mct_icon.ico

UninstallDisplayIcon={app}\MidnightCharacterTracker.exe

AppPublisherURL=https://github.com/sweenyHH/midnight-character-tracker
AppSupportURL=https://github.com/sweenyHH/midnight-character-tracker
AppUpdatesURL=https://github.com/sweenyHH/midnight-character-tracker

DefaultDirName={autopf}\Midnight Character Tracker
DefaultGroupName=Midnight Character Tracker

OutputDir=output
OutputBaseFilename=MidnightCharacterTrackerSetup

Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "MidnightCharacterTracker.exe"; DestDir: "{app}"
Source: "_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Icons]
Name: "{group}\Midnight Character Tracker"; Filename: "{app}\MidnightCharacterTracker.exe"
Name: "{autodesktop}\Midnight Character Tracker"; Filename: "{app}\MidnightCharacterTracker.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MidnightCharacterTracker.exe"; Description: "Launch Midnight Character Tracker"; Flags: nowait postinstall skipifsilent
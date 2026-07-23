[Setup]
AppName=Warband Manager
AppVersion=2.0.0
AppPublisher=Malte Maehlmann

SetupIconFile=mct_icon.ico

UninstallDisplayIcon={app}\WarbandManager.exe

AppPublisherURL=https://github.com/sweenyHH/warband-manager
AppSupportURL=https://github.com/sweenyHH/warband-manager
AppUpdatesURL=https://github.com/sweenyHH/warband-manager

DefaultDirName={autopf}\Warband Manager
DefaultGroupName=Warband Manager

OutputDir=output
OutputBaseFilename=WarbandManagerSetup

Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "WarbandManager.exe"; DestDir: "{app}"
Source: "_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Icons]
Name: "{group}\Warband Manager"; Filename: "{app}\WarbandManager.exe"
Name: "{autodesktop}\Warband Manager"; Filename: "{app}\WarbandManager.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\WarbandManager.exe"; Description: "Launch Warband Manager"; Flags: nowait postinstall skipifsilent
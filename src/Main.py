import re
import tkinter as tk
import tkinter.font as tkFont
import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# variables
window = tk.Tk()

teamsOn = False
matchesOn = False
ranksOn = False
teamGraphsOn = False

teamSubbuttons = []
teamSublables = []
lastClickedTeam = None

matchSubbuttons = []
matchSublables = []
lastClickedMatch = None

teamGraphSubbuttons = []
teamGraphSublables = []
lastClickedteamGraph = None
lastTeamGraphFrame = None

offensiveSkillButton = tk.PhotoImage(file="Sprites/OffensiveSkillButton.png")
defensiveSkillButton = tk.PhotoImage(file="Sprites/DefensiveSkillButton.png")
backButton = tk.PhotoImage(file="Sprites/BackButton.png")
genBorderHighlighted = tk.PhotoImage(file="Sprites/GeneralButtonHighlighted.png")
genBorder = tk.PhotoImage(file="Sprites/GeneralButton.png")
teamsButtonSprite = tk.PhotoImage(file="Sprites/TeamsButton.png")
teamsButtonHightlightedSprite = tk.PhotoImage(file="Sprites/TeamsButtonHighlighted.png")
matchesButtonSprite = tk.PhotoImage(file="Sprites/MatchesButton.png")
matchesButtonHightlightedSprite = tk.PhotoImage(file="Sprites/MatchesButtonHighlighted.png")
ranksButtonSprite = tk.PhotoImage(file="Sprites/RanksButton.png")
ranksButtonHightlightedSprite = tk.PhotoImage(file="Sprites/RanksButtonHighlighted.png")
teamGraphsButtonSprite = tk.PhotoImage(file="Sprites/TeamGraphsButton.png")
teamGraphsButtonHightlightedSprite = tk.PhotoImage(file="Sprites/TeamGraphsButtonHighlighted.png")
XButtonSprite = tk.PhotoImage(file="Sprites/XButton.png")

def color_check():
    global teamsOn, matchesOn, ranksOn, teamGraphsOn
    if teamsOn:
        matchesOn = False;
        ranksOn = False;
        teamGraphsOn = False;
    if matchesOn:
        teamsOn = False;
        ranksOn = False;
        teamGraphsOn = False;
    if ranksOn:
        matchesOn = False;
        teamsOn = False;
        teamGraphsOn = False;
    if teamGraphsOn:
        matchesOn = False;
        ranksOn = False;
        teamsOn= False;

    teamsButton.config(image=teamsButtonHightlightedSprite if teamsOn else teamsButtonSprite)
    matchesButton.config(image=(matchesButtonHightlightedSprite if matchesOn else matchesButtonSprite))
    ranksButton.config(image=(ranksButtonHightlightedSprite if ranksOn else ranksButtonSprite))
    teamGraphsButton.config(image=(teamGraphsButtonHightlightedSprite if teamGraphsOn else teamGraphsButtonSprite))

# functions
def on_team_subbutton_click(subbutton):
    global lastClickedTeam
    # Check if lastClickedTeam exists and is a valid button
    if lastClickedTeam is not None and isinstance(lastClickedTeam, tk.Button):
        try:
            # Reset the image of the previously clicked team button (if it exists)
            lastClickedTeam.config(image=genBorder)
        except Exception:
            # Suppress any exception, as it's not critical for functionality
            pass

    # Update the last clicked team
    lastClickedTeam = subbutton

    # Set the new image for the currently clicked team button
    subbutton.config(image=genBorderHighlighted)

def on_match_subbutton_click(subbutton):
    global lastClickedTeam
    if lastClickedTeam is not None:
        lastClickedTeam.config(image=genBorder)
    subbutton.config(image=genBorderHighlighted)
    lastClickedTeam = subbutton

def on_defensive_skill_click(file2, frame):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    scoutingFiles = os.listdir(scoutingPath)

    subframe = tk.Frame(frame, bg="lightgreen")
    subframe.place(x=0, y=0, relwidth=1, relheight=1)  # Use relative width/height to make it fullscreen

    BButton = tk.Button(subframe, image=backButton, width=125, height=125, command=lambda: subframe.destroy())
    BButton.place(x=1778, y=3)

    title = tk.Label(subframe, text=(("Team " + file2) + "s Defensive Skill"), font=("Scrabblefont", 54, "bold"), bg="lightgreen")
    title.place(x=(window.winfo_width()) / 5.5, y=50)

    teamSpecificMatchFiles = [string for string in scoutingFiles if file2 in string]
    teamDefensiveMatchScores = []
    teamSpecificMatches = []

    for i in range(len(teamSpecificMatchFiles)):
        result = teamSpecificMatchFiles[i].split(")")[1].split(")")[0].replace("(", " ")
        teamSpecificMatches.append(result)
        with open(os.path.join(scoutingPath, teamSpecificMatchFiles[i]), 'r') as file:
            content = file.read()
            defSkillNumber = content.split("\n")[30].split(":")[1].replace(" ", "")
            defSkillNumber = int(defSkillNumber)
            teamDefensiveMatchScores.append(defSkillNumber)

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(teamSpecificMatches, teamDefensiveMatchScores, color='blue')

    ax.set_xlabel('Matches')
    ax.set_ylabel('Defensive Score')
    ax.set_title(f"Team {file2}'s Defensive Skill")

    canvas = FigureCanvasTkAgg(fig, subframe)
    canvas.get_tk_widget().place(x=300, y=200, width=1300, height=750)
    canvas.draw()

def on_offensive_skill_click(file2, frame):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    scoutingFiles = os.listdir(scoutingPath)

    subframe = tk.Frame(frame, bg="lightgreen")
    subframe.place(x=0, y=0, relwidth=1, relheight=1)  # Use relative width/height to make it fullscreen

    BButton = tk.Button(subframe, image=backButton, width=125, height=125, command=lambda: subframe.destroy())
    BButton.place(x=1778, y=3)

    title = tk.Label(subframe, text=(("Team " + file2) + "s Offensive Skill"), font=("Scrabblefont", 54, "bold"), bg="lightgreen")
    title.place(x=(window.winfo_width()) / 5.5, y=50)

    teamSpecificMatchFiles = [string for string in scoutingFiles if file2 in string]
    teamOffensiveMatchScores = []
    teamSpecificMatches = []

    for i in range(len(teamSpecificMatchFiles)):
        result = teamSpecificMatchFiles[i].split(")")[1].split(")")[0].replace("(", " ")
        teamSpecificMatches.append(result)
        with open(os.path.join(scoutingPath, teamSpecificMatchFiles[i]), 'r') as file:
            content = file.read()
            offSkillNumber = content.split("\n")[29].split(":")[1].replace(" ", "")
            offSkillNumber = int(offSkillNumber)
            teamOffensiveMatchScores.append(offSkillNumber)

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(teamSpecificMatches, teamOffensiveMatchScores, color='red')

    ax.set_xlabel('Matches')
    ax.set_ylabel('Offensive Score')
    ax.set_title(f"Team {file2}'s Offensive Skill")

    canvas = FigureCanvasTkAgg(fig, subframe)
    canvas.get_tk_widget().place(x=300, y=200, width=1300, height=750)
    canvas.draw()

def on_teamgraph_subbutton_click(file):
    global lastTeamGraphFrame  # Declare it as global

    # Ensure lastTeamGraphFrame is initialized
    if 'lastTeamGraphFrame' not in globals():
        lastTeamGraphFrame = None

    # Remove the previous frame if it exists
    if lastTeamGraphFrame is not None:
        lastTeamGraphFrame.destroy()
        lastTeamGraphFrame = None

    frame = tk.Frame(window, bg="lightblue")
    frame.place(x=0, y=0, relwidth=1, relheight=1)  # Use relative width/height to make it fullscreen

    result = "Team " + file

    label = tk.Label(frame, text=result, font=("Scrabblefont", 72, "bold"), bg="lightblue")
    label.pack(pady=20)

    BButton = tk.Button(frame, image=backButton, width=125, height=125, command=lambda: frame.destroy())
    BButton.place(x=1778, y=3)

    OffensiveButton = tk.Button(frame, image=offensiveSkillButton, width=225, height=120, command=lambda: on_offensive_skill_click(file2=file, frame=frame))
    OffensiveButton.pack(pady=20)

    DefensiveButton = tk.Button(frame, image=defensiveSkillButton, width=225, height=120, command=lambda: on_defensive_skill_click(file2=file, frame=frame))
    DefensiveButton.pack(pady=20)

    lastTeamGraphFrame = frame  # Store the new frame reference


def on_main_button_click(button):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    scoutingFiles = os.listdir(scoutingPath)

    teamsList = set()
    for filename in scoutingFiles:
        match = re.search(r"Team\((\d+)\)", filename)
        if match:
            teamsList.add((match.group(1)))  # Convert to int for sorting if needed

    teamsList = [int(num) for num in teamsList]
    teamsList = sorted(teamsList)
    teamsList = [str(num) for num in teamsList]


    matchesList = set()
    for filename in scoutingFiles:
        match = re.search(r"Match\((\d+)\)", filename)
        if match:
            matchesList.add((match.group(1)))  # Convert to int for sorting if needed

    matchesList = [int(num) for num in matchesList]
    matchesList = sorted(matchesList)
    matchesList = [str(num) for num in matchesList]

    global teamsOn, matchesOn, ranksOn, teamGraphsOn, lastClickedTeam, lastClickedMatch
    
    # Turn all off first
    teamsOn = False
    matchesOn = False
    ranksOn = False
    teamGraphsOn = False

    # Then toggle only the clicked one
    if button == teamsButton:
        teamsOn = True
    elif button == matchesButton:
        matchesOn = True
    elif button == ranksButton:
        ranksOn = True
    elif button == teamGraphsButton:
        teamGraphsOn = True
    
    color_check()

    # Handle cleanup before creating subbuttons for the new active section
    if teamsOn:
        # Remove match subbuttons if any exist
        if matchesOn:
            if len(matchSubbuttons) > 0:
                for subbutton in matchSubbuttons:
                    subbutton.destroy()
                for label in matchSublables:
                    label.unbind("<Button-1>")
                    label.destroy()
            matchSubbuttons.clear()
            matchSublables.clear()
            lastClickedMatch = None
        
        # Create team subbuttons
        y = 100
        i = 0
        x = 100
        for file in teamsList:
            y += 160
            if y > 740:
                y = 260
                x += 320

            result = "Team " + file
            
            subbutton = tk.Button(window, image=genBorder, width=300, height=140, text=result, font=("Scrabblefont", 22, "bold"))
            subbutton.config(command=lambda b=subbutton: on_team_subbutton_click(b))
            subbutton.place(x=x, y=y)

            buttonText = tk.Label(window, text=result, font=("Scrabblefont", 22, "bold"), bg="white")
            buttonText.place(x=150, y=(y + 55))
            buttonText.bind("<Button-1>", lambda e, b=subbutton: on_team_subbutton_click(b))

            teamSubbuttons.append(subbutton)
            teamSublables.append(buttonText)
            i += 1

    # Handle subbutton creation/removal when toggling matches
    if matchesOn:
        # Remove team subbuttons if any exist
        if teamsOn:
            if len(teamSubbuttons) > 0:
                for subbutton in teamSubbuttons:
                    subbutton.destroy()
                for label in teamSublables:
                    label.unbind("<Button-1>")
                    label.destroy()
            teamSubbuttons.clear()
            teamSublables.clear()
            lastClickedTeam = None

        # Create match subbuttons
        y = 100
        i = 0
        x = 100
        for file in matchesList:
            y += 160
            if y > 740:
                y = 260
                x += 320
            result = "Match " + file

            subbutton = tk.Button(window, image=genBorder, width=300, height=140, text=result, font=("Scrabblefont", 22, "bold"))
            subbutton.config(command=lambda b=subbutton: on_match_subbutton_click(b))
            subbutton.place(x=x, y=y)

            buttonText = tk.Label(window, text=result, font=("Scrabblefont", 22, "bold"), bg="white")
            buttonText.place(x=(x + 80), y=(y + 55))
            buttonText.bind("<Button-1>", lambda e, b=subbutton: on_match_subbutton_click(b))

            matchSubbuttons.append(subbutton)
            matchSublables.append(buttonText)

    # Handle subbutton creation/removal when toggling ranks
    if ranksOn:
        # Remove match subbuttons if any exist
        if matchesOn:
            if len(matchSubbuttons) > 0:
                for subbutton in matchSubbuttons:
                    subbutton.destroy()
                for label in matchSublables:
                    label.unbind("<Button-1>")
                    label.destroy()
            matchSubbuttons.clear()
            matchSublables.clear()
            lastClickedMatch = None

        # Cleanup any other subbuttons if needed

    # Handle subbutton creation/removal when toggling teamGraphs
    if teamGraphsOn:
        # Cleanup any other subbuttons if needed
        if matchesOn:
            if len(matchSubbuttons) > 0:
                for subbutton in matchSubbuttons:
                    subbutton.destroy()
                for label in matchSublables:
                    label.unbind("<Button-1>")
                    label.destroy()
            matchSubbuttons.clear()
            matchSublables.clear()
            lastClickedMatch = None
        
        y = 100
        i = 0
        x = 100
        for file in teamsList:
            result = "Team " + file
            y += 160
            if y > 740:
                y = 260
                x += 320
            
            subbutton = tk.Button(window, image=genBorder, width=300, height=140, text=result, font=("Scrabblefont", 22, "bold"))
            subbutton.config(command=lambda b=file: on_teamgraph_subbutton_click(b))
            subbutton.place(x=x, y=y)

            buttonText = tk.Label(window, text=result, font=("Scrabblefont", 22, "bold"), bg="white")
            buttonText.place(x=150, y=(y + 55))
            buttonText.bind("<Button-1>", lambda e, b=file: on_teamgraph_subbutton_click(b))

            teamGraphSubbuttons.append(subbutton)
            teamGraphSublables.append(buttonText)

            i += 1

    # General cleanup logic
    if not teamsOn:
        if len(teamSubbuttons) > 0:
            for subbutton in teamSubbuttons:
                subbutton.destroy()
            for label in teamSublables:
                label.unbind("<Button-1>")
                label.destroy()
        teamSubbuttons.clear()
        teamSublables.clear()
        lastClickedTeam = None

    if not matchesOn:
        if len(matchSubbuttons) > 0:
            for subbutton in matchSubbuttons:
                subbutton.destroy()
            for label in matchSublables:
                label.unbind("<Button-1>")
                label.destroy()
        matchSubbuttons.clear()
        matchSublables.clear()
        lastClickedMatch = None

    if not teamGraphsOn:
        if len(teamGraphSubbuttons) > 0:
            for subbutton in teamGraphSubbuttons:
                subbutton.destroy()
            for label in teamGraphSublables:
                label.unbind("<Button-1>")
                label.destroy()
        teamGraphSubbuttons.clear()
        teamGraphSublables.clear()
        lastClickedteamGraph = None  # Reset last clicked team graph




window.title("ScoutingAppGraph")
window.geometry("1920x1080")  # Width x Height
# window.attributes("-fullscreen", True)

teamsButton = tk.Button(window, image=(teamsButtonHightlightedSprite if teamsOn else teamsButtonSprite), text="Click Me", width=300, height=140, command=lambda: on_main_button_click(teamsButton))    
teamsButton.place(x=20, y=15)
matchesButton = tk.Button(window, image=(matchesButtonHightlightedSprite if matchesOn else matchesButtonSprite), text="Click Me", width=300, height=140, command=lambda: on_main_button_click(matchesButton))    
matchesButton.place(x=350, y=15)
ranksButton = tk.Button(window, image=(ranksButtonHightlightedSprite if ranksOn else ranksButtonSprite), text="Click Me", width=300, height=140, command=lambda: on_main_button_click(ranksButton))    
ranksButton.place(x=680, y=15)
teamGraphsButton = tk.Button(window, image=(teamGraphsButtonHightlightedSprite if teamGraphsOn else teamGraphsButtonSprite), text="Click Me", width=300, height=140, command=lambda: on_main_button_click(teamGraphsButton))    
teamGraphsButton.place(x=1010, y=15)
XButton = tk.Button(window, image=XButtonSprite, width=125, height=125, command=lambda: window.quit())
XButton.place(x=1785, y=3)

window.mainloop()
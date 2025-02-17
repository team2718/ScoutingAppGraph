import json
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

lastClickSubTeam = None
subTeamsChildren = []

matchSubbuttons = []
matchSublables = []
lastClickedMatch = None
lastClickedSubMatch = None
subMatchesChildren = []

teamGraphSubbuttons = []
teamGraphSublables = []
lastClickedteamGraph = None
lastTeamGraphFrame = None

teamBorder = tk.PhotoImage(file="Sprites/TeamBorder.png")
teamBorderHighlighted = tk.PhotoImage(file="Sprites/TeamBorderHighlighted.png")
numberBorder = tk.PhotoImage(file="Sprites/NumberBorder.png")
numberBorderHighlighted = tk.PhotoImage(file="Sprites/NumberBorderHighlighted.png")
backgroundPage = tk.PhotoImage(file="Sprites/Background.png")
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

bg_label = tk.Label(window, image=backgroundPage)
bg_label.place(relwidth=1, relheight=1)

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
def on_team_subbutton_click(subbutton, file):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    scoutingFiles = os.listdir(scoutingPath)
    print(scoutingFiles)
    global lastClickedTeam

    matchesLabel = tk.Label(window, text="Matches", font=("Scrabblefont", 40, "bold"))
    matchesLabel.place(x=700, y=175)

    # Reset previously clicked team button if exists
    if lastClickedTeam is not None and isinstance(lastClickedTeam, tk.Button):
        try:
            lastClickedTeam.config(image=genBorder)
        except Exception:
            pass

    # Update last clicked team
    lastClickedTeam = subbutton
    subbutton.config(image=genBorderHighlighted)

    for widget in subTeamsChildren:
        widget.destroy()
    subTeamsChildren.clear()

    # Find matching files
    pattern = rf'Team\({file}\)Match\(\d+\)Text\.json'
    matches = [file2 for file2 in scoutingFiles if re.fullmatch(pattern, file2)]
    
    matchesList = sorted({str(re.search(r"Match\((\d+)\)", filename).group(1)) for filename in matches})

    x = 650
    y = 110
    for Match in matchesList:
        y += 150
        if y > 410:
            y = 260
            x += 150

        teamsubsubbutton = tk.Button(window, image=numberBorder, width=120, height=120)
        teamsubsublabel = tk.Label(window, text=Match, font=("Scrabblefont", 20, "bold"), bg="#F1EDE7")
        teamsubsublabel.place(x=(x + 52.5), y=(y + 52.5))

        # Pass teamsubsubbutton and teamsubsublabel to the lambda function
        teamsubsubbutton.config(command=lambda btn=teamsubsubbutton, label=teamsubsublabel, teamNumber=file, matchNumber=Match: team_on_subsubbutton_click(subsubbutton=btn, subsublabel=label, file=teamNumber, Match=matchNumber))
        teamsubsubbutton.place(x=x, y=y)
        teamsubsublabel.bind("<Button-1>", lambda event, btn=teamsubsubbutton, label=teamsubsublabel, teamNumber=file, matchNumber=Match: team_on_subsubbutton_click(subsubbutton=btn, subsublabel=label, file=teamNumber, Match=matchNumber))
        subTeamsChildren.append(teamsubsubbutton)
        subTeamsChildren.append(teamsubsublabel)
    subTeamsChildren.append(matchesLabel)

def team_on_subsubbutton_click(subsubbutton, subsublabel, Match, file):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    global lastClickSubTeam

    # Reset previously clicked sub-team button and label background
    if lastClickSubTeam is not None and isinstance(lastClickSubTeam, tk.Button):
        try:
            lastClickSubTeam.config(image=numberBorder)
            lastClickSubTeamLabel.config(bg="#F1EDE7")  # Ensure the previous label is reset
        except Exception:
            pass

    # Update last clicked sub-team and sublabel
    lastClickSubTeam = subsubbutton
    lastClickSubTeamLabel = subsublabel  # Keep track of the label for resetting later

    subsubbutton.config(image=numberBorderHighlighted)
    subsublabel.config(bg="#ECE6E2")

    theJsonFileToOpen = os.path.join(scoutingPath, f'Team({file})Match({Match})Text.json')
    
    with open(theJsonFileToOpen, "r") as theJsonFile:
        content = theJsonFile.read()
        content = content.replace(',', '\n')
        theFileShower = tk.Label(window, text=content, font=("Arial", 17, "bold"), bg="#F1EDE7")
        theFileShower.place(x=1200, y=200)
        subTeamsChildren.append(theFileShower)
        print(subTeamsChildren)

def on_match_subbutton_click(subbutton, file):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    scoutingFiles = os.listdir(scoutingPath)
    global lastClickedMatch
    if lastClickedMatch is not None:
        lastClickedMatch.config(image=genBorder)
    subbutton.config(image=genBorderHighlighted)
    lastClickedMatch = subbutton

    for widget in subMatchesChildren:
        widget.destroy()
    subMatchesChildren.clear()

    teamsLabel = tk.Label(window, text="Teams", font=("Scrabblefont", 40, "bold"))
    teamsLabel.place(x=1000, y=175)

    pattern = re.compile(rf"Match\({file}\)")
    matching_files = [file2 for file2 in scoutingFiles if pattern.search(file2)]

    x = 850
    y = 100
    for teamFile in matching_files:
        y += 150
        teamFile = teamFile.split(')')[0].replace('Team(', '')
        subsubMatchButton = tk.Button(window, image=teamBorder, width=200, height=120)
        subsubMatchButton.place(x=x, y=y)
        subsubMatchLabel = tk.Label(window, text=teamFile, font=("Scrabblefont", 20, "bold"), bg="#F5F1ED")
        subsubMatchLabel.place(x=(x + 66), y=(y + 45))
        subsubMatchButton.config(command=lambda ssb=subsubMatchButton, tf=teamFile, f=file: match_on_subsubbutton_click(subsubbutton=ssb, teamFile=tf, matchFile=f))
        subsubMatchLabel.bind("<Button-1>", lambda event, ssb=subsubMatchButton, tf=teamFile, f=file: match_on_subsubbutton_click(subsubbutton=ssb, teamFile=tf, matchFile=f))
        subMatchesChildren.append(subsubMatchButton)
        subMatchesChildren.append(subsubMatchLabel)
    subMatchesChildren.append(teamsLabel)

def match_on_subsubbutton_click(subsubbutton, teamFile, matchFile):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    global lastClickedSubMatch

    # Reset previously clicked sub-team button and label background
    if lastClickedSubMatch is not None and isinstance(lastClickedSubMatch, tk.Button):
        try:
            lastClickedSubMatch.config(image=teamBorder)
        except Exception:
            pass

    # Update last clicked sub-team and sublabel
    lastClickedSubMatch = subsubbutton
    lastClickedSubMatch.config(image=teamBorderHighlighted)

    theJsonFileToOpen = os.path.join(scoutingPath, f'Team({teamFile})Match({matchFile})Text.json')
    with open(theJsonFileToOpen, "r") as theJsonFile:
        content = theJsonFile.read()
        content = content.replace(',', '\n')
        theFileShower = tk.Label(window, text=content, font=("Arial", 17, "bold"), bg="#F1EDE7")
        theFileShower.place(x=1300, y=200)
        subMatchesChildren.append(theFileShower)

'''
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
'''

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
            content = json.load(file)

            auto1Number = content["autoL1"]
            auto2Number = content["autoL2"]
            auto3Number = content["autoL3"]
            auto4Number = content["autoL4"]

            teleop1Number = content["teleopL1"]
            teleop2Number = content["teleopL2"]
            teleop3Number = content["teleopL3"]
            teleop4Number = content["teleopL4"]

            auto1Number *= 3
            auto2Number *= 4
            auto3Number *= 6
            auto4Number *= 7

            teleop1Number *= 2
            teleop2Number *= 3
            teleop3Number *= 4
            teleop4Number *= 5

            teamOffensiveMatchScores.append(
                auto1Number +
                auto2Number +
                auto3Number +
                auto4Number +
                teleop1Number +
                teleop2Number +
                teleop3Number +
                teleop4Number
            )

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(teamSpecificMatches, teamOffensiveMatchScores, color='red')
    ax.plot(teamSpecificMatches, teamOffensiveMatchScores, color='blue', marker='o', linestyle='-', label="Avg Score")

    ax.set_xlabel('Matches')
    ax.set_ylabel('Total Score')
    ax.set_title(f"Team {file2}'s Offensive Skill")

    canvas = FigureCanvasTkAgg(fig, subframe)
    canvas.get_tk_widget().place(x=300, y=200, width=1300, height=750)
    canvas.draw()

def on_ranks_offensive_click(frame):
    scoutingPath = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Documents", "ScoutingData")
    scoutingFiles = os.listdir(scoutingPath)
    teamOffensiveMatchScores = []
    trueTeamOffensiveMatchScores = []

    subframe = tk.Frame(frame, bg="lightgreen")
    subframe.place(x=0, y=0, relwidth=1, relheight=1)

    label = tk.Label(subframe, text="Ranked Offensive Skill", font=("Scrabblefont", 72, "bold"), bg="lightgreen")
    label.pack(pady=20)

    BButton = tk.Button(subframe, image=backButton, width=125, height=125, command=lambda: subframe.destroy())
    BButton.place(x=1778, y=3)

    unique_teams = set()
    pattern = re.compile(r"Team\((\d+)\)")

    for file in scoutingFiles:
        match = pattern.search(file)
        if match:
            unique_teams.add(match.group(1))

    unique_teams = list(unique_teams)
    unique_teams.sort()

    for i in range(len(unique_teams)):
        teamSpecificMatchFiles = [string for string in scoutingFiles if unique_teams[i] in string]
        for i in range(len(teamSpecificMatchFiles)):
            with open(os.path.join(scoutingPath, teamSpecificMatchFiles[i]), 'r') as file:
                content = json.load(file)

                auto1Number = content["autoL1"]
                auto2Number = content["autoL2"]
                auto3Number = content["autoL3"]
                auto4Number = content["autoL4"]

                teleop1Number = content["teleopL1"]
                teleop2Number = content["teleopL2"]
                teleop3Number = content["teleopL3"]
                teleop4Number = content["teleopL4"]

                auto1Number *= 3
                auto2Number *= 4
                auto3Number *= 6
                auto4Number *= 7

                teleop1Number *= 2
                teleop2Number *= 3
                teleop3Number *= 4
                teleop4Number *= 5

                teamOffensiveMatchScores.append(
                    auto1Number +
                    auto2Number +
                    auto3Number +
                    auto4Number +
                    teleop1Number +
                    teleop2Number +
                    teleop3Number +
                    teleop4Number
                )
        average = sum(teamOffensiveMatchScores) / len(teamOffensiveMatchScores)
        teamOffensiveMatchScores.clear()
        trueTeamOffensiveMatchScores.append(average)
    print(trueTeamOffensiveMatchScores)

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(unique_teams, trueTeamOffensiveMatchScores, color='red')

    ax.set_xlabel('Teams')
    ax.set_ylabel('Average Offensive Score')
    ax.set_title(f"Average Teams Offensive Score")

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

    # DefensiveButton = tk.Button(frame, image=defensiveSkillButton, width=225, height=120, command=lambda: on_defensive_skill_click(file2=file, frame=frame))
    # DefensiveButton.pack(pady=20)

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
        for widget in subTeamsChildren:
            widget.destroy()
        subTeamsChildren.clear()
        for widget in subMatchesChildren:
            widget.destroy()
        subMatchesChildren.clear()
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
            subbutton.config(command=lambda b=subbutton, f=file: on_team_subbutton_click(subbutton=b, file=f))
            subbutton.place(x=x, y=y)

            buttonText = tk.Label(window, text=result, font=("Scrabblefont", 22, "bold"), bg="white")
            buttonText.place(x=150, y=(y + 55))
            buttonText.bind("<Button-1>", lambda e, b=subbutton, f=file: on_team_subbutton_click(subbutton=b, file=f))

            teamSubbuttons.append(subbutton)
            teamSublables.append(buttonText)
            i += 1

    # Handle subbutton creation/removal when toggling matches
    if matchesOn:
        for widget in subTeamsChildren:
            widget.destroy()
        subTeamsChildren.clear()
        for widget in subMatchesChildren:
            widget.destroy()
        subMatchesChildren.clear()
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
            subbutton.config(command=lambda b=subbutton, f=file: on_match_subbutton_click(subbutton=b, file=f))
            subbutton.place(x=x, y=y)

            buttonText = tk.Label(window, text=result, font=("Scrabblefont", 22, "bold"), bg="white")
            buttonText.place(x=(x + 80), y=(y + 55))
            buttonText.bind("<Button-1>", lambda e, b=subbutton, f=file: on_match_subbutton_click(subbutton=b, file=f))

            matchSubbuttons.append(subbutton)
            matchSublables.append(buttonText)

    # Handle subbutton creation/removal when toggling ranks
    if ranksOn:
        for widget in subTeamsChildren:
            widget.destroy()
        subTeamsChildren.clear()
        for widget in subMatchesChildren:
            widget.destroy()
        subMatchesChildren.clear()
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

        frame = tk.Frame(window, bg="lightblue")
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(frame, text="Ranks", font=("Scrabblefont", 72, "bold"), bg="lightblue")
        label.pack(pady=20)

        BButton = tk.Button(frame, image=backButton, width=125, height=125, command=lambda: frame.destroy())
        BButton.place(x=1778, y=3)

        OffensiveRanksButton = tk.Button(frame, image=offensiveSkillButton, width=225, height=120, command=lambda: on_ranks_offensive_click(frame=frame))
        OffensiveRanksButton.pack(pady=20)
        # Cleanup any other subbuttons if needed

    # Handle subbutton creation/removal when toggling teamGraphs
    if teamGraphsOn:
        for widget in subTeamsChildren:
            widget.destroy()
        subTeamsChildren.clear()
        for widget in subMatchesChildren:
            widget.destroy()
        subMatchesChildren.clear()
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
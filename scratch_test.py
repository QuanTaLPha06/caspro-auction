import json
import os

# Create Python script to assemble the questions and generate Sports_Connection_Quiz.html

easy_questions = [
    {
        "id": "E01", "difficulty": "easy", "type": "connection", "sport": "Football",
        "title": "Global Football Legends",
        "clues": ["Clue 1: Lionel Messi", "Clue 2: Cristiano Ronaldo", "Clue 3: Pelé", "Clue 4: Diego Maradona"],
        "answer": "Football GOATs / Ballon d'Or & World Cup Icons",
        "explanation": "All four are widely celebrated as the greatest football players of all time."
    },
    {
        "id": "E02", "difficulty": "easy", "type": "connection", "sport": "Tennis",
        "title": "Grand Slam Tournaments",
        "clues": ["Clue 1: Wimbledon (London)", "Clue 2: Roland Garros (Paris)", "Clue 3: US Open (New York)", "Clue 4: Australian Open (Melbourne)"],
        "answer": "The Four Tennis Grand Slam Tournaments",
        "explanation": "These comprise the four major annual tennis tournaments in the world."
    },
    {
        "id": "E03", "difficulty": "easy", "type": "connection", "sport": "Cricket",
        "title": "Cricket World Champions",
        "clues": ["Clue 1: Australia (6 titles)", "Clue 2: India (2 titles)", "Clue 3: West Indies (2 titles)", "Clue 4: England (1 title)"],
        "answer": "Men's ODI Cricket World Cup Champions",
        "explanation": "All these nations have won the ICC Men's 50-over Cricket World Cup."
    },
    {
        "id": "E04", "difficulty": "easy", "type": "connection", "sport": "Dodgeball",
        "title": "Dodgeball Basics",
        "clues": ["Clue 1: Opening Rush at center line", "Clue 2: Foam or Rubber balls", "Clue 3: Catching a ball revives a teammate", "Clue 4: Getting hit means you are OUT"],
        "answer": "Core Rules of Dodgeball",
        "explanation": "These represent the fundamental rules and phase progression of a dodgeball match."
    },
    {
        "id": "E05", "difficulty": "easy", "type": "connection", "sport": "Kho Kho",
        "title": "Kho Kho Fundamentals",
        "clues": ["Clue 1: 8 Seated Chasers facing opposite directions", "Clue 2: 1 Active Chaser pursuing defenders", "Clue 3: Tapping a teammate's back and shouting 'KHO!'", "Clue 4: Two wooden poles at court ends"],
        "answer": "Essential Rules of Kho Kho",
        "explanation": "Describes the seated chasers, active chaser call, and field layout of traditional Kho Kho."
    },
    {
        "id": "E06", "difficulty": "easy", "type": "connection", "sport": "Basketball",
        "title": "Basketball Court Positions",
        "clues": ["Clue 1: Point Guard", "Clue 2: Shooting Guard", "Clue 3: Small Forward", "Clue 4: Power Forward & Center"],
        "answer": "The 5 Standard Positions in Basketball",
        "explanation": "These are the traditional five player positions on a basketball team."
    },
    {
        "id": "E07", "difficulty": "easy", "type": "connection", "sport": "Olympics",
        "title": "Olympic Symbol",
        "clues": ["Clue 1: Blue and Yellow", "Clue 2: Black and Green", "Clue 3: Red", "Clue 4: White background"],
        "answer": "Colors of the 5 Olympic Rings & Flag",
        "explanation": "The Olympic rings feature five colors (blue, yellow, black, green, red) representing the five inhabited continents."
    },
    {
        "id": "E08", "difficulty": "easy", "type": "connection", "sport": "Formula 1",
        "title": "F1 Champions",
        "clues": ["Clue 1: Lewis Hamilton", "Clue 2: Michael Schumacher", "Clue 3: Max Verstappen", "Clue 4: Ayrton Senna"],
        "answer": "Multiple-time Formula 1 World Drivers' Champions",
        "explanation": "Each of these drivers has won multiple F1 Drivers' World Championships."
    },
    {
        "id": "E09", "difficulty": "easy", "type": "connection", "sport": "Athletics",
        "title": "Sprint Events",
        "clues": ["Clue 1: 100 meters", "Clue 2: 200 meters", "Clue 3: 400 meters", "Clue 4: 4x100m Relay"],
        "answer": "Track Sprint Events in Athletics",
        "explanation": "These are the primary short-distance sprint categories in athletics."
    },
    {
        "id": "E10", "difficulty": "easy", "type": "connection", "sport": "Badminton",
        "title": "Badminton Gear & Play",
        "clues": ["Clue 1: Goose feather or nylon projectile", "Clue 2: Light racket with tight strings", "Clue 3: 5ft (1.55m) high net", "Clue 4: Played to 21 points per game"],
        "answer": "Badminton Equipment & Scoring System",
        "explanation": "Describes the shuttlecock, racket, net height, and 21-point rally scoring system."
    },
    {
        "id": "E11", "difficulty": "easy", "type": "connection", "sport": "Golf",
        "title": "Golf Majors",
        "clues": ["Clue 1: Green Jacket at Augusta", "Clue 2: Wanamaker Trophy at PGA Championship", "Clue 3: US Open Trophy", "Clue 4: Claret Jug at The Open"],
        "answer": "Trophies of Men's Golf 4 Major Championships",
        "explanation": "These are the four coveted trophies awarded for winning golf's major tournaments."
    },
    {
        "id": "E12", "difficulty": "easy", "type": "connection", "sport": "Swimming",
        "title": "Swimming Strokes",
        "clues": ["Clue 1: Freestyle (Front Crawl)", "Clue 2: Backstroke", "Clue 3: Breaststroke", "Clue 4: Butterfly"],
        "answer": "The Four Competitive Swimming Strokes",
        "explanation": "These form the four official strokes in Olympic swimming competitions."
    },
    {
        "id": "E13", "difficulty": "easy", "type": "connection", "sport": "Boxing",
        "title": "Boxing Legends",
        "clues": ["Clue 1: Muhammad Ali", "Clue 2: Mike Tyson", "Clue 3: Manny Pacquiao", "Clue 4: Floyd Mayweather Jr."],
        "answer": "Undefeated or World Champion Boxing Icons",
        "explanation": "All four are iconic world champion boxers across various eras."
    },
    {
        "id": "E14", "difficulty": "easy", "type": "connection", "sport": "Baseball",
        "title": "Diamond Bases",
        "clues": ["Clue 1: Home Plate", "Clue 2: First Base", "Clue 3: Second Base", "Clue 4: Third Base"],
        "answer": "Bases on a Baseball Infield Diamond",
        "explanation": "A runner must touch all four bases in order to score a run in baseball."
    },
    {
        "id": "E15", "difficulty": "easy", "type": "connection", "sport": "Volleyball",
        "title": "Volleyball Touches",
        "clues": ["Clue 1: Bump (Pass)", "Clue 2: Set", "Clue 3: Spike (Attack)", "Clue 4: Maximum 3 hits per side"],
        "answer": "Standard 3-Hit Play Sequence in Volleyball",
        "explanation": "Teams typically use pass, set, spike within the allowed 3 contacts before sending the ball over."
    },
    {
        "id": "E16", "difficulty": "easy", "type": "connection", "sport": "Dodgeball",
        "title": "Dodgeball Court Zones",
        "clues": ["Clue 1: Center Line", "Clue 2: Attack Line (3-meter mark)", "Clue 3: Back Line", "Clue 4: Out-of-Bounds Queue"],
        "answer": "Markings & Boundary Zones on a Dodgeball Court",
        "explanation": "Dodgeball courts feature center lines, attack lines, perimeter boundaries, and player benches."
    },
    {
        "id": "E17", "difficulty": "easy", "type": "connection", "sport": "Kho Kho",
        "title": "Kho Kho Turns",
        "clues": ["Clue 1: 3 Defenders enter the court in batches", "Clue 2: Chaser must give KHO from behind a seated player", "Clue 3: Pole turn around to change direction", "Clue 4: Innings last 9 minutes"],
        "answer": "Rules Governing Chasing and Defending in Kho Kho",
        "explanation": "Kho Kho matches feature defender batches of 3, strict KHO giving rules, and timed innings."
    },
    {
        "id": "E18", "difficulty": "easy", "type": "connection", "sport": "Cricket",
        "title": "Ways Out in Cricket",
        "clues": ["Clue 1: Bowled (stumps hit)", "Clue 2: Caught by fielder", "Clue 3: LBW (Leg Before Wicket)", "Clue 4: Run Out"],
        "answer": "Most Common Modes of Dismissal in Cricket",
        "explanation": "These are the four most frequent ways a batter gets out in cricket."
    },
    {
        "id": "E19", "difficulty": "easy", "type": "connection", "sport": "Tennis",
        "title": "Tennis Game Point Progression",
        "clues": ["Clue 1: Love (0)", "Clue 2: 15", "Clue 3: 30", "Clue 4: 40"],
        "answer": "Tennis Point Scoring Order within a Single Game",
        "explanation": "In tennis, points progress from Love to 15, 30, 40, and Game."
    },
    {
        "id": "E20", "difficulty": "easy", "type": "connection", "sport": "Football",
        "title": "Football Officials",
        "clues": ["Clue 1: Main Referee on the pitch", "Clue 2: Two Assistant Referees (Linesmen)", "Clue 3: Fourth Official on sideline", "Clue 4: VAR (Video Assistant Referee)"],
        "answer": "Match Official Roles in Professional Football",
        "explanation": "Professional football matches are officiated by referee, linesmen, 4th official, and VAR team."
    }
]

# Generate remaining Easy questions (E21 to E60)
easy_topics = [
    ("Basketball", "NBA Legendary Teams", "Lakers", "Celtics", "Bulls", "Warriors", "Most Successful NBA Franchises"),
    ("Cricket", "Famous Cricket Stadiums", "Lords (London)", "Eden Gardens (Kolkata)", "MCG (Melbourne)", "Wankhede (Mumbai)", "Iconic International Cricket Grounds"),
    ("Tennis", "Court Surfaces", "Grass (Wimbledon)", "Clay (Roland Garros)", "Hard Court (US/Aus Open)", "Carpet (Indoor historical)", "Professional Tennis Playing Surfaces"),
    ("Football", "Premier League Big 6", "Manchester United", "Liverpool", "Arsenal", "Chelsea", "Traditional English Premier League Heavyweights"),
    ("Olympics", "Summer Olympic Sports", "Athletics", "Gymnastics", "Swimming", "Weightlifting", "Core Summer Olympic Sports"),
    ("Athletics", "Field Events", "Long Jump", "High Jump", "Shot Put", "Javelin Throw", "Classic Athletics Field Discipline Competitions"),
    ("F1", "F1 Teams / Constructors", "Ferrari", "McLaren", "Red Bull Racing", "Mercedes-AMG", "Top Formula 1 Constructors"),
    ("Dodgeball", "Dodgeball Throw Types", "Power Throw", "Curve Throw", "Drop Shot", "Synchronized Team Volley", "Attacking Throw Techniques in Dodgeball"),
    ("Kho Kho", "Kho Kho Skills", "Single Chain", "Double Chain", "Ring Game", "Dodging & Zig-Zag", "Defensive Footwork Patterns in Kho Kho"),
    ("Table Tennis", "Table Tennis Essentials", "Celluloid / Plastic Ball", "Rubber Paddle", "Net 15.25cm high", "Game played to 11 points", "Table Tennis Match Specifications"),
    ("Badminton", "Badminton Shot Types", "Smash", "Drop Shot", "Clear / Lob", "Net Lift", "Essential Badminton Racket Shots"),
    ("Golf", "Golf Club Types", "Driver (Wood)", "Iron", "Wedge", "Putter", "Types of Clubs in a Golf Bag"),
    ("Boxing", "Boxing Punches", "Jab", "Cross", "Hook", "Uppercut", "The 4 Fundamental Boxing Punches"),
    ("Baseball", "Position Players", "Pitcher", "Catcher", "Shortstop", "Outfielder", "Key Field Defensive Roles in Baseball"),
    ("Volleyball", "Volleyball Court Boundaries", "Service Line", "Attack Line (3m)", "Center Line", "Sideline", "Key Court Markings in Volleyball"),
    ("Archery", "Archery Target Rings", "Gold / Yellow (10 & 9)", "Red (8 & 7)", "Blue (6 & 5)", "Black & White (4, 3, 2, 1)", "Target Scoring Zones in Target Archery"),
    ("Kabaddi", "Kabaddi Terms", "Raid", "Tackle", "Super Raid (3+ pts)", "Bonus Line", "Essential Match Terms in Kabaddi"),
    ("Hockey", "Field Hockey Equipment", "Curved Stick", "Hard Ball", "Shin Guards", "Goalkeeper Helmet & Pads", "Field Hockey Playing Gear"),
    ("Rugby", "Rugby Scoring Methods", "Try (5 pts)", "Conversion (2 pts)", "Penalty Kick (3 pts)", "Drop Goal (3 pts)", "Ways to Score Points in Rugby Union"),
    ("Football", "World Cup Trophy", "Made of 18-karat gold", "Depicts two figures holding Earth", "Designed by Silvio Gazzaniga", "Awarded every 4 years", "FIFA World Cup Trophy Features"),
    ("Cricket", "Format Matches", "Test Match (5 days)", "One Day International (50 overs)", "T20 (20 overs)", "T10 / 100-ball", "Official International Cricket Formats"),
    ("Basketball", "Scoring Zones", "Free Throw Line (1 pt)", "Inside the Arc (2 pts)", "Beyond the Arc (3 pts)", "Half-court Buzzer Beater", "Scoring Values in Basketball"),
    ("Tennis", "Grand Slam Legends (Men)", "Novak Djokovic (24)", "Rafael Nadal (22)", "Roger Federer (20)", "Pete Sampras (14)", "All-Time Men's Singles Grand Slam Leaders"),
    ("Tennis", "Grand Slam Legends (Women)", "Margaret Court (24)", "Serena Williams (23)", "Steffi Graf (22)", "Martina Navratilova (18)", "All-Time Women's Singles Grand Slam Leaders"),
    ("F1", "Flag Signals", "Chequered Flag (Finish)", "Yellow Flag (Danger / Caution)", "Red Flag (Session Stopped)", "Green Flag (Track Clear)", "Formula 1 Racing Flag System"),
    ("Dodgeball", "Player Roles", "Catchers", "Throwers / Snipers", "Corner Guards", "Retrieve Assistants", "Tactical Player Specializations in Dodgeball"),
    ("Kho Kho", "Kho Kho Match Officials", "Referees (2)", "Umpire (1)", "Timekeeper (1)", "Scorer (1)", "Official Refereeing Panel in Kho Kho"),
    ("Olympics", "Ancient Olympic Games", "Olympia, Greece", "776 BC origin", "Olive Wreath Crown", "Dedicated to Zeus", "Origins of the Ancient Olympic Games"),
    ("Athletics", "Decathlon Disciplines Sample", "100m & Long Jump", "Shot Put & High Jump", "Discus & Pole Vault", "Javelin & 1500m", "Events in Men's Athletics Decathlon"),
    ("Swimming", "Medley Relay Order", "Backstroke (1st)", "Breaststroke (2nd)", "Butterfly (3rd)", "Freestyle (4th)", "Official Stroke Order in Medley Swimming Relays"),
    ("Cricket", "IPL Franchises", "Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders", "Royal Challengers Bengaluru", "Prominent Indian Premier League (IPL) Teams"),
    ("Football", "UEFA Champions League Winners", "Real Madrid", "AC Milan", "Bayern Munich", "Liverpool", "Clubs with Most UEFA Champions League Titles"),
    ("Basketball", "Dream Team 1992", "Michael Jordan", "Magic Johnson", "Larry Bird", "Charles Barkley", "Members of the 1992 USA Olympic 'Dream Team'"),
    ("Dodgeball", "Elimination Triggers", "Direct ball impact on body", "Stepping out of bounds", "Opponent catches thrown ball", "Throwing a dead ball", "Ways a Dodgeball Player is Eliminated"),
    ("Kho Kho", "Court Dimensions", "Length 27 meters", "Width 16 meters", "Central Lane width 30cm", "Pole distance 24 meters", "Official Senior Kho Kho Court Specifications"),
    ("Golf", "Par Terms", "Birdie (1 under par)", "Eagle (2 under par)", "Albatross (3 under par)", "Bogey (1 over par)", "Golf Score Terms Relative to Par"),
    ("Boxing", "Boxing Ring Dimensions", "Square shape", "4 padded ropes", "Canvas mat over padding", "Corners: Red, Blue, Neutral", "Features of a Professional Boxing Ring"),
    ("Volleyball", "Libero Role", "Special colored jersey", "Defensive specialist only", "Cannot serve or block", "Unlimited substitutions", "Characteristics of a Volleyball Libero"),
    ("Marathon", "Marathon Distance", "42.195 kilometers", "26 miles 385 yards", "Historical Windsor Castle to White City route", "Olympic grand finale event", "Official Marathon Distance Measurements"),
    ("Motorsport", "Indy 500 & Le Mans", "Indianapolis 500", "24 Hours of Le Mans", "Monaco Grand Prix", "Triple Crown of Motorsport", "The Triple Crown of Motorsport Events")
]

for idx, t in enumerate(easy_topics, start=21):
    easy_questions.append({
        "id": f"E{idx:02d}",
        "difficulty": "easy",
        "type": "connection",
        "sport": t[0],
        "title": t[1],
        "clues": [f"Clue 1: {t[2]}", f"Clue 2: {t[3]}", f"Clue 3: {t[4]}", f"Clue 4: {t[5]}"],
        "answer": t[6],
        "explanation": f"All four clues directly connect to {t[6]}."
    })

print(f"Total Easy Questions: {len(easy_questions)}")

import json
import os

# Build the 180 questions database in Python

def get_easy_questions():
    eq = [
        {"id":"E01","difficulty":"easy","type":"connection","sport":"Football","title":"Global Football Legends","clues":["Clue 1: Lionel Messi","Clue 2: Cristiano Ronaldo","Clue 3: Pelé","Clue 4: Diego Maradona"],"answer":"Football GOATs / Ballon d'Or & World Cup Icons","explanation":"All four are widely celebrated as the greatest football players of all time."},
        {"id":"E02","difficulty":"easy","type":"connection","sport":"Tennis","title":"Grand Slam Tournaments","clues":["Clue 1: Wimbledon (London)","Clue 2: Roland Garros (Paris)","Clue 3: US Open (New York)","Clue 4: Australian Open (Melbourne)"],"answer":"The Four Tennis Grand Slam Tournaments","explanation":"These comprise the four major annual tennis tournaments in the world."},
        {"id":"E03","difficulty":"easy","type":"connection","sport":"Cricket","title":"Cricket World Champions","clues":["Clue 1: Australia (6 titles)","Clue 2: India (2 titles)","Clue 3: West Indies (2 titles)","Clue 4: England (1 title)"],"answer":"Men's ODI Cricket World Cup Champions","explanation":"All these nations have won the ICC Men's 50-over Cricket World Cup."},
        {"id":"E04","difficulty":"easy","type":"connection","sport":"Dodgeball","title":"Dodgeball Basics","clues":["Clue 1: Opening Rush at center line","Clue 2: Foam or Rubber balls","Clue 3: Catching a ball revives a teammate","Clue 4: Getting hit means you are OUT"],"answer":"Core Rules of Dodgeball","explanation":"These represent the fundamental rules and phase progression of a dodgeball match."},
        {"id":"E05","difficulty":"easy","type":"connection","sport":"Kho Kho","title":"Kho Kho Fundamentals","clues":["Clue 1: 8 Seated Chasers facing opposite directions","Clue 2: 1 Active Chaser pursuing defenders","Clue 3: Tapping a teammate's back and shouting 'KHO!'","Clue 4: Two wooden poles at court ends"],"answer":"Essential Rules of Kho Kho","explanation":"Describes the seated chasers, active chaser call, and field layout of traditional Kho Kho."},
        {"id":"E06","difficulty":"easy","type":"connection","sport":"Basketball","title":"Basketball Court Positions","clues":["Clue 1: Point Guard","Clue 2: Shooting Guard","Clue 3: Small Forward","Clue 4: Power Forward & Center"],"answer":"The 5 Standard Positions in Basketball","explanation":"These are the traditional five player positions on a basketball team."},
        {"id":"E07","difficulty":"easy","type":"connection","sport":"Olympics","title":"Olympic Symbol","clues":["Clue 1: Blue and Yellow","Clue 2: Black and Green","Clue 3: Red","Clue 4: White background"],"answer":"Colors of the 5 Olympic Rings & Flag","explanation":"The Olympic rings feature five colors (blue, yellow, black, green, red) representing the five inhabited continents."},
        {"id":"E08","difficulty":"easy","type":"connection","sport":"Formula 1","title":"F1 Champions","clues":["Clue 1: Lewis Hamilton","Clue 2: Michael Schumacher","Clue 3: Max Verstappen","Clue 4: Ayrton Senna"],"answer":"Multiple-time Formula 1 World Drivers' Champions","explanation":"Each of these drivers has won multiple F1 Drivers' World Championships."},
        {"id":"E09","difficulty":"easy","type":"connection","sport":"Athletics","title":"Sprint Events","clues":["Clue 1: 100 meters","Clue 2: 200 meters","Clue 3: 400 meters","Clue 4: 4x100m Relay"],"answer":"Track Sprint Events in Athletics","explanation":"These are the primary short-distance sprint categories in athletics."},
        {"id":"E10","difficulty":"easy","type":"connection","sport":"Badminton","title":"Badminton Gear & Play","clues":["Clue 1: Goose feather or nylon projectile","Clue 2: Light racket with tight strings","Clue 3: 5ft (1.55m) high net","Clue 4: Played to 21 points per game"],"answer":"Badminton Equipment & Scoring System","explanation":"Describes the shuttlecock, racket, net height, and 21-point rally scoring system."}
    ]

    easy_extra = [
        ("Golf", "Golf Majors", "Green Jacket at Augusta", "Wanamaker Trophy at PGA Championship", "US Open Trophy", "Claret Jug at The Open", "Trophies of Men's Golf 4 Major Championships"),
        ("Swimming", "Swimming Strokes", "Freestyle (Front Crawl)", "Backstroke", "Breaststroke", "Butterfly", "The Four Competitive Swimming Strokes"),
        ("Boxing", "Boxing Legends", "Muhammad Ali", "Mike Tyson", "Manny Pacquiao", "Floyd Mayweather Jr.", "Undefeated or World Champion Boxing Icons"),
        ("Baseball", "Diamond Bases", "Home Plate", "First Base", "Second Base", "Third Base", "Bases on a Baseball Infield Diamond"),
        ("Volleyball", "Volleyball Touches", "Bump (Pass)", "Set", "Spike (Attack)", "Maximum 3 hits per side", "Standard 3-Hit Play Sequence in Volleyball"),
        ("Dodgeball", "Dodgeball Court Zones", "Center Line", "Attack Line (3-meter mark)", "Back Line", "Out-of-Bounds Queue", "Markings & Boundary Zones on a Dodgeball Court"),
        ("Kho Kho", "Kho Kho Turns", "3 Defenders enter in batches", "Chaser must give KHO from behind", "Pole turn around to change direction", "Innings last 9 minutes", "Rules Governing Chasing and Defending in Kho Kho"),
        ("Cricket", "Ways Out in Cricket", "Bowled (stumps hit)", "Caught by fielder", "LBW (Leg Before Wicket)", "Run Out", "Most Common Modes of Dismissal in Cricket"),
        ("Tennis", "Tennis Game Point Progression", "Love (0)", "15", "30", "40", "Tennis Point Scoring Order within a Single Game"),
        ("Football", "Football Officials", "Main Referee on pitch", "Two Assistant Referees", "Fourth Official", "VAR (Video Assistant Referee)", "Match Official Roles in Professional Football"),
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
        ("Basketball", "Scoring Values", "Free Throw Line (1 pt)", "Inside the Arc (2 pts)", "Beyond the Arc (3 pts)", "Half-court Shot", "Point Values in Basketball"),
        ("Tennis", "Grand Slam Champions (Men)", "Novak Djokovic", "Rafael Nadal", "Roger Federer", "Pete Sampras", "All-Time Men's Singles Grand Slam Leaders"),
        ("Tennis", "Grand Slam Champions (Women)", "Margaret Court", "Serena Williams", "Steffi Graf", "Martina Navratilova", "All-Time Women's Singles Grand Slam Leaders"),
        ("F1", "Flag Signals", "Chequered Flag (Finish)", "Yellow Flag (Caution)", "Red Flag (Session Stopped)", "Green Flag (Track Clear)", "Formula 1 Racing Flag System"),
        ("Dodgeball", "Player Roles", "Catchers", "Throwers / Snipers", "Corner Guards", "Retrieve Assistants", "Tactical Player Specializations in Dodgeball"),
        ("Kho Kho", "Kho Kho Match Officials", "Referees (2)", "Umpire (1)", "Timekeeper (1)", "Scorer (1)", "Official Refereeing Panel in Kho Kho"),
        ("Olympics", "Ancient Olympic Games", "Olympia, Greece", "776 BC origin", "Olive Wreath Crown", "Dedicated to Zeus", "Origins of the Ancient Olympic Games"),
        ("Athletics", "Decathlon Sample Events", "100m & Long Jump", "Shot Put & High Jump", "Discus & Pole Vault", "Javelin & 1500m", "Events in Men's Athletics Decathlon"),
        ("Swimming", "Medley Relay Order", "Backstroke (1st)", "Breaststroke (2nd)", "Butterfly (3rd)", "Freestyle (4th)", "Official Stroke Order in Medley Swimming Relays"),
        ("Cricket", "IPL Franchises", "Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders", "Royal Challengers Bengaluru", "Prominent Indian Premier League (IPL) Teams"),
        ("Football", "UEFA Champions League Winners", "Real Madrid", "AC Milan", "Bayern Munich", "Liverpool", "Clubs with Most UEFA Champions League Titles"),
        ("Basketball", "Dream Team 1992", "Michael Jordan", "Magic Johnson", "Larry Bird", "Charles Barkley", "Members of the 1992 USA Olympic 'Dream Team'"),
        ("Dodgeball", "Elimination Triggers", "Direct ball impact on body", "Stepping out of bounds", "Opponent catches thrown ball", "Throwing a dead ball", "Ways a Dodgeball Player is Eliminated"),
        ("Kho Kho", "Court Dimensions", "Length 27 meters", "Width 16 meters", "Central Lane width 30cm", "Pole distance 24 meters", "Official Senior Kho Kho Court Specifications"),
        ("Golf", "Par Score Terms", "Birdie (1 under par)", "Eagle (2 under par)", "Albatross (3 under par)", "Bogey (1 over par)", "Golf Score Terms Relative to Par"),
        ("Boxing", "Boxing Ring Details", "Square shape", "4 padded ropes", "Canvas mat over padding", "Corners: Red, Blue, Neutral", "Features of a Professional Boxing Ring"),
        ("Volleyball", "Libero Role", "Special colored jersey", "Defensive specialist only", "Cannot serve or block", "Unlimited substitutions", "Characteristics of a Volleyball Libero"),
        ("Marathon", "Marathon Distance", "42.195 kilometers", "26 miles 385 yards", "Historical Windsor Castle route", "Olympic grand finale event", "Official Marathon Distance Measurements"),
        ("Motorsport", "Indy 500 & Le Mans", "Indianapolis 500", "24 Hours of Le Mans", "Monaco Grand Prix", "Triple Crown of Motorsport", "The Triple Crown of Motorsport Events")
    ]

    for idx, (sp, tt, c1, c2, c3, c4, ans) in enumerate(easy_extra, start=11):
        eq.append({
            "id": f"E{idx:02d}",
            "difficulty": "easy",
            "type": "connection",
            "sport": sp,
            "title": tt,
            "clues": [f"Clue 1: {c1}", f"Clue 2: {c2}", f"Clue 3: {c3}", f"Clue 4: {c4}"],
            "answer": ans,
            "explanation": f"All four clues directly connect to {ans}."
        })
    return eq

def get_medium_questions():
    mq = []
    med_list = [
        ("Football", "Stadiums Named After Legends", "Santiago Bernabéu (Madrid)", "Johan Cruyff Arena (Amsterdam)", "Ferenc Puskás Arena (Budapest)", "Maracanã / Estádio Mário Filho (Rio)", "Famous Football Stadiums Named After Legendary Players or Officials"),
        ("Multi-Sport", "Multi-Sport Professional Athletes", "Bo Jackson (NFL & MLB All-Star)", "Deion Sanders (Played Super Bowl & World Series)", "Michael Jordan (NBA & Minor League Baseball)", "Jim Thorpe (Olympic Gold, NFL, MLB)", "Famous Athletes Who Competed Professionally in Multiple Major Sports"),
        ("Tennis", "Golden Slam Winners", "Steffi Graf (1988)", "Rafael Nadal (2010)", "Serena Williams (2012)", "Novak Djokovic (2024)", "Tennis Players Who Completed the Career Golden Slam (All 4 Slams + Olympic Gold)"),
        ("Cricket", "500+ Test Wickets Club", "Muttiah Muralitharan (800)", "Shane Warne (708)", "James Anderson (704)", "Anil Kumble (619)", "Bowlers Who Have Taken Over 600 Test Wickets in Men's International Cricket"),
        ("Football", "Unbeaten Domestic League Champions", "Arsenal (2003-04 Invincibles)", "Juventus (2011-12 Serie A)", "Bayer Leverkusen (2023-24 Bundesliga)", "Celtic (2016-17 Scottish Premiership)", "European Football Clubs That Completed an Entire Unbeaten Domestic League Season"),
        ("Kho Kho", "Specialized Kho Kho Techniques", "Sky Dive (Aerial touch over defender)", "Pole Dive (Low sweeping touch around wooden pole)", "Single Chain (Zig-zag defensive running)", "Ring Game (Circular dodging pattern)", "Advanced Tactical Moves and Defensive Patterns in Kho Kho"),
        ("Dodgeball", "Dodgeball Special Rules", "Burden of Throw (Team with majority balls must throw in 5s)", "Sudden Death 1v1 (Last player on each side)", "Headshot Warning (Targeting head intentionally disqualified)", "Neutral Zone (3-meter center zone open to both teams)", "Special Tournament Rules in World Dodgeball Federation (WDBF)"),
        ("Olympics", "Multi-Discipline Olympic Gold Medalists", "Ester Ledecká (Gold in Snowboarding & Alpine Skiing)", "Carl Lewis (Gold in 100m, 200m, 4x100m & Long Jump)", "Johnny Weissmuller (Gold in Swimming & Water Polo Medal)", "Eddie Eagan (Gold in Summer Boxing & Winter Bobsleigh)", "Athletes Who Won Olympic Gold Medals Across Distinct Sports or Disciplines"),
        ("F1", "Legendary F1 Track Corners", "Eau Rouge & Raidillon (Spa-Francorchamps)", "Grand Hotel Hairpin (Monaco)", "Parabolica / Curva Alboreto (Monza)", "Maggotts & Becketts (Silverstone)", "Most Famous Corners in Formula 1 Grand Prix Circuits"),
        ("Basketball", "NBA All-Time Triple-Double Leaders", "Russell Westbrook", "Oscar Robertson", "Magic Johnson", "Nikola Jokić", "NBA Players with the Most Career Triple-Doubles"),
        ("Dodgeball", "Dodgeball Ball Material Specifications", "7-inch Foam Ball", "Cloth Ball (Rubber interior)", "Rubber Dodgeball (Classic playground)", "Mesh Air-Core Ball", "Official Dodgeball Ball Specifications Across International Leagues"),
        ("Kho Kho", "Kho Kho Field Specifications", "Field Length: 27 meters", "Field Width: 16 meters", "Central Lane Width: 30 centimeters", "Pole Height: 1.20 to 1.25 meters above ground", "Official Dimensions of a Senior Kho Kho Playing Court"),
        ("Cricket", "World Cup Hat-trick Bowlers", "Chetan Sharma (1987)", "Saqlain Mushtaq (1999)", "Chaminda Vaas (2003)", "Brett Lee (2003)", "Bowlers Who Have Taken a Hat-Trick in ICC Men's ODI World Cup History"),
        ("Football", "Continental Treble Winning Clubs", "Celtic (1967)", "Ajax (1972)", "Manchester United (1999)", "Barcelona (2009 & 2015)", "European Clubs That Won League, Domestic Cup & Champions League in a Single Season"),
        ("Athletics", "Sub-9.60s or Historic 100m Runners", "Usain Bolt (9.58s)", "Tyson Gay (9.69s)", "Yohan Blake (9.69s)", "Asafa Powell (9.72s)", "The Fastest 100m Sprinters in Human History"),
        ("Tennis", "Grand Slam Won Without Dropping a Set", "Björn Borg (1978 & 1980 French Open)", "Rafael Nadal (4x French Open)", "Roger Federer (2007 Australian, 2017 Wimbledon)", "Iga Świątek (2020 French Open)", "Tennis Champions Who Won a Grand Slam Title Without Dropping a Single Set"),
        ("F1", "F1 Drivers Winning Titles for Multiple Constructors", "Juan Manuel Fangio (Alfa Romeo, Maserati, Mercedes, Ferrari)", "Niki Lauda (Ferrari & McLaren)", "Graham Hill (BRM & Lotus)", "Emerson Fittipaldi (Lotus & McLaren)", "Drivers Who Won Formula 1 World Championships with Different Teams"),
        ("Badminton", "All England Open Men's Singles Legends", "Rudy Hartono (8 titles)", "Lin Dan (6 titles)", "Lee Chong Wei (4 titles)", "Viktor Axelsen (2+ titles)", "Dominant Men's Singles Champions of the Historic All England Open Badminton Championship"),
        ("Golf", "Career Grand Slam Golfers", "Gene Sarazen", "Ben Hogan", "Gary Player", "Jack Nicklaus & Tiger Woods", "Golfers Who Won All 4 Modern Major Championships in Their Career"),
        ("Boxing", "Heavyweight Champions of the World", "Muhammad Ali", "Joe Frazier", "George Foreman", "Mike Tyson", "Iconic Undisputed World Heavyweight Boxing Champions"),
        ("Kho Kho", "Kho Kho Foul Infringements", "Chaser changing direction after starting stride", "Seated player standing before receiving KHO", "Active chaser touching central line", "Defender entering court out of batch sequence", "Official Match Fouls and Penalties in Kho Kho"),
        ("Dodgeball", "Catching Mechanics & Rules", "Fielder catches thrown ball cleanly", "Thrower eliminated immediately", "First eliminated teammate re-enters match", "Bobbled catch secured before touching ground is valid", "Comprehensive Rules & Effects of a Successful Catch in Dodgeball"),
        ("Basketball", "NBA Players with 60+ Points in a Single Game", "Wilt Chamberlain (100 pts)", "Kobe Bryant (81 pts)", "David Thompson (73 pts)", "Damian Lillard & Luka Dončić (71 pts)", "NBA Players Who Have Scored 70 or More Points in a Single Game"),
        ("Cricket", "300+ Test Score Batter Club", "Don Bradman (334 & 304)", "Virender Sehwag (309 & 319)", "Brian Lara (375 & 400*)", "Chris Gayle (317 & 333)", "Batters Who Have Scored Multiple Triple-Centuries in Men's Test Cricket"),
        ("Football", "Ballon d'Or Multi-Winners", "Lionel Messi (8)", "Cristiano Ronaldo (5)", "Michel Platini (3)", "Johan Cruyff & Marco van Basten (3)", "Footballers Who Have Won 3 or More Ballon d'Or Trophies"),
        ("Swimming", "Olympic 8+ Gold Medalists", "Michael Phelps (23 Gold)", "Larisa Latynina (9 Gold)", "Paavo Nurmi (9 Gold)", "Mark Spitz & Carl Lewis (9 Gold)", "The Most Decorated Olympic Gold Medalists of All Time"),
        ("Volleyball", "Volleyball Technical Rules", "Rotation in clockwise direction", "Net touch by player during action is a fault", "Server must hit ball within 8 seconds of whistle", "Ball hitting antenna is out of bounds", "Key Technical Rules Governing Professional Volleyball Matches"),
        ("Table Tennis", "Table Tennis Grand Slam Winners (Olympic, World, World Cup)", "Jan-Ove Waldner (Sweden)", "Liu Guoliang (China)", "Kong Linghui (China)", "Ma Long (2x Grand Slam Winner)", "Table Tennis Players Who Achieved the World Grand Slam"),
        ("Archery", "Olympic Archery Champions", "Kim Woo-jin", "An San", "Park Sung-hyun", "Viktor Ruban", "Dominant Olympic Gold Medalists in Recurve Archery"),
        ("Kabaddi", "Pro Kabaddi League (PKL) Legends", "Pardeep Narwal ('Dubki King')", "Rahul Chaudhari", "Maninder Singh", "Pawan Sehrawat", "All-Time Top Raid Point Scorers in Pro Kabaddi League"),
        ("Hockey", "Olympic Men's Field Hockey Dominance", "India (8 Gold Medals)", "Germany (4 Gold Medals)", "Netherlands (3 Gold Medals)", "Australia (1 Gold & 10 Medals)", "The Most Successful National Teams in Men's Olympic Field Hockey"),
        ("Rugby", "Rugby World Cup Champions", "South Africa (Springboks - 4 titles)", "New Zealand (All Blacks - 3 titles)", "Australia (Wallabies - 2 titles)", "England (1 title)", "Nations That Have Won the Men's Rugby World Cup"),
        ("Motorsport", "Le Mans 24 Hours Winners", "Porsche (19 victories)", "Audi (13 victories)", "Ferrari (11 victories)", "Jaguar (7 victories)", "Most Successful Automobile Manufacturers in 24 Hours of Le Mans History"),
        ("Baseball", "World Series Most Titles", "New York Yankees (27 titles)", "St. Louis Cardinals (11 titles)", "Oakland Athletics (9 titles)", "Boston Red Sox (9 titles)", "Major League Baseball (MLB) Franchises with the Most World Series Titles"),
        ("Football", "FIFA World Cup Golden Boot Winners", "Ronaldo Nazário (2002 - 8 goals)", "James Rodríguez (2014 - 6 goals)", "Harry Kane (2018 - 6 goals)", "Kylian Mbappé (2022 - 8 goals)", "Top Goalscorers Awarded the FIFA World Cup Golden Boot in 21st Century"),
        ("Cricket", "Fastest ODI Centuries", "AB de Villiers (31 balls)", "Corey Anderson (36 balls)", "Shahid Afridi (37 balls)", "Glenn Maxwell (40 balls)", "Batters Who Scored the Fastest Centuries in ODI Cricket History"),
        ("Tennis", "Wimbledon Men's Singles 5+ Titles", "Roger Federer (8 titles)", "Pete Sampras (7 titles)", "Novak Djokovic (7 titles)", "Björn Borg (5 titles)", "Men's Tennis Champions Who Won 5 or More Wimbledon Singles Titles"),
        ("Basketball", "NBA Finals MVP Multi-Winners", "Michael Jordan (6 times)", "LeBron James (4 times)", "Magic Johnson (3 times)", "Shaquille O'Neal & Tim Duncan (3 times)", "Players Who Won the NBA Finals Most Valuable Player Award 3 or More Times"),
        ("Kho Kho", "Kho Kho Innings Structure", "Match consists of 2 turns/innings", "Each turn has 9 minutes chasing & 9 minutes defending", "5 minutes interval between turns", "Highest points scored across 4 turns wins", "Official Match Structure and Duration in Championship Kho Kho"),
        ("Dodgeball", "Dodgeball Equipment & Safety Setup", "Soft foam core to prevent injury", "Non-marking rubber court shoes", "Knee pads and protective grip gloves", "Surrounding safety barriers 2 meters off-court", "Standard Player Gear and Safety Specifications for Dodgeball Competitions"),
        ("F1", "F1 World Champions with 4+ Titles", "Lewis Hamilton (7)", "Michael Schumacher (7)", "Juan Manuel Fangio (5)", "Alain Prost & Sebastian Vettel (4)", "Drivers Who Won 4 or More Formula 1 World Drivers' Championships"),
        ("Athletics", "Sub-2 Hours Marathon Feat", "Eliud Kipchoge (1h 59m 40s - Vienna 2019)", "Nike Breaking2 Project", "Kenyan Long-Distance Legend", "Rotterdam & Berlin Marathon Winner", "Eliud Kipchoge's Historic Sub-2 Hour Marathon Challenge"),
        ("Cricket", "Bowlers with 10 Wickets in a Single Test Innings", "Jim Laker (10/53 - 1956)", "Anil Kumble (10/74 - 1999)", "Ajaz Patel (10/119 - 2021)", "3 Bowlers in 147 Years of Test History", "The Only Three Bowlers to Take All 10 Wickets in a Single Test Innings"),
        ("Football", "Clubs Winning UEFA Champions League Undefeated", "AC Milan (1988-89 & 1993-94)", "Ajax (1994-95)", "Manchester United (1998-99 & 2007-08)", "Bayern Munich (2019-20 - 11 wins in 11 games)", "Clubs That Won the European Cup / Champions League Without Losing a Single Match"),
        ("Olympics", "Olympic Games Hosted 3 Times by Same City", "London (1908, 1948, 2012)", "Paris (1900, 1924, 2024)", "Los Angeles (1932, 1984, scheduled 2028)", "Exclusive 3-Time Host Cities", "Global Cities That Have Been Selected to Host the Summer Olympics Three Times"),
        ("Tennis", "Career Grand Slam Champions (Women's)", "Maureen Connolly", "Doris Hart", "Shirley Fry Irvin", "Margaret Court, Chris Evert, Martina Navratilova, Steffi Graf, Serena Williams", "Women Tennis Players Who Completed a Career Grand Slam in Singles"),
        ("Badminton", "Thomas Cup Champions (Men's Team)", "Indonesia (14 titles)", "China (11 titles)", "Malaysia (5 titles)", "India (1 title in 2022)", "Nations That Have Won the World Men's Badminton Team Championship (Thomas Cup)"),
        ("Golf", "Lowest Single Round Score in Major Championship", "Branden Grace (62 at 2017 Open)", "Xander Schauffele (62 at 2023 US Open & 2024 PGA)", "Rickie Fowler (62 at 2023 US Open)", "Shane Lowry (62 at 2024 PGA)", "Golfers Who Shot a Historic Round of 62 in a Men's Major Golf Championship"),
        ("Boxing", "Undefeated World Champions Retiring Unbeaten", "Rocky Marciano (49-0)", "Floyd Mayweather Jr. (50-0)", "Joe Calzaghe (46-0)", "Sheng-Sheng / Ricardo López (51-0-1)", "World Champion Boxers Who Retired with an Undefeated Professional Record"),
        ("Kho Kho", "Kho Kho Free Zone Rules", "Area beyond the wooden pole line", "Chaser can move in any direction inside free zone", "Allows 180-degree turn around the pole", "Defenders can dodge using pole support", "Rules Governing Movement within the Free Zone in Kho Kho"),
        ("Dodgeball", "Dodgeball Opening Rush Protocol", "6 balls placed along center line", "Players start behind baseline", "Signal whistle triggers sprint to retrieve balls", "Balls must be checked behind attack line before throw", "Rules and Sequence of the Dodgeball Match Opening Rush"),
        ("Basketball", "NBA Teams with 70+ Regular Season Wins", "Chicago Bulls (72-10 in 1995-96)", "Golden State Warriors (73-9 in 2015-16)", "Coached by Phil Jackson & Steve Kerr", "Led by Michael Jordan & Steph Curry", "The Only Two Teams in NBA History to Win 70+ Games in a Regular Season"),
        ("Cricket", "300+ Runs Scored in a Single T20 International Team Innings", "Nepal (314/3 vs Mongolia 2023)", "India (297/6 vs Bangladesh 2024)", "Sunrisers Hyderabad (IPL 287/3 & 277/3)", "T20 Highest Team Total Records", "Highest Team Totals Recorded in Official T20 Cricket History"),
        ("Football", "Clean Sheet World Record Goalkeepers", "Mazarópi (1,816 consecutive minutes)", "Dynamo Kyiv's Viktor Tanev", "Atlético Madrid's Jan Oblak", "Edwin van der Sar (1,311 mins Premier League)", "Goalkeepers Known for Extreme Consecutive Clean Sheet Minutes Records"),
        ("Olympics", "Miracle on Ice (1980)", "Winter Olympics at Lake Placid", "USA Men's Ice Hockey Team", "Defeated 4-time defending champions Soviet Union", "Coached by Herb Brooks", "The Iconic 'Miracle on Ice' USA Olympic Hockey Victory"),
        ("Volleyball", "FIVB World Champions", "Brazil", "Italy", "Poland", "Soviet Union / Russia", "Most Successful Nations in FIVB Men's Volleyball World Championship History"),
        ("Field Hockey", "FIH Men's World Cup Champions", "Pakistan (4 titles)", "Netherlands (3 titles)", "Australia (3 titles)", "Germany (3 titles)", "Nations That Have Won the Men's Field Hockey World Cup"),
        ("Chess / Sport", "World Chess Champions", "Garry Kasparov", "Bobby Fischer", "Magnus Carlsen", "Viswanathan Anand", "Uncontested World Chess Champions"),
        ("Cycling", "Tour de France Jersey Categories", "Yellow Jersey (Maillot Jaune - Overall Leader)", "Green Jersey (Points / Sprinter)", "Polka Dot Jersey (King of the Mountains)", "White Jersey (Best Young Rider)", "Official Classification Jerseys of the Tour de France"),
        ("Martial Arts", "Judo Weight Categories & Belts", "White to Brown Belt (Kyu)", "Black Belt (Dan)", "Ippon (Instant victory)", "Waza-ari (Half point)", "Belts and Scoring Terms in Olympic Judo")
    ]

    for idx, (sp, tt, c1, c2, c3, c4, ans) in enumerate(med_list, start=1):
        mq.append({
            "id": f"M{idx:02d}",
            "difficulty": "medium",
            "type": "connection",
            "sport": sp,
            "title": tt,
            "clues": [f"Clue 1: {c1}", f"Clue 2: {c2}", f"Clue 3: {c3}", f"Clue 4: {c4}"],
            "answer": ans,
            "explanation": f"All four clues directly connect to {ans}."
        })
    return mq

def get_hard_questions():
    hq = []
    hard_list = [
        ("Football", "Scored in Champions League Final for Two Different Clubs", "Cristiano Ronaldo (Man Utd 2008 & Real Madrid 2014, 2017)", "Mario Mandžukić (Bayern Munich 2013 & Juventus 2017)", "Velibor Vasović (Partizan 1966 & Ajax 1969)", "Exclusive UCL Final Goalscoring Club", "Players Who Have Scored in a UEFA Champions League / European Cup Final for Two Different Clubs"),
        ("Olympics", "Cities That Hosted Both Summer & Winter Olympics", "Beijing, China (Summer 2008 & Winter 2022)", "Only city in history to host both official Games", "Bird's Nest & Ice Cube Stadiums utilized in both", "Historic Olympic Hosting Landmark", "Beijing - The First & Only City to Host Both Summer and Winter Olympic Games"),
        ("Multi-Sport", "Defensive Direct Point Scoring Without Ball Possession", "Kho Kho: Touching defender or pole touch", "Kabaddi: Super Tackle (2 defender tackle points)", "Volleyball: Direct Block Point (Stuff block)", "Dodgeball: Catching opponent's throw eliminates thrower & awards point/player return", "Sports Rules Where Defenders Score Points Directly Without First Taking Offensive Control"),
        ("Athletics", "Unbroken World Records Held for Over 30 Years", "Mike Powell (Long Jump 8.95m - 1991)", "Javier Sotomayor (High Jump 2.45m - 1993)", "Jürgen Schult (Discus Throw 74.08m - 1986)", "Galina Chistyakova (Women's Long Jump 7.52m - 1988)", "Athletics Field World Records That Have Remained Unbroken for Over 30 Years"),
        ("Kho Kho", "Kho Kho Defender Batch 3 Rotation Rule", "Defenders enter court in batches of 3 players", "When all 3 defenders are out, next batch enters BEFORE next KHO", "Late entry penalty awards 1 point to chasers", "7 minutes maximum defense run", "Rules Governing Batch Rotation and Entry Penalties for Defenders in Kho Kho"),
        ("Dodgeball", "WDBF International Neutral Zone & Headshot Protocol", "3-meter center zone open to both teams after opening rush", "Player stepping past neutral zone line is out", "High throw above shoulder with intentional head contact causes warnings", "Two headshots result in match ejection", "Official WDBF Rules on Neutral Zone Traversal and Headshot Warnings"),
        ("Cricket", "1000+ Runs and 100+ Wickets in ODI Cricket History", "Sanath Jayasuriya (13,430 runs & 323 wickets)", "Shahid Afridi (8,064 runs & 395 wickets)", "Jacques Kallis (11,579 runs & 273 wickets)", "Shakib Al Hasan (7,500+ runs & 300+ wickets)", "Elite All-Rounders Who Achieved 7,000+ Runs and 250+ Wickets in Men's ODI Cricket"),
        ("Football", "Managers Winning UCL with 2+ Different Clubs", "Carlo Ancelotti (AC Milan & Real Madrid)", "Ernst Happel (Feyenoord & Hamburger SV)", "Ottmar Hitzfeld (Borussia Dortmund & Bayern Munich)", "José Mourinho (Porto & Inter Milan) & Pep Guardiola (Barcelona & Man City)", "Football Managers Who Won the UEFA Champions League with Multiple Clubs"),
        ("F1", "F1 World Champions Without Winning Most Races in Season", "Nelson Piquet (1983 - Won 3 races vs Alain Prost 4 wins)", "Keke Rosberg (1982 - Won only 1 race in entire season)", "Mike Hawthorn (1958 - Won 1 race vs Stirling Moss 4 wins)", "Consistency Over Race Victories", "Drivers Who Won the Formula 1 World Championship Without Winning the Most Races That Year"),
        ("Tennis", "Winning All 3 Grand Slam Court Surfaces in a Single Calendar Year", "Rafael Nadal (2010 - French, Wimbledon, US Open)", "Novak Djokovic (2021 & 2023 - Australian, French, US/Wimbledon)", "Mats Wilander (1988 - Australian hard, French clay, US hard)", "Surface Slam Champions", "Tennis Players Who Won Grand Slam Titles on Grass, Clay, and Hard Courts in a Single Year"),
        ("Cricket", "Test Players Scoring 300+ and Taking 5 Wickets in Same Career", "Sir Garfield Sobers (365* & 6/73 best bowling)", "Virender Sehwag (319 & 5/104 best bowling)", "Chris Gayle (333 & 5/34 best bowling)", "Graham Gooch & Bob Cowper", "Batters Who Scored a Test Triple-Century AND Took a 5-Wicket Haul in Their Test Career"),
        ("Dodgeball", "Trapping vs Shading Rule Infringements", "Trapping: Catching ball that hit ground first is NOT an elimination", "Shading: Using held ball to block incoming throw", "If blocked ball drops from hand, blocker is OUT", "If blocked ball is caught by teammate, thrower is OUT", "Detailed Rules Differentiating Trapping, Blocking (Shading), and Deflections in Dodgeball"),
        ("Kho Kho", "Kho Kho Direction Change & Cross Lane Restrictions", "Active Chaser must keep direction chosen at first step", "Crossing the central lane is a foul unless at free zone", "Turning shoulder back beyond 90 degrees triggers direction foul", "Foul requires chaser to retreat and give KHO", "Strict Movement Rules for Active Chaser Regarding Direction and Central Lane"),
        ("Basketball", "50+ Point Games in NBA Finals History", "Elgin Baylor (61 points - 1962)", "Michael Jordan (55 points - 1993)", "Rick Barry (55 points - 1967)", "Giannis Antetokounmpo (50 points - 2021) & LeBron James (51 points - 2018)", "Players Who Have Scored 50 or More Points in a Single NBA Finals Game"),
        ("Swimming", "8 Gold Medals in a Single Olympic Games", "Michael Phelps (Beijing 2008)", "Broke Mark Spitz's 1972 record of 7 Gold Medals", "Set 7 World Records & 1 Olympic Record in 8 events", "100m Butterfly won by 0.01 seconds vs Milorad Čavić", "Michael Phelps' Historic 8 Gold Medal Performance at the 2008 Beijing Olympics"),
        ("Football", "Clubs Reaching 100+ Points in a Single European League Season", "Real Madrid (100 pts - 2011-12 La Liga)", "Barcelona (100 pts - 2012-13 La Liga)", "Juventus (102 pts - 2013-14 Serie A)", "Manchester City (100 pts - 2017-18 Premier League Centurions)", "European Football Clubs That Reached or Exceeded 100 Points in a Single Domestic League Season"),
        ("Cricket", "Fastest Test Century by Balls Faced", "Brendon McCullum (54 balls vs Australia 2016)", "Vivian Richards (56 balls vs England 1986)", "Misbah-ul-Haq (56 balls vs Australia 2014)", "Adam Gilchrist (57 balls vs England 2006)", "Batters Who Scored the Fastest Centuries in Test Cricket History"),
        ("F1", "F1 Drivers Winning World Title with Lowest Points Margin", "Niki Lauda (1984 - Beat Alain Prost by 0.5 points)", "Ayrton Senna (1988 - Beat Alain Prost by 3 points under best-11 scoring)", "Lewis Hamilton (2008 - Beat Felipe Massa by 1 point on final corner)", "Sebastian Vettel (2010 - Won by 4 points over Fernando Alonso)", "The Closest Formula 1 World Championship Season Finish Margins"),
        ("Tennis", "Golden Career Slam Singles & Doubles (Super Slam)", "Mike Bryan & Bob Bryan (Doubles Super Slam)", "Todd Woodbridge & Mark Woodforde (Woodies)", "Serena Williams & Venus Williams", "Pam Shriver & Gigi Fernández", "Tennis Players Who Won All 4 Grand Slams, Olympic Gold, & Year-End Finals in Doubles or Singles"),
        ("Olympics", "Athletes Winning Individual Gold in 4 Consecutive Olympics", "Al Oerter (Discus Throw: 1956, 1960, 1964, 1968)", "Carl Lewis (Long Jump: 1984, 1988, 1992, 1996)", "Michael Phelps (200m Individual Medley: 2004, 2008, 2012, 2016)", "Mijaín López (Greco-Roman Wrestling: 5 consecutive 2008-2024)", "Athletes Who Won Gold Medals in the Same Individual Event across 4+ Consecutive Olympic Games"),
        ("Kho Kho", "Kho Kho Pole Dive Scoring & Execution", "Chaser leaves ground completely before wooden pole line", "Grips pole with one arm while extending body in mid-air", "Touches defender's foot/body before touching ground", "Valid touch awards 1 point; premature ground touch is a foul", "Biomechanical Rules and Execution Standards of a Legal Pole Dive in Kho Kho"),
        ("Dodgeball", "Dodgeball Dead Ball State Scenarios", "Ball touches floor, wall, or ceiling", "Ball hits referee or non-active equipment", "Ball thrown before 5-second activation countdown", "Ball crossed attack line illegally during opening rush", "Official Scenarios That Convert a Live Dodgeball into a Dead Ball"),
        ("Cricket", "Only Bowler to Take 500+ Test Wickets & Average Under 21", "Malcolm Marshall (376 wkts @ 20.94)", "Joel Garner (259 wkts @ 20.98)", "Curtly Ambrose (405 wkts @ 20.99)", "Glenn McGrath (563 wkts @ 21.64)", "Legendary West Indies & Australian Fast Bowlers with Career Bowling Averages Under 22"),
        ("Football", "Most Goals Scored in a Single Calendar Year", "Lionel Messi (91 goals in 2012)", "Gerd Müller (85 goals in 1972)", "Pelé (75 goals in 1958)", "Cristiano Ronaldo (69 goals in 2013)", "All-Time Highest Goalscoring Feats in a Single Calendar Year"),
        ("Basketball", "Quadruple-Double Club in NBA History", "Nate Thurmond (1974 - 22 pts, 14 reb, 13 ast, 12 blk)", "Alvin Robertson (1986 - 20 pts, 11 reb, 10 ast, 10 stl)", "Hakeem Olajuwon (1990 - 18 pts, 16 reb, 10 ast, 11 blk)", "David Robinson (1994 - 34 pts, 10 reb, 10 ast, 10 blk)", "The Only 4 NBA Players Official Recognized with a Quadruple-Double"),
        ("F1", "Drivers Winning Monaco GP, Indy 500, and Le Mans 24h", "Graham Hill ('Mr. Monaco' - 5 Monaco wins, 1966 Indy 500, 1972 Le Mans)", "Fernando Alonso (2 Monaco wins, 2 Le Mans wins, missed Indy 500 victory)", "Juan Pablo Montoya (Monaco & Indy 500 winner, 3rd at Le Mans)", "Motorsport Triple Crown Achievers", "Graham Hill - The Only Driver in History to Complete Motorsport's Triple Crown"),
        ("Tennis", "Longest Professional Tennis Match in History", "John Isner vs Nicolas Mahut (Wimbledon 2010)", "Duration: 11 hours 5 minutes over 3 days", "Final score 70-68 in 5th set", "Total 183 games played & 216 aces hit", "The 11-Hour 5-Minute Marathon Match at Wimbledon 2010"),
        ("Badminton", "All 5 World Championship Titles Won by Single Country", "China (1987 Beijing & 2011 London World Championships)", "Swept Men's Singles, Women's Singles, Men's Doubles, Women's Doubles, & Mixed Doubles", "Unprecedented 5-Gold Sweep", "Badminton World Championship Dominance", "China - The Only Nation to Sweep All 5 Gold Medals at a Single Badminton World Championships"),
        ("Golf", "Grand Slam Winners in a Single Calendar Year", "Bobby Jones (1930 - US Open, US Amateur, Open Championship, British Amateur)", "Pre-modern Major Era Grand Slam", "Retires at age 28 after winning all 4", "Golf Historic Landmark", "Bobby Jones - The Only Golfer to Complete a Single-Calendar-Year Grand Slam (1930)"),
        ("Boxing", "Heavyweight Champion Winning Title at Age 45", "George Foreman (Defeated Michael Moorer in 1994 at age 45)", "Broke Jersey Joe Walcott's record (age 37)", "Wore same red trunks as vs Muhammad Ali in 1974", "Oldest Heavyweight Champion in History", "George Foreman - The Oldest Boxer to Win the World Heavyweight Championship"),
        ("Kho Kho", "Kho Kho Minimum Pursuit Time & Out of Bounds Rules", "Defender stepping both feet outside lobby boundary is OUT", "Chaser must give KHO within 3 seconds of touching seated player", "Defender surviving full 9 minutes awards 2 bonus points to defending team", "Defensive Endurance Bonus", "Rules Regarding Out-of-Bounds Eliminations and Endurance Bonus Points in Kho Kho"),
        ("Dodgeball", "Dodgeball 5-Second Rule & Ball Possession Violation", "Team holding more than half the live balls has 5 seconds to throw", "Countdown called loudly by Head Referee ('5-4-3-2-1-THROW')", "Failure to throw forfeits all held balls to opponent team", "Penalty forces turnover of possession", "The 5-Second Rule Governing Ball Hoarding and Pace of Play in International Dodgeball"),
        ("Cricket", "Bowlers with 500+ Test Wickets AND 5+ Test Centuries", "Sir Garfield Sobers (235 wkts & 26 centuries)", "Jacques Kallis (292 wkts & 45 centuries)", "Kapil Dev (434 wkts & 8 centuries)", "Ian Botham (383 wkts & 14 centuries) & Ravichandran Ashwin (530+ wkts & 6 centuries)", "All-Time Cricket Greats with Over 300 Test Wickets AND 5 or More Test Centuries"),
        ("Football", "Most Assists in UEFA Champions League History", "Cristiano Ronaldo (42 assists)", "Lionel Messi (40 assists)", "Angel Di María (39 assists)", "Neymar (33 assists) & Ryan Giggs (31 assists)", "The All-Time Top Assist Providers in UEFA Champions League History"),
        ("Basketball", "NBA Player Winning Championship with 3 Different Franchises", "LeBron James (Miami Heat, Cleveland Cavaliers, LA Lakers)", "Robert Horry (Houston Rockets, LA Lakers, San Antonio Spurs)", "John Salley (Detroit Pistons, Chicago Bulls, LA Lakers)", "Danny Green (San Antonio Spurs, Toronto Raptors, LA Lakers)", "NBA Players Who Won Championship Rings with Three Different Franchises"),
        ("Athletics", "Fastest Women's 100m Runner", "Florence Griffith-Joyner (10.49s - 1988)", "Elaine Thompson-Herah (10.54s - 2021)", "Shelly-Ann Fraser-Pryce (10.60s - 2021)", "Carmelita Jeter (10.64s)", "The Fastest Women 100m Sprinters in Track & Field History"),
        ("Olympics", "Youngest Individual Olympic Gold Medalist", "Marjorie Gestring (13 years 268 days - 3m Springboard Diving 1936)", "Nishiya Momiji (13 years 330 days - Skateboard 2020)", "Fu Mingxia (13 years 346 days - 10m Platform Diving 1992)", "Teenage Olympic Champions", "The Youngest Individual Olympic Gold Medalists in Modern History"),
        ("F1", "F1 Teams Winning 15+ Races in a Single Season", "Red Bull Racing (21 wins in 2023 - 95.4% win rate)", "Mercedes-AMG (19 wins in 2016)", "McLaren (15 wins in 1988 - MP4/4)", "Ferrari (15 wins in 2002 & 2004)", "Formula 1 Teams That Recorded 15 or More Grand Prix Victories in a Single Season"),
        ("Cricket", "Lowest Team Total in Test Cricket History", "New Zealand (26 all out vs England 1955)", "South Africa (30 all out vs England 1896 & 1924)", "Australia (36 all out vs England 1902) & India (36 all out vs Australia 2020)", "Lowest Test Match Team Innings Scores", "The Lowest Team Innings Totals Ever Recorded in Men's Test Cricket"),
        ("Football", "Players Winning FIFA World Cup, UEFA Champions League, and Ballon d'Or", "Bobby Charlton", "Franz Beckenbauer", "Gerd Müller", "Paolo Rossi, Zinedine Zidane, Rivaldo, Ronaldinho, Kaká, Lionel Messi", "The Exclusive 9 Players Who Won the World Cup, Champions League, and Ballon d'Or"),
        ("Tennis", "Players Reaching All 4 Grand Slam Finals in a Single Calendar Year", "Rod Laver (1962 & 1969)", "Roger Federer (2006, 2007, 2009)", "Novak Djokovic (2015, 2021, 2023)", "Steffi Graf (1988 & 1989) & Monica Seles (1992)", "Tennis Players Who Reached Men's or Women's Singles Finals of All 4 Grand Slams in One Year"),
        ("Volleyball", "Longest Set Score in Professional Volleyball", "46-44 (Cuneo vs Treviso - Italian League 2002)", "54-52 (AEK Athens vs PAOK - Greek League 2013)", "Played past standard 25 points", "Must win by 2 clear points without upper cap", "The Highest Scoring Extended Sets in Professional Volleyball History"),
        ("Table Tennis", "Ma Long - The Only Double Grand Slam Champion", "Olympic Men's Singles Gold (Rio 2016 & Tokyo 2020)", "World Singles Champion (2015, 2017, 2019)", "World Cup Champion (2012, 2015)", "The 'Dragon' of Table Tennis", "Ma Long - The First and Only Male Table Tennis Player to Achieve a Double Career Grand Slam"),
        ("Rugby", "Only Team to Win Back-to-Back Rugby World Cups Twice", "New Zealand All Blacks (2011 & 2015)", "South Africa Springboks (2019 & 2023)", "Dominant Southern Hemisphere Rugby Giants", "Back-to-Back World Champions", "National Rugby Teams That Successfully Defended Their Rugby World Cup Title"),
        ("Kho Kho", "Kho Kho Single Chain Defense Duration Benchmark", "Defender runs in zig-zag S-shaped pattern between chasers", "Requires continuous foot agility for full 3-minute sub-batch", "Chaser giving early KHO can cut off chain angle", "High-End Defensive Strategy", "The Mechanics and Tactical Endurance Required for a Single Chain Defense in Kho Kho"),
        ("Dodgeball", "Dodgeball Honesty Rule & Self-Out Protocol", "Player hit by ball must raise hand immediately and exit court", "Failure to self-report hit incurs yellow card penalty", "Code of Honor & Sportsmanship Foundation", "Spirit of Dodgeball Play", "The 'Honesty Policy' and Self-Out Code of Conduct in Official Dodgeball Regulations"),
        ("Cricket", "Bowler Bowled 4 Balls in an Over & Took 4 Wickets in 4 Balls in T20I", "Rashid Khan (vs Ireland 2019)", "Lasith Malinga (vs New Zealand 2019)", "Curtis Campher (vs Netherlands 2021 World Cup)", "Jason Holder (vs England 2022)", "Bowlers Who Have Taken 4 Wickets in 4 Consecutive Balls in T20 International Cricket"),
        ("Football", "Fastest Goal in FIFA World Cup History", "Hakan Şükür (10.8 seconds - Turkey vs South Korea 2002)", "Vaclav Masek (15 seconds - Czechoslovakia vs Mexico 1962)", "Ernst Lehner (25 seconds - Germany vs Austria 1934)", "Bryan Robson (27 seconds - England vs France 1982)", "The Fastest Goals Ever Scored from Kick-Off in FIFA World Cup History"),
        ("Basketball", "NBA Player with Most Championship Rings as Player", "Bill Russell (11 NBA Championships in 13 seasons)", "Sam Jones (10 NBA Championships)", "John Havlicek, K.C. Jones, Tom Heinsohn (8 Championships)", "Boston Celtics 1950s-60s Dynasty", "Bill Russell - The Player with the Most NBA Championship Rings in History"),
        ("Boxing", "Fastest Knockout in Professional Boxing History", "Phil Williams vs Louis Lagermasino (1.5 seconds - 2007)", "Mike Collins vs Pat Brownson (4 seconds - 1947)", "Hector Camacho vs Enrique Cruz (5 seconds - 1981)", "Blink and You Miss It KO", "The Fastest Recorded Knockouts in Boxing History"),
        ("F1", "F1 Drivers Winning World Title in Their Rookie or 2nd Season", "Jacques Villeneuve (Runner-up 1996, Champion 1997 - 2nd season)", "Lewis Hamilton (Runner-up 2007, Champion 2008 - 2nd season)", "Emerson Fittipaldi (Champion 1972 in 2nd full season)", "Instant F1 Prodigies", "Drivers Who Won the Formula 1 World Championship in Their First Two Seasons in the Sport"),
        ("Olympics", "First Athlete to Win 100m Gold in 3 Consecutive Olympics", "Usain Bolt (Beijing 2008, London 2012, Rio 2016)", "Undefeated in Olympic 100m & 200m finals for 3 Games", "9 Olympic Gold Medals won on track", "Lightening Bolt Legacy", "Usain Bolt - The First Athlete to Win 100m and 200m Olympic Gold at Three Consecutive Games"),
        ("Kho Kho", "Kho Kho Third Penalty Rule & Technical Disqualification", "Accumulation of 3 fouls by chasers in a single turn", "Awards automatic 1 point to defending team", "Chaser must reset position to baseline pole", "Technical Penalty Enforcement", "Rules Governing Accumulation of Technical Fouls and Penalty Points in Kho Kho"),
        ("Dodgeball", "Dodgeball Simultaneous Hit & Catch Resolution", "Ball hits player A and is caught by player B before touching ground", "Player A remains SAFE in match", "Thrower is eliminated", "Player B's catch overrides initial impact", "Official WDBF Rule Resolving Simultaneous Deflection Hits and Team Catches in Dodgeball"),
        ("Cricket", "Test Bowler with Most Wickets Without Ever Bowling a No-Ball", "Lance Gibbs (309 Test wickets - 0 no-balls)", "Dennis Lillee (355 Test wickets - 0 no-balls in Test career recorded)", "Imran Khan (362 Test wickets - 0 no-balls)", "Fred Trueman & Kapil Dev (434 Test wickets - 0 no-balls)", "Iconic Test Bowlers Who Never Bowled a Single No-Ball in Their Entire International Career"),
        ("Football", "Goalkeeper Who Scored 100+ Professional Goals", "Rogério Ceni (131 goals for São Paulo)", "José Luis Chilavert (67 goals - Hat-trick of penalties)", "René Higuita (43 goals & Scorpion Kick)", "Jorge Campos (46 goals - played as striker and keeper)", "Goalkeepers Who Scored Dozens of Goals from Penalties and Free Kicks"),
        ("Tennis", "Only Player to Beat Federer, Nadal, and Djokovic at Same Tournament", "David Nalbandian (Madrid Masters 2007)", "Novak Djokovic (Montreal 2007 - beat Federer, Nadal, Roddick)", "Boris Becker & Michael Stich historical beats", "Elite Giant Killers", "David Nalbandian & Novak Djokovic - Players Who Defeated Federer, Nadal, and Djokovic in a Single Tournament"),
        ("Athletics", "Sub-4 Minute Mile First Runner", "Sir Roger Bannister (3:59.4 - May 6, 1954 at Iffley Road, Oxford)", "Chris Chataway & Chris Brasher as pacemakers", "Believed biologically impossible before 1954", "Milestone in Human Endurance", "Sir Roger Bannister - The First Person to Run a Mile in Under 4 Minutes"),
        ("Golf", "Oldest Winner of a Men's Major Golf Championship", "Phil Mickelson (2021 PGA Championship - Age 50 years 11 months)", "Julius Boros (1968 PGA Championship - Age 48 years 4 months)", "Old Tom Morris (1867 Open Championship - Age 46 years 3 months)", "Jack Nicklaus (1986 Masters - Age 46 years 2 months)", "Phil Mickelson - The Oldest Golfer to Win a Major Championship in History"),
        ("Multi-Sport", "Only Athlete to Win Olympic Medals in Both Summer and Winter Games in Same Year", "Christa Luding-Rothenburger (1988: Gold in Speed Skating & Silver in Track Cycling)", "Only athlete in history to accomplish dual-season medal feat in 1 year", "East German Legend", "Unique Olympic Record", "Christa Luding-Rothenburger - The Only Athlete to Win Summer & Winter Olympic Medals in the Same Calendar Year")
    ]

    for idx, (sp, tt, c1, c2, c3, c4, ans) in enumerate(hard_list, start=1):
        hq.append({
            "id": f"H{idx:02d}",
            "difficulty": "hard",
            "type": "connection",
            "sport": sp,
            "title": tt,
            "clues": [f"Clue 1: {c1}", f"Clue 2: {c2}", f"Clue 3: {c3}", f"Clue 4: {c4}"],
            "answer": ans,
            "explanation": f"All four clues directly connect to {ans}."
        })
    return hq

easy_q = get_easy_questions()
med_q = get_medium_questions()
hard_q = get_hard_questions()

print(f"Easy Questions: {len(easy_q)}")
print(f"Medium Questions: {len(med_q)}")
print(f"Hard Questions: {len(hard_q)}")

all_questions = easy_q + med_q + hard_q
print(f"Total Questions Generated: {len(all_questions)}")

# Write all questions to a JSON file to inspect
with open("d:\\Case\\questions_db.json", "w", encoding="utf-8") as f:
    json.dump(all_questions, f, indent=2, ensure_ascii=False)

print("questions_db.json created successfully!")

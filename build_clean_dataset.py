import json

# Re-building all 180 questions with accurate facts, proper sport tags, clean question text,
# and close, contextually relevant options of the same category.

questions = [
    # 0 - 19
    {
        "id": "Q001", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which national team won the 2023 ICC Men's Cricket World Cup?",
        "options": ["India", "Australia", "South Africa", "New Zealand"],
        "correct": 1
    },
    {
        "id": "Q002", "sport": "Tennis", "difficulty": "Easy",
        "question": "Which Grand Slam tournament is held annually in Melbourne?",
        "options": ["Australian Open", "French Open", "Wimbledon", "US Open"],
        "correct": 0
    },
    {
        "id": "Q003", "sport": "Cricket", "difficulty": "Easy",
        "question": "How many runs is a hit that bounces before crossing the boundary worth?",
        "options": ["2", "4", "6", "3"],
        "correct": 1
    },
    {
        "id": "Q004", "sport": "Tennis", "difficulty": "Easy",
        "question": "Which Grand Slam tournament is played on grass courts?",
        "options": ["Australian Open", "French Open", "Wimbledon", "US Open"],
        "correct": 2
    },
    {
        "id": "Q005", "sport": "Football", "difficulty": "Easy",
        "question": "Which trophy is awarded to the FIFA World Cup winners?",
        "options": ["UEFA Champions League Trophy", "The FIFA World Cup Trophy", "Ballon d'Or", "Copa América"],
        "correct": 1
    },
    {
        "id": "Q006", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the traditional court surface used at Wimbledon?",
        "options": ["Clay", "Hard Court", "Carpet", "Grass"],
        "correct": 3
    },
    {
        "id": "Q007", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the term for the stroke played on the side opposite to the dominant hand?",
        "options": ["Forehand", "Backhand", "Volley", "Slice"],
        "correct": 1
    },
    {
        "id": "Q008", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the term for a 40-40 tie in a tennis game?",
        "options": ["Deuce", "Advantage", "Break Point", "Tiebreak"],
        "correct": 0
    },
    {
        "id": "Q009", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the term for a high, arching shot designed to go over an opponent's head?",
        "options": ["Smash", "Lob", "Drop shot", "Passing shot"],
        "correct": 1
    },
    {
        "id": "Q010", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which Indian batter is world-famous for inventing the 'helicopter shot'?",
        "options": ["Sachin Tendulkar", "MS Dhoni", "Virender Sehwag", "AB de Villiers"],
        "correct": 1
    },
    {
        "id": "Q011", "sport": "Tennis", "difficulty": "Easy",
        "question": "In a standard tennis game, what score comes immediately after 30?",
        "options": ["35", "40", "45", "Game"],
        "correct": 1
    },
    {
        "id": "Q012", "sport": "Cricket", "difficulty": "Easy",
        "question": "How many wooden stumps make up the wicket at one end of the pitch?",
        "options": ["2", "3", "4", "5"],
        "correct": 1
    },
    {
        "id": "Q013", "sport": "Tennis", "difficulty": "Easy",
        "question": "On which court surface is the French Open played?",
        "options": ["Hard Court", "Grass", "Clay", "Carpet"],
        "correct": 2
    },
    {
        "id": "Q014", "sport": "Cricket", "difficulty": "Easy",
        "question": "What is taking three wickets in three consecutive deliveries called?",
        "options": ["Super Over", "Triple Strike", "Hat-trick", "Clean Sweep"],
        "correct": 2
    },
    {
        "id": "Q015", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is a powerful, overhead shot used to finish a point called?",
        "options": ["Drop shot", "Slice", "Smash", "Volley"],
        "correct": 2
    },
    {
        "id": "Q016", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the name of the central mesh barrier that divides the tennis court?",
        "options": ["Baseline", "Service Line", "Alley", "Net"],
        "correct": 3
    },
    {
        "id": "Q017", "sport": "Cricket", "difficulty": "Easy",
        "question": "How many runs is a hit over the boundary without bouncing worth?",
        "options": ["4", "6", "8", "5"],
        "correct": 1
    },
    {
        "id": "Q018", "sport": "Football", "difficulty": "Easy",
        "question": "Which governing body oversees world football?",
        "options": ["UEFA", "CONMEBOL", "FIFA", "IOC"],
        "correct": 2
    },
    {
        "id": "Q019", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is it called when a server commits two consecutive serving errors?",
        "options": ["Foot fault", "Let", "Fault", "Double fault"],
        "correct": 3
    },
    {
        "id": "Q020", "sport": "Cricket", "difficulty": "Easy",
        "question": "What color ball is traditionally used in daytime Test cricket?",
        "options": ["White", "Red", "Pink", "Yellow"],
        "correct": 1
    },

    # 20 - 39
    {
        "id": "Q021", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which country won the 2024 ICC Men's T20 World Cup?",
        "options": ["South Africa", "England", "India", "Australia"],
        "correct": 2
    },
    {
        "id": "Q022", "sport": "Football", "difficulty": "Easy",
        "question": "Which player has won the most Ballon d'Or awards in history?",
        "options": ["Cristiano Ronaldo", "Johan Cruyff", "Lionel Messi", "Michel Platini"],
        "correct": 2
    },
    {
        "id": "Q023", "sport": "Football", "difficulty": "Easy",
        "question": "How many players are on the field for one team at the start of a football match?",
        "options": ["10", "9", "12", "11"],
        "correct": 3
    },
    {
        "id": "Q024", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the term for winning a point directly from a serve that the opponent cannot touch?",
        "options": ["Ace", "Winner", "Smash", "Passing shot"],
        "correct": 0
    },
    {
        "id": "Q025", "sport": "Tennis", "difficulty": "Easy",
        "question": "What term is used in tennis scoring to represent zero points?",
        "options": ["Nil", "Zero", "Love", "Blank"],
        "correct": 2
    },
    {
        "id": "Q026", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the term for a shot hit softly over the net, landing just on the other side?",
        "options": ["Drop shot", "Lob", "Slice", "Volley"],
        "correct": 0
    },
    {
        "id": "Q027", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which country hosted the 2023 ICC Men's Cricket World Cup?",
        "options": ["Australia", "England", "India", "South Africa"],
        "correct": 2
    },
    {
        "id": "Q028", "sport": "Tennis", "difficulty": "Easy",
        "question": "What color are tennis balls universally used in professional tournaments today?",
        "options": ["White", "Yellow / Optic Yellow", "Bright Green", "Orange"],
        "correct": 1
    },
    {
        "id": "Q029", "sport": "Football", "difficulty": "Easy",
        "question": "Who is globally celebrated as 'The King of Football' (O Rei)?",
        "options": ["Pelé", "Diego Maradona", "Johan Cruyff", "Zinedine Zidane"],
        "correct": 0
    },
    {
        "id": "Q030", "sport": "Tennis", "difficulty": "Easy",
        "question": "What score must a player reach first to win a standard set tie-break?",
        "options": ["5 points", "6 points", "7 points", "10 points"],
        "correct": 2
    },
    {
        "id": "Q031", "sport": "Cricket", "difficulty": "Easy",
        "question": "What color ball is commonly used in day-night ODI matches?",
        "options": ["Red", "White", "Pink", "Orange"],
        "correct": 1
    },
    {
        "id": "Q032", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is a legal serve that goes untouched by the receiver called?",
        "options": ["Fault", "Ace", "Let", "Winner"],
        "correct": 1
    },
    {
        "id": "Q033", "sport": "Football", "difficulty": "Easy",
        "question": "What color card is shown by the referee to send a player off the field?",
        "options": ["Yellow", "Red", "Blue", "Black"],
        "correct": 1
    },
    {
        "id": "Q034", "sport": "Football", "difficulty": "Easy",
        "question": "What is the maximum number of regular substitutions allowed per team in top competitions today?",
        "options": ["3", "4", "6", "5"],
        "correct": 3
    },
    {
        "id": "Q035", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which Indian cricketer is famously nicknamed 'Hitman'?",
        "options": ["Virat Kohli", "MS Dhoni", "Rohit Sharma", "KL Rahul"],
        "correct": 2
    },
    {
        "id": "Q036", "sport": "Football", "difficulty": "Easy",
        "question": "Which world superstar footballer is famously nicknamed 'La Pulga'?",
        "options": ["Cristiano Ronaldo", "Neymar Jr.", "Kylian Mbappé", "Lionel Messi"],
        "correct": 3
    },
    {
        "id": "Q037", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which country is historically recognized as the birthplace of cricket?",
        "options": ["Australia", "India", "England", "South Africa"],
        "correct": 2
    },
    {
        "id": "Q038", "sport": "Cricket", "difficulty": "Easy",
        "question": "What is the maximum number of overs per innings in a T20 match?",
        "options": ["15", "20", "50", "10"],
        "correct": 1
    },
    {
        "id": "Q039", "sport": "Football", "difficulty": "Easy",
        "question": "How long is a standard football match (excluding extra time and stoppage time)?",
        "options": ["80 minutes", "90 minutes", "100 minutes", "60 minutes"],
        "correct": 1
    },
    {
        "id": "Q040", "sport": "Cricket", "difficulty": "Easy",
        "question": "In cricket, what is a batter dismissed without scoring any runs called?",
        "options": ["A golden duck", "A duck", "A maiden", "A clean bowl"],
        "correct": 1
    },

    # 40 - 59
    {
        "id": "Q041", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which legendary Indian captain is fondly known as 'Captain Cool'?",
        "options": ["Kapil Dev", "Sourav Ganguly", "MS Dhoni", "Rahul Dravid"],
        "correct": 2
    },
    {
        "id": "Q042", "sport": "Tennis", "difficulty": "Easy",
        "question": "What term describes a tennis match played with one player on each side?",
        "options": ["Doubles", "Mixed Doubles", "Singles", "Solo"],
        "correct": 2
    },
    {
        "id": "Q043", "sport": "Cricket", "difficulty": "Easy",
        "question": "How many players are on the field for one fielding team in cricket?",
        "options": ["10", "11", "12", "9"],
        "correct": 1
    },
    {
        "id": "Q044", "sport": "Tennis", "difficulty": "Easy",
        "question": "What is the term for a shot hit before the ball bounces on the court?",
        "options": ["Groundstroke", "Volley", "Half-volley", "Drop shot"],
        "correct": 1
    },
    {
        "id": "Q045", "sport": "Football", "difficulty": "Easy",
        "question": "What is awarded when a defending player commits a foul inside their own penalty box?",
        "options": ["Direct free kick", "Corner kick", "Penalty kick", "Indirect free kick"],
        "correct": 2
    },
    {
        "id": "Q046", "sport": "Tennis", "difficulty": "Easy",
        "question": "Which Grand Slam tournament is played in New York City?",
        "options": ["Australian Open", "French Open", "Wimbledon", "US Open"],
        "correct": 3
    },
    {
        "id": "Q047", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which nation won the first-ever Cricket World Cup in 1975?",
        "options": ["Australia", "West Indies", "England", "India"],
        "correct": 1
    },
    {
        "id": "Q048", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which Indian cricketer is famously nicknamed 'King Kohli'?",
        "options": ["Rohit Sharma", "Virat Kohli", "Shubman Gill", "Yuvraj Singh"],
        "correct": 1
    },
    {
        "id": "Q049", "sport": "Football", "difficulty": "Easy",
        "question": "Which South American country is home to the famous football club Boca Juniors?",
        "options": ["Brazil", "Argentina", "Uruguay", "Colombia"],
        "correct": 1
    },
    {
        "id": "Q050", "sport": "Tennis", "difficulty": "Easy",
        "question": "What rule violation occurs when a server touches the baseline before hitting the serve?",
        "options": ["Line violation", "Double fault", "Foot fault", "Service fault"],
        "correct": 2
    },
    {
        "id": "Q051", "sport": "Football", "difficulty": "Easy",
        "question": "Which country won the FIFA World Cup in 2022 held in Qatar?",
        "options": ["Argentina", "France", "Croatia", "Brazil"],
        "correct": 0
    },
    {
        "id": "Q052", "sport": "Tennis", "difficulty": "Easy",
        "question": "What score value does the word 'Love' represent in tennis?",
        "options": ["0", "15", "30", "40"],
        "correct": 0
    },
    {
        "id": "Q053", "sport": "Football", "difficulty": "Easy",
        "question": "Which Liverpool star footballer is affectionately known as 'The Egyptian King'?",
        "options": ["Sadio Mané", "Mohamed Salah", "Roberto Firmino", "Riyad Mahrez"],
        "correct": 1
    },
    {
        "id": "Q054", "sport": "Tennis", "difficulty": "Easy",
        "question": "What surface are the matches at Wimbledon played on?",
        "options": ["Red Clay", "Hard Court", "Synthetic", "Grass"],
        "correct": 3
    },
    {
        "id": "Q055", "sport": "Olympic Sports", "difficulty": "Easy",
        "question": "Which city hosted the 2020 Summer Olympic Games (held in 2021)?",
        "options": ["Beijing", "Rio de Janeiro", "Tokyo", "Paris"],
        "correct": 2
    },
    {
        "id": "Q056", "sport": "Tennis", "difficulty": "Easy",
        "question": "On which court surface is the French Open (Roland Garros) played?",
        "options": ["Grass", "Hard Court", "Red Clay", "Carpet"],
        "correct": 2
    },
    {
        "id": "Q057", "sport": "Olympic Sports", "difficulty": "Easy",
        "question": "Which city hosted the iconic 2008 Summer Olympic Games?",
        "options": ["London", "Athens", "Beijing", "Tokyo"],
        "correct": 2
    },
    {
        "id": "Q058", "sport": "Football", "difficulty": "Easy",
        "question": "Which legendary football superstar is widely known as 'CR7'?",
        "options": ["Lionel Messi", "Cristiano Ronaldo", "Neymar Jr.", "Ronaldo Nazário"],
        "correct": 1
    },
    {
        "id": "Q059", "sport": "Cricket", "difficulty": "Easy",
        "question": "What is the maximum number of overs per team in a standard Men's ODI match?",
        "options": ["20", "40", "50", "60"],
        "correct": 2
    },
    {
        "id": "Q060", "sport": "Cricket", "difficulty": "Easy",
        "question": "Which nation has won the most ICC Men's ODI World Cup titles?",
        "options": ["India", "West Indies", "Australia", "England"],
        "correct": 2
    },

    # 60 - 79
    {
        "id": "Q061", "sport": "Basketball", "difficulty": "Medium",
        "question": "Who holds the NBA record for most career triple-doubles?",
        "options": ["Magic Johnson", "Oscar Robertson", "Russell Westbrook", "LeBron James"],
        "correct": 2
    },
    {
        "id": "Q062", "sport": "Football", "difficulty": "Medium",
        "question": "Which club has won the most UEFA Champions League (European Cup) titles?",
        "options": ["AC Milan", "Bayern Munich", "Liverpool", "Real Madrid"],
        "correct": 3
    },
    {
        "id": "Q063", "sport": "Basketball", "difficulty": "Medium",
        "question": "Who scored 100 points in a single NBA game in 1962?",
        "options": ["Kobe Bryant", "Wilt Chamberlain", "Michael Jordan", "Kareem Abdul-Jabbar"],
        "correct": 1
    },
    {
        "id": "Q064", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who scored the highest individual score in Test history (400 not out)?",
        "options": ["Don Bradman", "Brian Lara", "Virender Sehwag", "Matthew Hayden"],
        "correct": 1
    },
    {
        "id": "Q065", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA team has won the most championship titles overall?",
        "options": ["Los Angeles Lakers", "Boston Celtics", "Golden State Warriors", "Chicago Bulls"],
        "correct": 1
    },
    {
        "id": "Q066", "sport": "Football", "difficulty": "Medium",
        "question": "Who is the all-time top goalscorer in men's international football history?",
        "options": ["Lionel Messi", "Pelé", "Ali Daei", "Cristiano Ronaldo"],
        "correct": 3
    },
    {
        "id": "Q067", "sport": "Tennis", "difficulty": "Medium",
        "question": "Who holds the record for the most Grand Slam Men's singles titles?",
        "options": ["Roger Federer", "Rafael Nadal", "Novak Djokovic", "Pete Sampras"],
        "correct": 2
    },
    {
        "id": "Q068", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who has scored the most total centuries (100) in international cricket?",
        "options": ["Virat Kohli", "Ricky Ponting", "Sachin Tendulkar", "Jacques Kallis"],
        "correct": 2
    },
    {
        "id": "Q069", "sport": "Basketball", "difficulty": "Medium",
        "question": "Who is the NBA's all-time leading scorer in total regular season points?",
        "options": ["Kareem Abdul-Jabbar", "LeBron James", "Karl Malone", "Kobe Bryant"],
        "correct": 1
    },
    {
        "id": "Q070", "sport": "Football", "difficulty": "Medium",
        "question": "Which country has won the most FIFA Men's World Cup titles (5 titles)?",
        "options": ["Germany", "Italy", "Argentina", "Brazil"],
        "correct": 3
    },
    {
        "id": "Q071", "sport": "Tennis", "difficulty": "Medium",
        "question": "Which female tennis player has won 23 Grand Slam singles titles in the Open Era?",
        "options": ["Steffi Graf", "Serena Williams", "Martina Navratilova", "Chris Evert"],
        "correct": 1
    },
    {
        "id": "Q072", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which bowler has taken the most overall wickets in Test cricket history (800 wickets)?",
        "options": ["Shane Warne", "Anil Kumble", "Muttiah Muralitharan", "James Anderson"],
        "correct": 2
    },
    {
        "id": "Q073", "sport": "Football", "difficulty": "Medium",
        "question": "Which English club has won the most Premier League titles since its rebranding in 1992?",
        "options": ["Manchester City", "Arsenal", "Chelsea", "Manchester United"],
        "correct": 3
    },
    {
        "id": "Q074", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which player led the Chicago Bulls to six NBA championships in the 1990s?",
        "options": ["Scottie Pippen", "Michael Jordan", "Dennis Rodman", "Hakeem Olajuwon"],
        "correct": 1
    },
    {
        "id": "Q075", "sport": "Tennis", "difficulty": "Medium",
        "question": "Who is known as the 'King of Clay' for winning 14 French Open singles titles?",
        "options": ["Novak Djokovic", "Roger Federer", "Rafael Nadal", "Björn Borg"],
        "correct": 2
    },
    {
        "id": "Q076", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which team won the inaugural edition of the Indian Premier League (IPL) in 2008?",
        "options": ["Chennai Super Kings", "Mumbai Indians", "Rajasthan Royals", "Kolkata Knight Riders"],
        "correct": 2
    },
    {
        "id": "Q077", "sport": "Football", "difficulty": "Medium",
        "question": "Who won the FIFA Men's World Cup Golden Boot in 2022 by scoring 8 goals?",
        "options": ["Lionel Messi", "Kylian Mbappé", "Julian Alvarez", "Olivier Giroud"],
        "correct": 1
    },
    {
        "id": "Q078", "sport": "Tennis", "difficulty": "Medium",
        "question": "Which team tournament is regarded as the premier international team competition in men's tennis?",
        "options": ["Laver Cup", "ATP Cup", "Davis Cup", "Hopman Cup"],
        "correct": 2
    },
    {
        "id": "Q079", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which team drafted Stephen Curry 7th overall in the 2009 NBA Draft?",
        "options": ["Minnesota Timberwolves", "Golden State Warriors", "New York Knicks", "Sacramento Kings"],
        "correct": 1
    },
    {
        "id": "Q080", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who holds the record for the fastest century in Men's ODI cricket (off 31 balls)?",
        "options": ["Shahid Afridi", "Corey Anderson", "AB de Villiers", "Chris Gayle"],
        "correct": 2
    },

    # 80 - 99
    {
        "id": "Q081", "sport": "Cricket", "difficulty": "Medium",
        "question": "Against which nation did Anil Kumble take all 10 wickets in a single Test innings (1999)?",
        "options": ["Australia", "England", "Pakistan", "South Africa"],
        "correct": 2
    },
    {
        "id": "Q082", "sport": "Football", "difficulty": "Medium",
        "question": "Which manager won the 'Treble' with Manchester United in 1999 and Manchester City in 2023?",
        "options": ["Alex Ferguson", "Pep Guardiola", "José Mourinho", "Carlo Ancelotti"],
        "correct": 1
    },
    {
        "id": "Q083", "sport": "Tennis", "difficulty": "Medium",
        "question": "Who was the first male player to complete the career 'Golden Slam' (all 4 Grand Slams + Olympic Gold)?",
        "options": ["Andre Agassi", "Rafael Nadal", "Novak Djokovic", "Roger Federer"],
        "correct": 0
    },
    {
        "id": "Q084", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA star is nicknamed 'The Greek Freak'?",
        "options": ["Luka Dončić", "Giannis Antetokounmpo", "Nikola Jokić", "Joel Embiid"],
        "correct": 1
    },
    {
        "id": "Q085", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who was named Player of the Tournament in India's victorious 2011 ODI World Cup campaign?",
        "options": ["MS Dhoni", "Sachin Tendulkar", "Yuvraj Singh", "Zaheer Khan"],
        "correct": 2
    },
    {
        "id": "Q086", "sport": "Football", "difficulty": "Medium",
        "question": "Which Italian club is famously nicknamed 'The Old Lady' (La Vecchia Signora)?",
        "options": ["AC Milan", "Inter Milan", "Roma", "Juventus"],
        "correct": 3
    },
    {
        "id": "Q087", "sport": "Tennis", "difficulty": "Medium",
        "question": "Which female tennis player holds the all-time record with 24 Grand Slam singles titles?",
        "options": ["Serena Williams", "Steffi Graf", "Margaret Court", "Martina Navratilova"],
        "correct": 2
    },
    {
        "id": "Q088", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA player has won the most NBA championship rings in history (11 rings)?",
        "options": ["Michael Jordan", "Kareem Abdul-Jabbar", "Bill Russell", "Robert Horry"],
        "correct": 2
    },
    {
        "id": "Q089", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which bowler holds the record for most wickets taken in ODI World Cup history (71 wickets)?",
        "options": ["Wasim Akram", "Glenn McGrath", "Muttiah Muralitharan", "Lasith Malinga"],
        "correct": 1
    },
    {
        "id": "Q090", "sport": "Football", "difficulty": "Medium",
        "question": "Which German stadium is famously known as the home of Borussia Dortmund?",
        "options": ["Allianz Arena", "Signal Iduna Park", "Veltins-Arena", "Olympiastadion Berlin"],
        "correct": 1
    },
    {
        "id": "Q091", "sport": "Tennis", "difficulty": "Medium",
        "question": "Who won the Men's Singles title at Wimbledon in 2023 by defeating Novak Djokovic?",
        "options": ["Carlos Alcaraz", "Jannik Sinner", "Daniil Medvedev", "Alexander Zverev"],
        "correct": 0
    },
    {
        "id": "Q092", "sport": "Basketball", "difficulty": "Medium",
        "question": "Who won the NBA Most Valuable Player (MVP) award in back-to-back seasons (2021 and 2022)?",
        "options": ["Giannis Antetokounmpo", "Nikola Jokić", "Joel Embiid", "LeBron James"],
        "correct": 1
    },
    {
        "id": "Q093", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who holds the record for the highest individual score in Men's ODI cricket history (264 runs)?",
        "options": ["Virender Sehwag", "Martin Guptill", "Rohit Sharma", "Chris Gayle"],
        "correct": 2
    },
    {
        "id": "Q094", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which player was named NBA Finals MVP in 2023 after leading Denver to their first title?",
        "options": ["Jamal Murray", "Nikola Jokić", "Jimmy Butler", "LeBron James"],
        "correct": 1
    },
    {
        "id": "Q095", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who was the first male cricketer to score a double century (200*) in ODI history?",
        "options": ["Virender Sehwag", "Sachin Tendulkar", "Rohit Sharma", "Belinda Clark"],
        "correct": 1
    },
    {
        "id": "Q096", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA legend's silhouette is featured on the official NBA logo ('The Logo')?",
        "options": ["Michael Jordan", "Jerry West", "Wilt Chamberlain", "Oscar Robertson"],
        "correct": 1
    },
    {
        "id": "Q097", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which player holds the all-time record for most Test centuries (51 centuries)?",
        "options": ["Ricky Ponting", "Jacques Kallis", "Sachin Tendulkar", "Rahul Dravid"],
        "correct": 2
    },
    {
        "id": "Q098", "sport": "Football", "difficulty": "Medium",
        "question": "Which club has won the most French Ligue 1 titles in history?",
        "options": ["Marseille", "Lyon", "Paris Saint-Germain", "Saint-Étienne"],
        "correct": 2
    },
    {
        "id": "Q099", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who was awarded Player of the Match in the 2011 ICC ODI World Cup final?",
        "options": ["MS Dhoni", "Gautam Gambhir", "Yuvraj Singh", "Zaheer Khan"],
        "correct": 0
    },

    # 100 - 119
    {
        "id": "Q100", "sport": "Tennis", "difficulty": "Medium",
        "question": "What is the technical term for a serve that clips the net cord but still lands in the service box?",
        "options": ["Fault", "Let", "Ace", "Net ball"],
        "correct": 1
    },
    {
        "id": "Q101", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which fast bowler holds the record for most wickets in Test match history (604+ wickets)?",
        "options": ["Glenn McGrath", "James Anderson", "Stuart Broad", "Wasim Akram"],
        "correct": 1
    },
    {
        "id": "Q102", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA hall-of-famer center is world-famous for inventing the 'Dream Shake' footwork?",
        "options": ["Shaquille O'Neal", "Patrick Ewing", "Hakeem Olajuwon", "David Robinson"],
        "correct": 2
    },
    {
        "id": "Q103", "sport": "Tennis", "difficulty": "Medium",
        "question": "In what year was the first official French Championships (French Open) held?",
        "options": ["1877", "1891", "1905", "1925"],
        "correct": 1
    },
    {
        "id": "Q104", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which batter holds the record for most ODI centuries in international cricket history (50 centuries)?",
        "options": ["Sachin Tendulkar", "Virat Kohli", "Rohit Sharma", "Ricky Ponting"],
        "correct": 1
    },
    {
        "id": "Q105", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which wicketkeeper has recorded the most total dismissals in international cricket history?",
        "options": ["Adam Gilchrist", "MS Dhoni", "Mark Boucher", "Kumar Sangakkara"],
        "correct": 2
    },
    {
        "id": "Q106", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who holds the record for the highest individual score in Men's Test cricket history (400 not out)?",
        "options": ["Don Bradman", "Brian Lara", "Virender Sehwag", "Matthew Hayden"],
        "correct": 1
    },
    {
        "id": "Q107", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA team features a iconic shamrock clover in their primary logo?",
        "options": ["Boston Celtics", "Ireland Pacers", "Chicago Bulls", "New York Knicks"],
        "correct": 0
    },
    {
        "id": "Q108", "sport": "Basketball", "difficulty": "Medium",
        "question": "What is the standard FIBA three-point line distance from the center of the basket?",
        "options": ["6.75 meters", "7.24 meters", "6.00 meters", "7.00 meters"],
        "correct": 0
    },
    {
        "id": "Q109", "sport": "Football", "difficulty": "Medium",
        "question": "Which country hosted the memorable 2014 FIFA World Cup?",
        "options": ["South Africa", "Germany", "Brazil", "Russia"],
        "correct": 2
    },
    {
        "id": "Q110", "sport": "Football", "difficulty": "Medium",
        "question": "What does the abbreviation VAR stand for in modern football refereeing?",
        "options": ["Video Assistant Referee", "Visual Automated Review", "Virtual Action Replay", "Video Analysis Review"],
        "correct": 0
    },
    {
        "id": "Q111", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA franchise did hall-of-famer Tim Duncan play his entire 19-year career for?",
        "options": ["Dallas Mavericks", "Houston Rockets", "San Antonio Spurs", "Los Angeles Lakers"],
        "correct": 2
    },
    {
        "id": "Q112", "sport": "Cricket", "difficulty": "Medium",
        "question": "Against which country did Sachin Tendulkar score his iconic first-ever male 200* in ODIs (2010)?",
        "options": ["Australia", "South Africa", "Sri Lanka", "Pakistan"],
        "correct": 1
    },
    {
        "id": "Q113", "sport": "Cricket", "difficulty": "Medium",
        "question": "Who scored the fastest century in ODI cricket history off just 31 balls?",
        "options": ["Shahid Afridi", "Corey Anderson", "AB de Villiers", "Jos Buttler"],
        "correct": 2
    },
    {
        "id": "Q114", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which franchise won the inaugural BAA (NBA) championship in 1947?",
        "options": ["Philadelphia Warriors", "Chicago Stags", "Boston Celtics", "Minneapolis Lakers"],
        "correct": 0
    },
    {
        "id": "Q115", "sport": "Basketball", "difficulty": "Medium",
        "question": "Who is the NBA's all-time career assists leader (15,806 assists)?",
        "options": ["Jason Kidd", "Steve Nash", "John Stockton", "Chris Paul"],
        "correct": 2
    },
    {
        "id": "Q116", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which spinner holds the record for most wickets in ODI cricket history (534 wickets)?",
        "options": ["Shane Warne", "Anil Kumble", "Muttiah Muralitharan", "Saqlain Mushtaq"],
        "correct": 2
    },
    {
        "id": "Q117", "sport": "Basketball", "difficulty": "Medium",
        "question": "Which NBA team won the 2024 NBA Championship by defeating the Dallas Mavericks?",
        "options": ["Denver Nuggets", "Boston Celtics", "Golden State Warriors", "Milwaukee Bucks"],
        "correct": 1
    },
    {
        "id": "Q118", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which bowler has taken the most total wickets in Test cricket history (800 wickets)?",
        "options": ["Shane Warne", "Muttiah Muralitharan", "James Anderson", "Anil Kumble"],
        "correct": 1
    },
    {
        "id": "Q119", "sport": "Cricket", "difficulty": "Medium",
        "question": "Which Indian skipper hit the iconic winning six and scored 91* in the 2011 World Cup final?",
        "options": ["Gautam Gambhir", "Yuvraj Singh", "MS Dhoni", "Virender Sehwag"],
        "correct": 2
    },

    # 120 - 139 (Hard)
    {
        "id": "Q120", "sport": "Tennis", "difficulty": "Medium",
        "question": "What is the standard length of a regulation tennis court from baseline to baseline?",
        "options": ["78 feet (23.77 m)", "82 feet (25.00 m)", "72 feet (21.95 m)", "80 feet (24.38 m)"],
        "correct": 0
    },
    {
        "id": "Q121", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was the first international batter in cricket history to be given out by a third umpire (TV replay)?",
        "options": ["Sachin Tendulkar", "Rahul Dravid", "Jonty Rhodes", "Brian Lara"],
        "correct": 0
    },
    {
        "id": "Q122", "sport": "Football", "difficulty": "Hard",
        "question": "Which legendary goalkeeper captained Italy to victory in the 2006 FIFA World Cup?",
        "options": ["Iker Casillas", "Gianluigi Buffon", "Oliver Kahn", "Dino Zoff"],
        "correct": 1
    },
    {
        "id": "Q123", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which player has scored the most total centuries in ODI World Cup history (7 centuries)?",
        "options": ["Sachin Tendulkar", "Ricky Ponting", "Rohit Sharma", "David Warner"],
        "correct": 2
    },
    {
        "id": "Q124", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which head coach has won the most NBA championships in history (11 titles)?",
        "options": ["Gregg Popovich", "Red Auerbach", "Phil Jackson", "Pat Riley"],
        "correct": 2
    },
    {
        "id": "Q125", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which batter has hit the most total sixes in Men's ODI World Cup history (54 sixes)?",
        "options": ["Chris Gayle", "AB de Villiers", "Rohit Sharma", "Ricky Ponting"],
        "correct": 2
    },
    {
        "id": "Q126", "sport": "Football", "difficulty": "Hard",
        "question": "Who is the all-time top goalscorer for the Brazil men's national football team?",
        "options": ["Pelé", "Ronaldo Nazário", "Neymar Jr.", "Romário"],
        "correct": 2
    },
    {
        "id": "Q127", "sport": "Football", "difficulty": "Hard",
        "question": "Which national team has reached the most FIFA Men's World Cup final matches (8 finals)?",
        "options": ["Brazil", "Germany", "Italy", "Argentina"],
        "correct": 1
    },
    {
        "id": "Q128", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which coach holds the record for most regular-season wins in NBA coaching history?",
        "options": ["Don Nelson", "Lenny Wilkens", "Gregg Popovich", "Phil Jackson"],
        "correct": 2
    },
    {
        "id": "Q129", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was the first Indian cricketer to score centuries in all three international formats (Test, ODI, T20I)?",
        "options": ["Rohit Sharma", "Virat Kohli", "Suresh Raina", "KL Rahul"],
        "correct": 2
    },
    {
        "id": "Q130", "sport": "Football", "difficulty": "Hard",
        "question": "Which Italian defender won the coveted Ballon d'Or in 2006 after winning the World Cup?",
        "options": ["Paolo Maldini", "Fabio Cannavaro", "Alessandro Nesta", "Gianluigi Buffon"],
        "correct": 1
    },
    {
        "id": "Q131", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which NBA legend scored an astonishing 81 points in a single game against Toronto in 2006?",
        "options": ["LeBron James", "Kobe Bryant", "Tracy McGrady", "Allen Iverson"],
        "correct": 1
    },
    {
        "id": "Q132", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which country won the inaugural FIBA Basketball World Cup held in 1950?",
        "options": ["United States", "Argentina", "Brazil", "Yugoslavia"],
        "correct": 1
    },
    {
        "id": "Q133", "sport": "Tennis", "difficulty": "Hard",
        "question": "Which male player holds the record for the most ATP Finals singles titles (7 titles)?",
        "options": ["Roger Federer", "Novak Djokovic", "Pete Sampras", "Ivan Lendl"],
        "correct": 1
    },
    {
        "id": "Q134", "sport": "Basketball", "difficulty": "Hard",
        "question": "Whose jersey number (#6) was retired across the entire NBA league in 2022?",
        "options": ["Kobe Bryant", "Wilt Chamberlain", "Bill Russell", "Michael Jordan"],
        "correct": 2
    },
    {
        "id": "Q135", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which cricketer scored the fastest double century in Test history (off just 153 balls)?",
        "options": ["Virender Sehwag", "Nathan Astle", "Brendon McCullum", "Adam Gilchrist"],
        "correct": 1
    },
    {
        "id": "Q136", "sport": "Football", "difficulty": "Hard",
        "question": "Who is the only goalkeeper in football history to win the Ballon d'Or (1963)?",
        "options": ["Lev Yashin", "Dino Zoff", "Manuel Neuer", "Gordon Banks"],
        "correct": 0
    },
    {
        "id": "Q137", "sport": "Basketball", "difficulty": "Hard",
        "question": "Who was awarded the very first NBA Finals MVP Award in 1969 despite playing on the losing team?",
        "options": ["Bill Russell", "Wilt Chamberlain", "Jerry West", "John Havlicek"],
        "correct": 2
    },
    {
        "id": "Q138", "sport": "Tennis", "difficulty": "Hard",
        "question": "Who is the only male player to win the Calendar Grand Slam (all 4 in one year) twice in the Open Era?",
        "options": ["Rod Laver", "Don Budge", "Novak Djokovic", "Björn Borg"],
        "correct": 0
    },
    {
        "id": "Q139", "sport": "Tennis", "difficulty": "Hard",
        "question": "Which Grand Slam tournament is the only one still played on its original natural grass surface?",
        "options": ["Australian Open", "French Open", "Wimbledon", "US Open"],
        "correct": 2
    },

    # 140 - 179
    {
        "id": "Q140", "sport": "Football", "difficulty": "Hard",
        "question": "Which legendary football star scored the famous 'Hand of God' goal against England in 1986?",
        "options": ["Pelé", "Diego Maradona", "Mario Kempes", "Zico"],
        "correct": 1
    },
    {
        "id": "Q141", "sport": "Football", "difficulty": "Hard",
        "question": "Which nation won the 1938 FIFA World Cup held in France?",
        "options": ["Italy", "Hungary", "Brazil", "Germany"],
        "correct": 0
    },
    {
        "id": "Q142", "sport": "Football", "difficulty": "Hard",
        "question": "Which European club won the inaugural European Cup (UEFA Champions League) in 1956?",
        "options": ["Reims", "AC Milan", "Real Madrid", "Benfica"],
        "correct": 2
    },
    {
        "id": "Q143", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was the first player in Test cricket history to score a triple century (325 runs in 1930)?",
        "options": ["Don Bradman", "Andy Sandham", "Wally Hammond", "Hanif Mohammad"],
        "correct": 1
    },
    {
        "id": "Q144", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which NBA player scored 70 points in a single game before turning 21 years old?",
        "options": ["Luka Dončić", "Devin Booker", "LeBron James", "Kobe Bryant"],
        "correct": 1
    },
    {
        "id": "Q145", "sport": "Football", "difficulty": "Hard",
        "question": "Which European nation won Euro 1992 as a late substitute team after Yugoslavia was disqualified?",
        "options": ["Germany", "Denmark", "Netherlands", "Sweden"],
        "correct": 1
    },
    {
        "id": "Q146", "sport": "Football", "difficulty": "Hard",
        "question": "Which Brazilian midfielder won the Ballon d'Or award in 2007?",
        "options": ["Ronaldinho", "Kaká", "Rivaldo", "Robinho"],
        "correct": 1
    },
    {
        "id": "Q147", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which famous assistant coach developed the famous 'Triangle Offense' system implemented by Phil Jackson?",
        "options": ["Tex Winter", "Red Holzman", "Chuck Daly", "Larry Brown"],
        "correct": 0
    },
    {
        "id": "Q148", "sport": "Cricket", "difficulty": "Hard",
        "question": "What is Sir Donald Bradman's legendary, unmatched career Test batting average?",
        "options": ["95.14", "99.94", "101.20", "88.60"],
        "correct": 1
    },
    {
        "id": "Q149", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which batter hit an extraordinary 175* off 66 balls in an IPL match for RCB in 2013?",
        "options": ["Brendon McCullum", "Chris Gayle", "AB de Villiers", "KL Rahul"],
        "correct": 1
    },
    {
        "id": "Q150", "sport": "Football", "difficulty": "Hard",
        "question": "Which German city hosted the dramatic 2012 UEFA Champions League final ('Finale Dahoam')?",
        "options": ["Berlin", "Dortmund", "Munich", "Frankfurt"],
        "correct": 2
    },
    {
        "id": "Q151", "sport": "Football", "difficulty": "Hard",
        "question": "Which legendary Italian forward was famously nicknamed 'Il Divin Codino' ('The Divine Ponytail')?",
        "options": ["Alessandro Del Piero", "Roberto Baggio", "Francesco Totti", "Gianfranco Zola"],
        "correct": 1
    },
    {
        "id": "Q152", "sport": "Football", "difficulty": "Hard",
        "question": "Which English club is widely nicknamed 'The Citizens'?",
        "options": ["Manchester City", "Leicester City", "Norwich City", "Bristol City"],
        "correct": 0
    },
    {
        "id": "Q153", "sport": "Football", "difficulty": "Hard",
        "question": "Which Spanish club did Neymar leave when he made his world-record transfer to PSG in 2017?",
        "options": ["Real Madrid", "Santos", "Barcelona", "Atletico Madrid"],
        "correct": 2
    },
    {
        "id": "Q154", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which two international teams contested the very first official Men's T20 International in 2005?",
        "options": ["England and Australia", "Australia and New Zealand", "South Africa and New Zealand", "India and Pakistan"],
        "correct": 1
    },
    {
        "id": "Q155", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which defensive giant won the NBA Defensive Player of the Year award 4 times (tied record)?",
        "options": ["Ben Wallace & Dikembe Mutombo", "Dwight Howard", "Rudy Gobert", "Hakeem Olajuwon"],
        "correct": 0
    },
    {
        "id": "Q156", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which wicketkeeper holds the record for most stumpings in international cricket history (195 stumpings)?",
        "options": ["Kumar Sangakkara", "Romesh Kaluwitharana", "MS Dhoni", "Moin Khan"],
        "correct": 2
    },
    {
        "id": "Q157", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who scored the most total runs in a single edition of an ICC ODI World Cup (765 runs in 2023)?",
        "options": ["Sachin Tendulkar", "Matthew Hayden", "Virat Kohli", "Rohit Sharma"],
        "correct": 2
    },
    {
        "id": "Q158", "sport": "Football", "difficulty": "Hard",
        "question": "Which Italian star famously missed the decisive penalty in the 1994 FIFA World Cup final shootout?",
        "options": ["Franco Baresi", "Daniele Massaro", "Roberto Baggio", "Gianluca Vialli"],
        "correct": 2
    },
    {
        "id": "Q159", "sport": "Basketball", "difficulty": "Hard",
        "question": "Which player won NBA Finals MVP after leading the Dallas Mavericks to their 2011 championship?",
        "options": ["Jason Kidd", "Jason Terry", "Dirk Nowitzki", "Tyson Chandler"],
        "correct": 2
    },
    {
        "id": "Q160", "sport": "Football", "difficulty": "Hard",
        "question": "Which player holds the record for most international caps (appearances) in men's football history?",
        "options": ["Bader Al-Mutawa", "Cristiano Ronaldo", "Soh Chin Ann", "Lionel Messi"],
        "correct": 1
    },
    {
        "id": "Q161", "sport": "Tennis", "difficulty": "Hard",
        "question": "Which Grand Slam tournament has been played on three different surfaces (Grass, Har-Tru Clay, Decoturf Hard) in its history?",
        "options": ["Australian Open", "French Open", "Wimbledon", "US Open"],
        "correct": 3
    },
    {
        "id": "Q162", "sport": "Basketball", "difficulty": "Hard",
        "question": "Who became the first Indian-born player to be drafted and play in an NBA game?",
        "options": ["Sim Bhullar", "Satnam Singh Bhamara", "Princepal Singh", "Amjyot Singh"],
        "correct": 1
    },
    {
        "id": "Q163", "sport": "Football", "difficulty": "Hard",
        "question": "Which African football legend won the Ballon d'Or in 1995 while playing for AC Milan?",
        "options": ["George Weah", "Didier Drogba", "Samuel Eto'o", "Roger Milla"],
        "correct": 0
    },
    {
        "id": "Q164", "sport": "Football", "difficulty": "Hard",
        "question": "Which Italian club did Andrea Pirlo join on a free transfer after leaving AC Milan in 2011?",
        "options": ["Inter Milan", "Juventus", "Roma", "Fiorentina"],
        "correct": 1
    },
    {
        "id": "Q165", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was the first cricketer in history to reach 10,000 runs in Men's ODI cricket?",
        "options": ["Desmond Haynes", "Sunil Gavaskar", "Sachin Tendulkar", "Inzamam-ul-Haq"],
        "correct": 2
    },
    {
        "id": "Q166", "sport": "Football", "difficulty": "Hard",
        "question": "Which player scored the dramatic injury-time winner for Manchester United in the 1999 Champions League final?",
        "options": ["Teddy Sheringham", "Ole Gunnar Solskjær", "Dwight Yorke", "David Beckham"],
        "correct": 1
    },
    {
        "id": "Q167", "sport": "Football", "difficulty": "Hard",
        "question": "Which European nation hosted the inaugural UEFA European Championship (Euro) in 1960?",
        "options": ["Spain", "France", "Soviet Union", "Yugoslavia"],
        "correct": 1
    },
    {
        "id": "Q168", "sport": "Basketball", "difficulty": "Hard",
        "question": "Who won the first official NBA Slam Dunk Contest held during All-Star Weekend in 1984?",
        "options": ["Dominique Wilkins", "Julius Erving", "Larry Nance", "Michael Jordan"],
        "correct": 2
    },
    {
        "id": "Q169", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was the first bowler in cricket history to reach 500 wickets in Test match cricket?",
        "options": ["Shane Warne", "Muttiah Muralitharan", "Courtney Walsh", "Kapil Dev"],
        "correct": 2
    },
    {
        "id": "Q170", "sport": "Football", "difficulty": "Hard",
        "question": "Which Spanish club did Xabi Alonso leave when he transferred to Bayern Munich in 2014?",
        "options": ["Liverpool", "Real Sociedad", "Real Madrid", "Villarreal"],
        "correct": 2
    },
    {
        "id": "Q171", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which player scored the fastest half-century (50) in Men's ODI history off just 16 balls?",
        "options": ["Sanath Jayasuriya", "AB de Villiers", "Shahid Afridi", "Kusal Perera"],
        "correct": 1
    },
    {
        "id": "Q172", "sport": "Football", "difficulty": "Hard",
        "question": "What is the official name of Bayern Munich's iconic home stadium in Munich?",
        "options": ["Signal Iduna Park", "Veltins-Arena", "Allianz Arena", "Olympiastadion"],
        "correct": 2
    },
    {
        "id": "Q173", "sport": "Tennis", "difficulty": "Hard",
        "question": "What is the French Open Men's Singles trophy officially named in honor of?",
        "options": ["Coupe des Mousquetaires", "Coupe Suzanne Lenglen", "Coupe Davis", "Roland Garros Trophy"],
        "correct": 0
    },
    {
        "id": "Q174", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which bowler holds the record for best bowling figures in a Men's ODI innings (8 wickets for 19 runs)?",
        "options": ["Muttiah Muralitharan", "Chaminda Vaas", "Shahid Afridi", "Glenn McGrath"],
        "correct": 1
    },
    {
        "id": "Q175", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which non-wicketkeeper holds the record for most catches in Test cricket history (210 catches)?",
        "options": ["Mahela Jayawardene", "Ricky Ponting", "Rahul Dravid", "Jacques Kallis"],
        "correct": 2
    },
    {
        "id": "Q176", "sport": "Cricket", "difficulty": "Hard",
        "question": "Which bowler took 71 total wickets across ODI World Cup history to set the all-time record?",
        "options": ["Wasim Akram", "Lasith Malinga", "Glenn McGrath", "Mitchell Starc"],
        "correct": 2
    },
    {
        "id": "Q177", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was the first cricketer in history to reach 10,000 runs in Test match cricket?",
        "options": ["Allan Border", "Sachin Tendulkar", "Sunil Gavaskar", "Brian Lara"],
        "correct": 2
    },
    {
        "id": "Q178", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was awarded Player of the Tournament at the 2003 ICC ODI World Cup?",
        "options": ["Ricky Ponting", "Sachin Tendulkar", "Chaminda Vaas", "Adam Gilchrist"],
        "correct": 1
    },
    {
        "id": "Q179", "sport": "Cricket", "difficulty": "Hard",
        "question": "Who was the first spin bowler in cricket history to reach 600 Test match wickets?",
        "options": ["Muttiah Muralitharan", "Shane Warne", "Anil Kumble", "Nathan Lyon"],
        "correct": 1
    },
    {
        "id": "Q180", "sport": "Basketball", "difficulty": "Hard",
        "question": "Who was awarded the very first NBA Most Valuable Player (MVP) award for the 1955-56 season?",
        "options": ["Wilt Chamberlain", "Bob Cousy", "Bob Pettit", "Bill Russell"],
        "correct": 2
    }
]

print(f"Total questions created: {len(questions)}")

# Verify all indices and options
for i, q in enumerate(questions):
    assert len(q["options"]) == 4, f"Question {i} does not have 4 options"
    assert 0 <= q["correct"] <= 3, f"Question {i} invalid correct index"

with open('questions_180.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print("questions_180.json updated successfully!")

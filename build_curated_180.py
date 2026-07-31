import json
import random

# Seed for reproducible option shuffling
random.seed(42)

questions_data = [
    # ==========================================
    # --- EASY FOOTBALL (15) ---
    # ==========================================
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which nation won the 2022 FIFA World Cup hosted in Qatar?",
        "options": ["France", "Brazil", "Argentina", "Croatia"],
        "correct_answer": "Argentina"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which European club has won the most UEFA Champions League titles in history (15 titles)?",
        "options": ["AC Milan", "Liverpool", "Real Madrid", "Bayern Munich"],
        "correct_answer": "Real Madrid"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Who is the all-time leading goalscorer in UEFA Champions League history with 140 goals?",
        "options": ["Lionel Messi", "Robert Lewandowski", "Cristiano Ronaldo", "Karim Benzema"],
        "correct_answer": "Cristiano Ronaldo"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which English manager won 13 Premier League titles with Manchester United between 1986 and 2013?",
        "options": ["Matt Busby", "Sir Alex Ferguson", "Arsène Wenger", "Louis van Gaal"],
        "correct_answer": "Sir Alex Ferguson"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which country has won the most FIFA Men's World Cup titles in history (5 titles)?",
        "options": ["Germany", "Italy", "Brazil", "Argentina"],
        "correct_answer": "Brazil"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which English club went undefeated across the entire 2003-04 Premier League season ('The Invincibles')?",
        "options": ["Chelsea", "Manchester United", "Arsenal", "Liverpool"],
        "correct_answer": "Arsenal"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Who won the 2023 Men's Ballon d'Or award after captaining Argentina to World Cup victory?",
        "options": ["Kylian Mbappé", "Erling Haaland", "Lionel Messi", "Kevin De Bruyne"],
        "correct_answer": "Lionel Messi"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which English club completed a historic treble (Premier League, FA Cup, Champions League) in the 2022-23 season?",
        "options": ["Manchester United", "Liverpool", "Manchester City", "Arsenal"],
        "correct_answer": "Manchester City"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Who holds the record for the most official goals scored in a single calendar year (91 goals in 2012)?",
        "options": ["Cristiano Ronaldo", "Pele", "Lionel Messi", "Gerd Müller"],
        "correct_answer": "Lionel Messi"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which country defeated England in the final of UEFA Euro 2020 at Wembley Stadium?",
        "options": ["Spain", "France", "Italy", "Portugal"],
        "correct_answer": "Italy"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which German club won 11 consecutive Bundesliga titles between 2013 and 2023?",
        "options": ["Borussia Dortmund", "RB Leipzig", "Bayern Munich", "Bayer Leverkusen"],
        "correct_answer": "Bayern Munich"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Who scored the winning extra-time goal for Spain against Netherlands in the 2010 World Cup final?",
        "options": ["Xavi", "David Villa", "Andrés Iniesta", "Fernando Torres"],
        "correct_answer": "Andrés Iniesta"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which European club plays its home matches at the iconic Santiago Bernabéu stadium?",
        "options": ["FC Barcelona", "Atletico Madrid", "Real Madrid", "Valencia"],
        "correct_answer": "Real Madrid"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Who holds the record as the overall all-time top goalscorer in English Premier League history (260 goals)?",
        "options": ["Wayne Rooney", "Harry Kane", "Alan Shearer", "Sergio Agüero"],
        "correct_answer": "Alan Shearer"
    },
    {
        "sport": "Football",
        "difficulty": "Easy",
        "question": "Which French club dominated Ligue 1 by winning 10 league titles between 2013 and 2024?",
        "options": ["Marseille", "Lyon", "Paris Saint-Germain", "Monaco"],
        "correct_answer": "Paris Saint-Germain"
    },

    # ==========================================
    # --- EASY CRICKET (15) ---
    # ==========================================
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which country won the inaugural ICC Men's T20 World Cup held in South Africa in 2007?",
        "options": ["Pakistan", "Australia", "India", "Sri Lanka"],
        "correct_answer": "India"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Who is the only batter in cricket history to score 100 international centuries?",
        "options": ["Ricky Ponting", "Virat Kohli", "Sachin Tendulkar", "Jacques Kallis"],
        "correct_answer": "Sachin Tendulkar"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which nation has won the most ICC Men's Cricket World Cup (ODI) titles (6 titles)?",
        "options": ["India", "West Indies", "Australia", "England"],
        "correct_answer": "Australia"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which IPL franchise shares the record for most IPL titles (5) alongside Mumbai Indians?",
        "options": ["Kolkata Knight Riders", "Royal Challengers Bengaluru", "Chennai Super Kings", "Rajasthan Royals"],
        "correct_answer": "Chennai Super Kings"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Who famously hit six 6s in an over off Stuart Broad during the 2007 T20 World Cup?",
        "options": ["MS Dhoni", "Virender Sehwag", "Yuvraj Singh", "Chris Gayle"],
        "correct_answer": "Yuvraj Singh"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which Sri Lankan legend holds the record for the most career wickets in Test match history (800 wickets)?",
        "options": ["Shane Warne", "Anil Kumble", "Muttiah Muralitharan", "James Anderson"],
        "correct_answer": "Muttiah Muralitharan"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Who captained India to its iconic first-ever ODI World Cup victory in 1983 at Lord's?",
        "options": ["Sunil Gavaskar", "Mohinder Amarnath", "Kapil Dev", "Ravi Shastri"],
        "correct_answer": "Kapil Dev"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which batter holds the record for the highest individual score in Test match cricket (400*)?",
        "options": ["Matthew Hayden", "Sir Donald Bradman", "Brian Lara", "Virender Sehwag"],
        "correct_answer": "Brian Lara"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which country won the 2023 ICC Men's Cricket World Cup hosted in India?",
        "options": ["India", "South Africa", "Australia", "New Zealand"],
        "correct_answer": "Australia"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Who was the captain of the Indian team that won the 2011 ICC ODI World Cup?",
        "options": ["Sachin Tendulkar", "Rahul Dravid", "MS Dhoni", "Virender Sehwag"],
        "correct_answer": "MS Dhoni"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which country won the 2024 ICC Men's T20 World Cup in Barbados by defeating South Africa in the final?",
        "options": ["England", "Australia", "India", "Pakistan"],
        "correct_answer": "India"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which batter holds the record for the highest individual score in Men's ODI cricket history (264 runs)?",
        "options": ["Martin Guptill", "Virender Sehwag", "Rohit Sharma", "Chris Gayle"],
        "correct_answer": "Rohit Sharma"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which iconic English venue is universally referred to as the 'Home of Cricket'?",
        "options": ["The Oval", "Edgbaston", "Lord's", "Headingley"],
        "correct_answer": "Lord's"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Who is the all-time leading run-scorer in Men's T20 World Cup history?",
        "options": ["Rohit Sharma", "Chris Gayle", "Virat Kohli", "Jos Buttler"],
        "correct_answer": "Virat Kohli"
    },
    {
        "sport": "Cricket",
        "difficulty": "Easy",
        "question": "Which Australian fast bowler holds the record for most wickets in ODI World Cup history (71 wickets)?",
        "options": ["Wasim Akram", "Lasith Malinga", "Glenn McGrath", "Mitchell Starc"],
        "correct_answer": "Glenn McGrath"
    },

    # ==========================================
    # --- EASY BASKETBALL (15) ---
    # ==========================================
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which NBA franchise won 6 NBA championships during the 1990s led by Michael Jordan?",
        "options": ["Los Angeles Lakers", "Boston Celtics", "Chicago Bulls", "Houston Rockets"],
        "correct_answer": "Chicago Bulls"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Who surpassed Kareem Abdul-Jabbar in 2023 to become the NBA's all-time leading regular season scorer?",
        "options": ["Kobe Bryant", "Stephen Curry", "LeBron James", "Kevin Durant"],
        "correct_answer": "LeBron James"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which two NBA franchises share the record for most NBA championships in history (17 each)?",
        "options": ["Bulls & Lakers", "Lakers & Celtics", "Celtics & Warriors", "Spurs & Lakers"],
        "correct_answer": "Lakers & Celtics"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Who holds the single-game NBA scoring record by scoring 100 points in a single game in 1962?",
        "options": ["Michael Jordan", "Kobe Bryant", "Wilt Chamberlain", "Elgin Baylor"],
        "correct_answer": "Wilt Chamberlain"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which Golden State Warriors star holds the record for most career 3-pointers made in NBA history?",
        "options": ["Ray Allen", "Reggie Miller", "Stephen Curry", "Klay Thompson"],
        "correct_answer": "Stephen Curry"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which team set the NBA regular season record by winning 73 games out of 82 in the 2015-16 season?",
        "options": ["Chicago Bulls", "San Antonio Spurs", "Golden State Warriors", "Miami Heat"],
        "correct_answer": "Golden State Warriors"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Who scored 81 points in a single NBA game against the Toronto Raptors in 2006?",
        "options": ["Michael Jordan", "LeBron James", "Kobe Bryant", "Allen Iverson"],
        "correct_answer": "Kobe Bryant"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which Greek superstar led the Milwaukee Bucks to the NBA championship in 2021?",
        "options": ["Nikola Jokić", "Luka Dončić", "Giannis Antetokounmpo", "Joel Embiid"],
        "correct_answer": "Giannis Antetokounmpo"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which player won NBA Finals MVP in 2006 after leading the Miami Heat back from a 0-2 deficit against Dallas?",
        "options": ["Shaquille O'Neal", "Alonzo Mourning", "Dwyane Wade", "Gary Payton"],
        "correct_answer": "Dwyane Wade"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which legendary center won 11 NBA championships during his 13-year career with the Boston Celtics?",
        "options": ["Wilt Chamberlain", "Kareem Abdul-Jabbar", "Bill Russell", "Larry Bird"],
        "correct_answer": "Bill Russell"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which NBA team based in Canada won their franchise's first NBA title in 2019 led by Kawhi Leonard?",
        "options": ["Vancouver Grizzlies", "Montreal Alliance", "Toronto Raptors", "Seattle SuperSonics"],
        "correct_answer": "Toronto Raptors"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Who won the NBA MVP award for two consecutive seasons in 2021 and 2022 with the Denver Nuggets?",
        "options": ["Giannis Antetokounmpo", "Joel Embiid", "Nikola Jokić", "James Harden"],
        "correct_answer": "Nikola Jokić"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which franchise won the 2024 NBA Championship by defeating the Dallas Mavericks 4-1 in the Finals?",
        "options": ["Denver Nuggets", "Golden State Warriors", "Boston Celtics", "Miami Heat"],
        "correct_answer": "Boston Celtics"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which player was drafted #1 overall by the Cleveland Cavaliers in the famous 2003 NBA Draft?",
        "options": ["Carmelo Anthony", "Dwyane Wade", "LeBron James", "Chris Bosh"],
        "correct_answer": "LeBron James"
    },
    {
        "sport": "Basketball",
        "difficulty": "Easy",
        "question": "Which NBA team won three consecutive titles ('Three-peat') from 2000 to 2002 led by Shaq and Kobe?",
        "options": ["Chicago Bulls", "San Antonio Spurs", "Los Angeles Lakers", "Miami Heat"],
        "correct_answer": "Los Angeles Lakers"
    },

    # ==========================================
    # --- EASY TENNIS (15) ---
    # ==========================================
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which male tennis player holds the record for the most Grand Slam singles titles in history (24 titles)?",
        "options": ["Rafael Nadal", "Roger Federer", "Novak Djokovic", "Pete Sampras"],
        "correct_answer": "Novak Djokovic"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Who earned the nickname 'King of Clay' after winning an unmatched 14 French Open singles titles?",
        "options": ["Novak Djokovic", "Roger Federer", "Rafael Nadal", "Björn Borg"],
        "correct_answer": "Rafael Nadal"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which American female tennis legend won 23 Grand Slam singles titles during the Open Era?",
        "options": ["Steffi Graf", "Martina Navratilova", "Serena Williams", "Venus Williams"],
        "correct_answer": "Serena Williams"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which Swiss legend won 20 Grand Slam singles titles, including a record 8 Wimbledon men's singles titles?",
        "options": ["Stan Wawrinka", "Novak Djokovic", "Roger Federer", "Andy Murray"],
        "correct_answer": "Roger Federer"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which Grand Slam tournament is played annually on red clay courts at Roland Garros in Paris?",
        "options": ["Wimbledon", "Australian Open", "French Open", "US Open"],
        "correct_answer": "French Open"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Who became the first British man in 77 years to win the Wimbledon singles title when he won in 2013?",
        "options": ["Tim Henman", "Greg Rusedski", "Andy Murray", "Cameron Norrie"],
        "correct_answer": "Andy Murray"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which Grand Slam tournament is played on grass courts at the All England Club in London?",
        "options": ["US Open", "Australian Open", "Wimbledon", "French Open"],
        "correct_answer": "Wimbledon"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Who won her first Grand Slam title at the 2018 US Open by defeating Serena Williams in the final?",
        "options": ["Coco Gauff", "Iga Świątek", "Naomi Osaka", "Emma Raducanu"],
        "correct_answer": "Naomi Osaka"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which Spanish star won his first Grand Slam at the 2022 US Open and reached World No. 1 at age 19?",
        "options": ["Jannik Sinner", "Daniil Medvedev", "Carlos Alcaraz", "Holger Rune"],
        "correct_answer": "Carlos Alcaraz"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which Grand Slam tournament takes place annually in January at Melbourne Park?",
        "options": ["US Open", "Wimbledon", "Australian Open", "French Open"],
        "correct_answer": "Australian Open"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Who won the 2021 US Open women's singles title as an 18-year-old qualifier without dropping a set?",
        "options": ["Leylah Fernandez", "Coco Gauff", "Emma Raducanu", "Bianca Andreescu"],
        "correct_answer": "Emma Raducanu"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which Polish superstar won four French Open titles between 2020 and 2024?",
        "options": ["Aryna Sabalenka", "Elena Rybakina", "Iga Świątek", "Ons Jabeur"],
        "correct_answer": "Iga Świątek"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Who holds the record for the most Wimbledon women's singles titles in history (9 titles)?",
        "options": ["Steffi Graf", "Serena Williams", "Martina Navratilova", "Chris Evert"],
        "correct_answer": "Martina Navratilova"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Which American male legend held the record of 14 Grand Slam singles titles before Roger Federer broke it?",
        "options": ["Andre Agassi", "John McEnroe", "Pete Sampras", "Jimmy Connors"],
        "correct_answer": "Pete Sampras"
    },
    {
        "sport": "Tennis",
        "difficulty": "Easy",
        "question": "Who is the only male tennis player to win all four Grand Slams at least three times each?",
        "options": ["Rafael Nadal", "Roger Federer", "Novak Djokovic", "Rod Laver"],
        "correct_answer": "Novak Djokovic"
    },

    # ==========================================
    # --- MEDIUM FOOTBALL (15) ---
    # ==========================================
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Who provided the cross for Mario Götze's 113th-minute winning goal for Germany in the 2014 World Cup final?",
        "options": ["Thomas Müller", "Toni Kroos", "André Schürrle", "Bastian Schweinsteiger"],
        "correct_answer": "André Schürrle"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "What was the score at half-time in the legendary 2005 UEFA Champions League final between AC Milan and Liverpool?",
        "options": ["2-0", "3-0", "3-1", "2-1"],
        "correct_answer": "3-0"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Who was head-butted by Zinedine Zidane in extra time of the 2006 FIFA World Cup final?",
        "options": ["Fabio Cannavaro", "Gianluca Zambrotta", "Marco Materazzi", "Gennaro Gattuso"],
        "correct_answer": "Marco Materazzi"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Which underdogs pulled off one of football's greatest shocks by winning UEFA Euro 2004?",
        "options": ["Portugal", "Czech Republic", "Greece", "Denmark"],
        "correct_answer": "Greece"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Who was the first defender in football history to win the Ballon d'Or twice (1972 & 1976)?",
        "options": ["Fabio Cannavaro", "Paolo Maldini", "Franz Beckenbauer", "Franco Baresi"],
        "correct_answer": "Franz Beckenbauer"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Which African country became the first in history to reach a FIFA World Cup semi-final at Qatar 2022?",
        "options": ["Cameroon", "Senegal", "Morocco", "Ghana"],
        "correct_answer": "Morocco"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Which club holds the record for winning the most UEFA Europa League (formerly UEFA Cup) titles (7 titles)?",
        "options": ["Atletico Madrid", "Villarreal", "Sevilla", "Valencia"],
        "correct_answer": "Sevilla"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Which manager won UEFA Champions League titles with both FC Porto (2004) and Inter Milan (2010)?",
        "options": ["Carlo Ancelotti", "Pep Guardiola", "José Mourinho", "Rafa Benítez"],
        "correct_answer": "José Mourinho"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Who won the Ballon d'Or in 2007, the last player to win it before the era of Messi and Ronaldo dominance?",
        "options": ["Cristiano Ronaldo", "Lionel Messi", "Kaká", "Ronaldinho"],
        "correct_answer": "Kaká"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Which Italian club did Andrea Pirlo join on a free transfer in 2011 after leaving AC Milan?",
        "options": ["Inter Milan", "Roma", "Juventus", "Fiorentina"],
        "correct_answer": "Juventus"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Who was the manager of Arsenal during their famous 49-game unbeaten Premier League streak?",
        "options": ["Sir Alex Ferguson", "José Mourinho", "Arsène Wenger", "Claudio Ranieri"],
        "correct_answer": "Arsène Wenger"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Which defender won the 2006 Ballon d'Or after captaining Italy to FIFA World Cup victory?",
        "options": ["Gianluigi Buffon", "Andrea Pirlo", "Fabio Cannavaro", "Zinedine Zidane"],
        "correct_answer": "Fabio Cannavaro"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Who scored FC Barcelona's dramatic 93rd-minute equalizer against Chelsea at Stamford Bridge in the 2009 UCL semi-final?",
        "options": ["Lionel Messi", "Samuel Eto'o", "Andrés Iniesta", "Xavi"],
        "correct_answer": "Andrés Iniesta"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Which nation won the inaugural UEFA European Championship (Euro) held in 1960?",
        "options": ["France", "Yugoslavia", "Soviet Union", "Spain"],
        "correct_answer": "Soviet Union"
    },
    {
        "sport": "Football",
        "difficulty": "Medium",
        "question": "Who scored both goals for Inter Milan in their 2-0 win over Bayern Munich in the 2010 UCL final?",
        "options": ["Samuel Eto'o", "Wesley Sneijder", "Diego Milito", "Goran Pandev"],
        "correct_answer": "Diego Milito"
    },

    # ==========================================
    # --- MEDIUM CRICKET (15) ---
    # ==========================================
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Against which country did Sachin Tendulkar make his international Test debut in 1989 at age 16?",
        "options": ["Australia", "England", "Pakistan", "West Indies"],
        "correct_answer": "Pakistan"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Against which team did Anil Kumble take all 10 wickets in a single Test match innings in 1999 at Delhi?",
        "options": ["Australia", "England", "Pakistan", "Sri Lanka"],
        "correct_answer": "Pakistan"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Who holds the record for the fastest century in Men's ODI history, scored off just 31 balls in 2015?",
        "options": ["Shahid Afridi", "Corey Anderson", "AB de Villiers", "Jos Buttler"],
        "correct_answer": "AB de Villiers"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Which Indian bowler took the first-ever hat-trick in Cricket World Cup history during the 1987 tournament?",
        "options": ["Kapil Dev", "Javagal Srinath", "Chetan Sharma", "Maninder Singh"],
        "correct_answer": "Chetan Sharma"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Who captained Australia to back-to-back undefeated ODI World Cup titles in 2003 and 2007?",
        "options": ["Steve Waugh", "Allan Border", "Ricky Ponting", "Michael Clarke"],
        "correct_answer": "Ricky Ponting"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Who scored a legendary 175* against Zimbabwe in the 1983 World Cup when India was reeling at 17/5?",
        "options": ["Sunil Gavaskar", "Mohinder Amarnath", "Kapil Dev", "Yashpal Sharma"],
        "correct_answer": "Kapil Dev"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Which Australian batter scored 140* off 121 balls against India in the 2003 ODI World Cup final?",
        "options": ["Adam Gilchrist", "Matthew Hayden", "Ricky Ponting", "Damien Martyn"],
        "correct_answer": "Ricky Ponting"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Who holds the record for most dismissals by a wicketkeeper across all international cricket formats (998)?",
        "options": ["Adam Gilchrist", "MS Dhoni", "Mark Boucher", "Kumar Sangakkara"],
        "correct_answer": "Mark Boucher"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Which venue in Melbourne hosted the first-ever official Test match played in March 1877?",
        "options": ["Sydney Cricket Ground", "Lord's", "Melbourne Cricket Ground (MCG)", "The Oval"],
        "correct_answer": "Melbourne Cricket Ground (MCG)"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Who was the bowler that bowled the final over in India's victory over Pakistan in the 2007 T20 World Cup final?",
        "options": ["Sreesanth", "RP Singh", "Joginder Sharma", "Irfan Pathan"],
        "correct_answer": "Joginder Sharma"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Which batter hit the highest individual score in Test history by an Indian (319 vs South Africa in 2008)?",
        "options": ["Sachin Tendulkar", "Rahul Dravid", "Virender Sehwag", "Karun Nair"],
        "correct_answer": "Virender Sehwag"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Which legendary West Indies fast bowler pair was famously known as the 'Fire in Babylon' duo?",
        "options": ["Ambrose & Walsh", "Holding & Roberts", "Marshall & Garner", "Croft & Garner"],
        "correct_answer": "Ambrose & Walsh"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Who was named Player of the Tournament at the 2011 ICC Men's ODI World Cup?",
        "options": ["MS Dhoni", "Sachin Tendulkar", "Yuvraj Singh", "Zaheer Khan"],
        "correct_answer": "Yuvraj Singh"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Who was the first bowler to take 500 Test wickets in cricket history (achieved in 2001)?",
        "options": ["Shane Warne", "Muttiah Muralitharan", "Courtney Walsh", "Kapil Dev"],
        "correct_answer": "Courtney Walsh"
    },
    {
        "sport": "Cricket",
        "difficulty": "Medium",
        "question": "Which country won the 2013 ICC Champions Trophy under MS Dhoni by defeating England in the final?",
        "options": ["Sri Lanka", "South Africa", "India", "England"],
        "correct_answer": "India"
    },

    # ==========================================
    # --- MEDIUM BASKETBALL (15) ---
    # ==========================================
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Who was the first unanimous MVP selection in NBA history during the 2015-16 season?",
        "options": ["Michael Jordan", "LeBron James", "Stephen Curry", "Shaquille O'Neal"],
        "correct_answer": "Stephen Curry"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which Houston Rockets player famously scored 13 points in 35 seconds to beat San Antonio in 2004?",
        "options": ["Kobe Bryant", "Reggie Miller", "Tracy McGrady", "James Harden"],
        "correct_answer": "Tracy McGrady"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Who won NBA Finals MVP in 2004 after the Detroit Pistons upset the Los Angeles Lakers in 5 games?",
        "options": ["Ben Wallace", "Rasheed Wallace", "Chauncey Billups", "Richard Hamilton"],
        "correct_answer": "Chauncey Billups"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Who broke Oscar Robertson's long-standing record for the most career triple-doubles in NBA history?",
        "options": ["LeBron James", "Nikola Jokić", "Russell Westbrook", "Magic Johnson"],
        "correct_answer": "Russell Westbrook"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which player won Finals MVP in 2014 with the San Antonio Spurs after guarding LeBron James?",
        "options": ["Tim Duncan", "Tony Parker", "Kawhi Leonard", "Manu Ginóbili"],
        "correct_answer": "Kawhi Leonard"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Who scored 60 points in his final career NBA game before retiring in April 2016?",
        "options": ["Dwyane Wade", "Dirk Nowitzki", "Kobe Bryant", "Paul Pierce"],
        "correct_answer": "Kobe Bryant"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which NBA player hit the famous clutch 3-pointer in Game 6 of the 2013 NBA Finals to save Miami Heat?",
        "options": ["Dwyane Wade", "LeBron James", "Ray Allen", "Chris Bosh"],
        "correct_answer": "Ray Allen"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which NBA team completed the only 3-1 series comeback in NBA Finals history (2016)?",
        "options": ["Golden State Warriors", "Miami Heat", "Cleveland Cavaliers", "Toronto Raptors"],
        "correct_answer": "Cleveland Cavaliers"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Who was the first non-American player to be selected #1 overall in the NBA Draft (1984)?",
        "options": ["Patrick Ewing", "Yao Ming", "Hakeem Olajuwon", "Tim Duncan"],
        "correct_answer": "Hakeem Olajuwon"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which head coach holds the record for most total coaching wins in regular season NBA history?",
        "options": ["Don Nelson", "Lenny Wilkens", "Gregg Popovich", "Phil Jackson"],
        "correct_answer": "Gregg Popovich"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Who won back-to-back NBA MVP awards in 2005 and 2006 with the Phoenix Suns?",
        "options": ["Jason Kidd", "Shaquille O'Neal", "Steve Nash", "Kobe Bryant"],
        "correct_answer": "Steve Nash"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which player won regular season MVP, Finals MVP, and Defensive Player of the Year in 1994?",
        "options": ["Michael Jordan", "David Robinson", "Hakeem Olajuwon", "Shaquille O'Neal"],
        "correct_answer": "Hakeem Olajuwon"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which NBA franchise retired the number 23 jersey in honor of Michael Jordan, despite him never playing for them?",
        "options": ["Orlando Magic", "Brooklyn Nets", "Miami Heat", "Charlotte Hornets"],
        "correct_answer": "Miami Heat"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "In what NBA season was the three-point field goal officially introduced to the league?",
        "options": ["1976-77", "1978-79", "1979-80", "1984-85"],
        "correct_answer": "1979-80"
    },
    {
        "sport": "Basketball",
        "difficulty": "Medium",
        "question": "Which franchise relocated from Seattle in 2008 and was rebranded as the Oklahoma City Thunder?",
        "options": ["Vancouver Grizzlies", "New Orleans Hornets", "Seattle SuperSonics", "Charlotte Bobcats"],
        "correct_answer": "Seattle SuperSonics"
    },

    # ==========================================
    # --- MEDIUM TENNIS (15) ---
    # ==========================================
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who is the only tennis player in history to achieve a single-calendar-year 'Golden Slam' (all 4 Slams + Olympic Gold in 1988)?",
        "options": ["Serena Williams", "Martina Navratilova", "Steffi Graf", "Monica Seles"],
        "correct_answer": "Steffi Graf"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who became the first unseeded woman in the Open Era to win the Wimbledon singles title (2023)?",
        "options": ["Ons Jabeur", "Barbora Krejčíková", "Markéta Vondroušová", "Elena Rybakina"],
        "correct_answer": "Markéta Vondroušová"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Which player defeated Roger Federer in the 2009 US Open final, snapping Federer's 5-year streak of US Open titles?",
        "options": ["Andy Murray", "Novak Djokovic", "Juan Martín del Potro", "Stan Wawrinka"],
        "correct_answer": "Juan Martín del Potro"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Which player holds the Open Era record for most consecutive weeks ranked World No. 1 (237 weeks)?",
        "options": ["Novak Djokovic", "Pete Sampras", "Roger Federer", "Jimmy Connors"],
        "correct_answer": "Roger Federer"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who became the youngest male Grand Slam singles champion in history by winning the 1989 French Open at age 17?",
        "options": ["Boris Becker", "Mats Wilander", "Michael Chang", "Lleyton Hewitt"],
        "correct_answer": "Michael Chang"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "What year did the 'Open Era' of tennis officially begin, allowing professionals to compete in Grand Slams?",
        "options": ["1965", "1967", "1968", "1970"],
        "correct_answer": "1968"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who broke Pete Sampras's record of 14 Grand Slam singles titles by winning his 15th at Wimbledon 2009?",
        "options": ["Rafael Nadal", "Novak Djokovic", "Roger Federer", "Andy Roddick"],
        "correct_answer": "Roger Federer"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who was the last male tennis player from Australia to win a Grand Slam singles title (2002 Wimbledon)?",
        "options": ["Patrick Rafter", "Mark Philippoussis", "Lleyton Hewitt", "Nick Kyrgios"],
        "correct_answer": "Lleyton Hewitt"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Which Swiss player won three Grand Slam singles titles (2014 Aus Open, 2015 French Open, 2016 US Open)?",
        "options": ["Roger Federer", "Marc Rosset", "Stan Wawrinka", "Heinz Günthardt"],
        "correct_answer": "Stan Wawrinka"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who won the 2020 US Open men's singles title after coming back from two sets down against Alexander Zverev?",
        "options": ["Daniil Medvedev", "Stefanos Tsitsipas", "Dominic Thiem", "Pablo Carreño Busta"],
        "correct_answer": "Dominic Thiem"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who won the 2014 US Open Men's Singles title by defeating Kei Nishikori in the final?",
        "options": ["Milos Raonic", "Grigor Dimitrov", "Marin Čilić", "Tomáš Berdych"],
        "correct_answer": "Marin Čilić"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Which legend won 8 Grand Slam titles and achieved a Career Grand Slam wearing neon gear in the 1990s?",
        "options": ["Pete Sampras", "Jim Courier", "Andre Agassi", "Michael Chang"],
        "correct_answer": "Andre Agassi"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Which ATP Masters 1000 tournament is popularly referred to as the 'Fifth Grand Slam'?",
        "options": ["Miami Open", "Monte-Carlo Masters", "Indian Wells Masters", "Cincinnati Masters"],
        "correct_answer": "Indian Wells Masters"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who won three Grand Slam singles titles in 2016 (Australian Open & US Open) and reached World No. 1?",
        "options": ["Garbine Muguruza", "Simona Halep", "Angelique Kerber", "Victoria Azarenka"],
        "correct_answer": "Angelique Kerber"
    },
    {
        "sport": "Tennis",
        "difficulty": "Medium",
        "question": "Who defeated Roger Federer in the epic 2008 Wimbledon men's singles final, widely called the greatest match ever?",
        "options": ["Novak Djokovic", "Andy Murray", "Rafael Nadal", "Andy Roddick"],
        "correct_answer": "Rafael Nadal"
    },

    # ==========================================
    # --- HARD FOOTBALL (15) --- (EXPERT TRIVIA)
    # ==========================================
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who scored the only goal in the UEFA Euro 2008 final between Spain and Germany?",
        "options": ["David Villa", "Xavi", "Fernando Torres", "Andrés Iniesta"],
        "correct_answer": "Fernando Torres"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who holds the record for the fastest hat-trick in Premier League history (2 minutes 56 seconds in 2015)?",
        "options": ["Robbie Fowler", "Sadio Mané", "Sergio Agüero", "Jermain Defoe"],
        "correct_answer": "Sadio Mané"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who was the manager of Greece when they won the UEFA Euro 2004 tournament?",
        "options": ["Otto Rehhagel", "Guus Hiddink", "Lars Lagerbäck", "Karel Brückner"],
        "correct_answer": "Otto Rehhagel"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who scored the 85th-minute winning goal for Ajax against AC Milan in the 1995 Champions League final?",
        "options": ["Jari Litmanen", "Marc Overmars", "Patrick Kluivert", "Clarence Seedorf"],
        "correct_answer": "Patrick Kluivert"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who was the inaugural winner of the FIFA Puskás Award in 2009 for his 40-yard strike against FC Porto?",
        "options": ["Neymar", "Zlatan Ibrahimović", "Cristiano Ronaldo", "Wayne Rooney"],
        "correct_answer": "Cristiano Ronaldo"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Which goalkeeper holds the all-time record for most clean sheets in Premier League history (202 clean sheets)?",
        "options": ["David James", "Edwin van der Sar", "Petr Čech", "Mark Schwarzer"],
        "correct_answer": "Petr Čech"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who is the only player in football history to win the UEFA Champions League with three different clubs?",
        "options": ["Cristiano Ronaldo", "Samuel Eto'o", "Clarence Seedorf", "Toni Kroos"],
        "correct_answer": "Clarence Seedorf"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Which African nation won the gold medal in men's football at the 1996 Atlanta Olympics, beating Brazil and Argentina?",
        "options": ["Cameroon", "Nigeria", "Ghana", "South Africa"],
        "correct_answer": "Nigeria"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who scored the extra-time winner for Borussia Dortmund in the 1997 UCL final against Juventus with his very first touch after coming on?",
        "options": ["Karl-Heinz Riedle", "Andreas Möller", "Lars Ricken", "Stephane Chapuisat"],
        "correct_answer": "Lars Ricken"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who was the top goalscorer (Golden Boot winner on tiebreakers) at the 2010 FIFA World Cup in South Africa?",
        "options": ["Wesley Sneijder", "David Villa", "Thomas Müller", "Diego Forlán"],
        "correct_answer": "Thomas Müller"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who scored FC Porto's opening goal in the 2004 UEFA Champions League final against AS Monaco?",
        "options": ["Deco", "Maniche", "Carlos Alberto", "Dmitri Alenichev"],
        "correct_answer": "Carlos Alberto"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Which Eastern European club won the 1991 European Cup (Champions League) by defeating Marseille on penalties?",
        "options": ["Steaua București", "Partizan Belgrade", "Red Star Belgrade", "Dynamo Kyiv"],
        "correct_answer": "Red Star Belgrade"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who scored the winning goal for Portugal against France in extra time of the UEFA Euro 2016 final?",
        "options": ["Nani", "Ricardo Quaresma", "Éder", "Cristiano Ronaldo"],
        "correct_answer": "Éder"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Who was the Liberian icon who became the first and only African player to win the Ballon d'Or in 1995?",
        "options": ["Didier Drogba", "Samuel Eto'o", "George Weah", "Roger Milla"],
        "correct_answer": "George Weah"
    },
    {
        "sport": "Football",
        "difficulty": "Hard",
        "question": "Which English club won back-to-back European Cups in 1979 and 1980 under manager Brian Clough?",
        "options": ["Aston Villa", "Leeds United", "Nottingham Forest", "Celtic"],
        "correct_answer": "Nottingham Forest"
    },

    # ==========================================
    # --- HARD CRICKET (15) --- (EXPERT TRIVIA)
    # ==========================================
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who was the bowler bowling to Carlos Brathwaite when he hit 4 consecutive sixes to win the 2016 T20 World Cup?",
        "options": ["Chris Jordan", "David Willey", "Ben Stokes", "Mark Wood"],
        "correct_answer": "Ben Stokes"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who was the bowler when Netherlands' Daan van Bunge was hit for 6 sixes in an over by Herschelle Gibbs in 2007?",
        "options": ["Peter Borren", "Daan van Bunge", "Ryan ten Doeschte", "Paul van Meekeren"],
        "correct_answer": "Daan van Bunge"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who was named Player of the Match in the 1999 ICC Cricket World Cup Final after taking 4 for 33 against Pakistan?",
        "options": ["Glenn McGrath", "Damien Fleming", "Shane Warne", "Tom Moody"],
        "correct_answer": "Shane Warne"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who was the first bowler in cricket history to take a hat-trick in T20 International cricket (2007 vs Bangladesh)?",
        "options": ["Umar Gul", "Lasith Malinga", "Brett Lee", "Jacob Oram"],
        "correct_answer": "Brett Lee"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who scored a century on Test debut for India against Australia in 2013 off just 85 balls (fastest debut Test 100)?",
        "options": ["Murali Vijay", "Cheteshwar Pujara", "Shikhar Dhawan", "Prithvi Shaw"],
        "correct_answer": "Shikhar Dhawan"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Against which team did Sunil Gavaskar score his 10,000th Test run in 1987, becoming the first batter to reach the milestone?",
        "options": ["Australia", "England", "Pakistan", "West Indies"],
        "correct_answer": "Pakistan"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Which non-wicketkeeper holds the record for most catches in Test match cricket history (210 catches)?",
        "options": ["Mahela Jayawardene", "Ricky Ponting", "Rahul Dravid", "Jacques Kallis"],
        "correct_answer": "Rahul Dravid"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who caught Wasim Akram to complete Anil Kumble's legendary 10-wicket Test innings in 1999 at Delhi?",
        "options": ["Sourav Ganguly", "Sachin Tendulkar", "VVS Laxman", "Sadagoppan Ramesh"],
        "correct_answer": "VVS Laxman"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who took the wicket of Sachin Tendulkar in the 1st over of the 2003 ODI World Cup final?",
        "options": ["Brett Lee", "Jason Gillespie", "Glenn McGrath", "Andy Bichel"],
        "correct_answer": "Glenn McGrath"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who holds the record for the highest individual score in an ICC T20 World Cup match (123 off 58 balls in 2012)?",
        "options": ["Chris Gayle", "Alex Hales", "Brendon McCullum", "Mahela Jayawardene"],
        "correct_answer": "Brendon McCullum"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who was the leading run-scorer of the 2019 ICC Men's Cricket World Cup with 648 runs?",
        "options": ["David Warner", "Shakib Al Hasan", "Rohit Sharma", "Kane Williamson"],
        "correct_answer": "Rohit Sharma"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who was the first cricketer in history to be given out by a TV third umpire in an international match (1992)?",
        "options": ["Rahul Dravid", "Brian Lara", "Sachin Tendulkar", "Inzamam-ul-Haq"],
        "correct_answer": "Sachin Tendulkar"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who shared the highest wicket-taker award (21 wickets) with Zaheer Khan at the 2011 ICC Cricket World Cup?",
        "options": ["Yuvraj Singh", "Muttiah Muralitharan", "Shahid Afridi", "Lasith Malinga"],
        "correct_answer": "Shahid Afridi"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who holds the record for the fastest 50 in T20 International history (off just 9 balls against Mongolia in 2023)?",
        "options": ["Yuvraj Singh", "Abhishek Sharma", "Dipendra Singh Airee", "Marcus Stoinis"],
        "correct_answer": "Dipendra Singh Airee"
    },
    {
        "sport": "Cricket",
        "difficulty": "Hard",
        "question": "Who scored 175 runs off 143 balls for Australia in the famous 434 vs 438 ODI match against South Africa in 2006?",
        "options": ["Adam Gilchrist", "Matthew Hayden", "Ricky Ponting", "Michael Hussey"],
        "correct_answer": "Ricky Ponting"
    },

    # ==========================================
    # --- HARD BASKETBALL (15) --- (EXPERT TRIVIA)
    # ==========================================
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Which assistant coach under Phil Jackson is famous for developing and refining the 'Triangle Offense'?",
        "options": ["Red Holzman", "Tex Winter", "Chuck Daly", "Larry Brown"],
        "correct_answer": "Tex Winter"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Which NBA player holds the single-season record for most technical fouls (41 technicals in 2000-01)?",
        "options": ["Dennis Rodman", "Ron Artest", "Rasheed Wallace", "Draymond Green"],
        "correct_answer": "Rasheed Wallace"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Which franchise selected Kobe Bryant with the 13th overall pick in the 1996 NBA Draft before trading him?",
        "options": ["New Jersey Nets", "Sacramento Kings", "Charlotte Hornets", "Philadelphia 76ers"],
        "correct_answer": "Charlotte Hornets"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who was selected #2 overall in the famous 2003 NBA Draft right after LeBron James (#1 pick)?",
        "options": ["Carmelo Anthony", "Dwyane Wade", "Darko Miličić", "Chris Bosh"],
        "correct_answer": "Darko Miličić"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who won the NBA Finals MVP award in 2015 for his crucial defensive work guarding LeBron James?",
        "options": ["Stephen Curry", "Klay Thompson", "Andre Iguodala", "Draymond Green"],
        "correct_answer": "Andre Iguodala"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who is the only player in NBA history to win Finals MVP while playing for the losing team (1969 Finals)?",
        "options": ["Wilt Chamberlain", "Elgin Baylor", "Jerry West", "John Havlicek"],
        "correct_answer": "Jerry West"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who was the head coach of the 'Bad Boys' Detroit Pistons during their back-to-back NBA championships (1989 & 1990)?",
        "options": ["Pat Riley", "Larry Brown", "Chuck Daly", "Doug Collins"],
        "correct_answer": "Chuck Daly"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who hit the famous 4-bounce Game 7 buzzer-beater for Toronto against Philadelphia in the 2019 playoffs?",
        "options": ["Kyle Lowry", "Pascal Siakam", "Kawhi Leonard", "Fred VanVleet"],
        "correct_answer": "Kawhi Leonard"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who won the 1993 NBA Regular Season MVP award, interrupting Michael Jordan's streak?",
        "options": ["Hakeem Olajuwon", "David Robinson", "Charles Barkley", "Karl Malone"],
        "correct_answer": "Charles Barkley"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who holds the record for most missed field goals in NBA regular season history (14,481 missed shots)?",
        "options": ["LeBron James", "John Havlicek", "Kobe Bryant", "Elvin Hayes"],
        "correct_answer": "Kobe Bryant"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Which player scored 70 points against the Boston Celtics in March 2017 at just 20 years old?",
        "options": ["Kyrie Irving", "Donovan Mitchell", "Devin Booker", "Jayson Tatum"],
        "correct_answer": "Devin Booker"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who was the head coach of the Dallas Mavericks when they defeated the Miami Heat 'Big Three' in the 2011 NBA Finals?",
        "options": ["Avery Johnson", "Don Nelson", "Rick Carlisle", "Jason Kidd"],
        "correct_answer": "Rick Carlisle"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Before the 24-second shot clock was introduced in 1954, what was the lowest-scoring game score in NBA history?",
        "options": ["24-23", "31-30", "19-18", "38-37"],
        "correct_answer": "19-18"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who recorded a historic 60-point, 21-rebound, 10-assist triple-double in an NBA game in December 2022?",
        "options": ["Nikola Jokić", "Russell Westbrook", "Luka Dončić", "Giannis Antetokounmpo"],
        "correct_answer": "Luka Dončić"
    },
    {
        "sport": "Basketball",
        "difficulty": "Hard",
        "question": "Who holds the NBA record for most assists in a single NBA Finals game (21 assists in 1984)?",
        "options": ["John Stockton", "Isiah Thomas", "Magic Johnson", "Bob Cousy"],
        "correct_answer": "Magic Johnson"
    },

    # ==========================================
    # --- HARD TENNIS (15) --- (EXPERT TRIVIA)
    # ==========================================
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who was the coach who guided Novak Djokovic to 6 Grand Slam titles during their partnership from 2013 to 2016?",
        "options": ["Marian Vajda", "Andre Agassi", "Boris Becker", "Goran Ivanišević"],
        "correct_answer": "Boris Becker"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who won the 2009 French Open men's singles title after Robin Söderling famously shocked Rafael Nadal in the 4th round?",
        "options": ["Novak Djokovic", "Andy Murray", "Roger Federer", "Juan Martín del Potro"],
        "correct_answer": "Roger Federer"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who holds the record for the highest serve speed ever officially recorded in professional tennis (163.7 mph / 263.4 km/h)?",
        "options": ["John Isner", "Ivo Karlović", "Samuel Groth", "Andy Roddick"],
        "correct_answer": "Samuel Groth"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who saved two match points against Roger Federer in the 2011 US Open semi-final with an iconic forehand return winner?",
        "options": ["Rafael Nadal", "Andy Murray", "Novak Djokovic", "Stan Wawrinka"],
        "correct_answer": "Novak Djokovic"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who defeated Serena Williams in the 2015 US Open semi-finals, stopping Serena's bid for a Calendar Grand Slam?",
        "options": ["Flavia Pennetta", "Victoria Azarenka", "Roberta Vinci", "Simona Halep"],
        "correct_answer": "Roberta Vinci"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who was the last Australian woman to win the Wimbledon singles title before Ashleigh Barty won in 2021?",
        "options": ["Samantha Stosur", "Margaret Court", "Evonne Goolagong Cawley", "Wendy Turnbull"],
        "correct_answer": "Evonne Goolagong Cawley"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Which male tennis player lost 11 Grand Slam singles finals during his career (tied with Andy Murray's 8 losses)?",
        "options": ["Pete Sampras", "Björn Borg", "Ivan Lendl", "Jimmy Connors"],
        "correct_answer": "Ivan Lendl"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who was the first male player outside the 'Big Four' (Federer, Nadal, Djokovic, Murray) to reach World No. 1 since 2004?",
        "options": ["Dominic Thiem", "Alexander Zverev", "Daniil Medvedev", "Carlos Alcaraz"],
        "correct_answer": "Daniil Medvedev"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who holds the all-time record for winning the most ATP Masters 1000 titles in history (40 titles)?",
        "options": ["Rafael Nadal", "Roger Federer", "Novak Djokovic", "Pete Sampras"],
        "correct_answer": "Novak Djokovic"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who was the chair umpire involved in the controversial 2018 US Open Women's Final between Serena Williams and Naomi Osaka?",
        "options": ["Mohamed Lahyani", "Eva Asderaki-Moore", "Carlos Ramos", "Pascal Maria"],
        "correct_answer": "Carlos Ramos"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Which two players contested the longest match in tennis history (11 hours 5 minutes across 3 days) at Wimbledon 2010?",
        "options": ["Federer & Roddick", "Djokovic & Nadal", "John Isner & Nicolas Mahut", "Anderson & Isner"],
        "correct_answer": "John Isner & Nicolas Mahut"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who won the 2015 French Open men's singles title, beating Novak Djokovic in the final wearing distinctive plaid shorts?",
        "options": ["Roger Federer", "Rafael Nadal", "Stan Wawrinka", "David Ferrer"],
        "correct_answer": "Stan Wawrinka"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who was the last male player before Carlos Alcaraz to win his first Grand Slam title as a teenager (2005 French Open)?",
        "options": ["Novak Djokovic", "Roger Federer", "Rafael Nadal", "Lleyton Hewitt"],
        "correct_answer": "Rafael Nadal"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who won the Gold Medal in Men's Singles at the 2016 Rio Olympic Games?",
        "options": ["Juan Martín del Potro", "Rafael Nadal", "Andy Murray", "Novak Djokovic"],
        "correct_answer": "Andy Murray"
    },
    {
        "sport": "Tennis",
        "difficulty": "Hard",
        "question": "Who was the only wildcard entry in Wimbledon history to win the Men's Singles title (2001)?",
        "options": ["Tim Henman", "Patrick Rafter", "Goran Ivanišević", "Richard Krajicek"],
        "correct_answer": "Goran Ivanišević"
    }
]

# Separate by difficulty
easy_qs = [q for q in questions_data if q["difficulty"] == "Easy"]
medium_qs = [q for q in questions_data if q["difficulty"] == "Medium"]
hard_qs = [q for q in questions_data if q["difficulty"] == "Hard"]

# Shuffle within difficulty to interleave sports nicely
random.shuffle(easy_qs)
random.shuffle(medium_qs)
random.shuffle(hard_qs)

final_180 = []
audit_lines = []
qid = 1

for diff_pool in [easy_qs, medium_qs, hard_qs]:
    for item in diff_pool:
        correct_ans = item["correct_answer"]
        opts = list(item["options"])
        random.shuffle(opts)
        correct_idx = opts.index(correct_ans)
        
        q_obj = {
            "id": f"Q{qid:03d}",
            "sport": item["sport"],
            "difficulty": item["difficulty"],
            "question": item["question"],
            "options": opts,
            "correct": correct_idx
        }
        final_180.append(q_obj)
        
        audit_lines.append(
            f"Q{qid:03d} [{item['sport']}|{item['difficulty']}] {item['question']}\n"
            f"      Options: {opts}\n"
            f"      Correct: Index {correct_idx} -> '{correct_ans}'\n"
        )
        qid += 1

output_json_path = r"d:\Case\questions_180.json"
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(final_180, f, indent=2, ensure_ascii=False)

output_audit_path = r"d:\Case\question_options_audit.txt"
with open(output_audit_path, "w", encoding="utf-8") as f:
    f.write("\n".join(audit_lines))

print(f"Successfully generated {len(final_180)} high-quality sports questions in questions_180.json and updated question_options_audit.txt")

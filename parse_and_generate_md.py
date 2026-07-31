import re
import json

raw_text = """
1. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Usain Bolt won the 100m in Beijing 2008. What was his winning time?
   *Answer:* 9.69 seconds
2. Which athlete finished second behind Bolt in the Beijing 100m final?
   *Answer:* Richard Thompson (Trinidad & Tobago)
3. What is the current Olympic 100m record?
   *Answer:* 9.63 seconds
4. At which Olympics was that record set?
   *Answer:* London 2012
5. Bolt is the only athlete to achieve what feat in the 100m and 200m?
   *Answer:* Win both events at three consecutive Olympics (2008, 2012, 2016)

### 2. [Medium]

What penalty is given for stepping on/over the baseline before striking a serve?
*Answer:* Foot fault

### 3. [Medium]

Which NBA team has a shamrock logo?
*Answer:* Boston Celtics

### 4. [Easy]

Which Grand Slam tournament is held in New York City?
*Answer:* US Open

### 5. [Easy]

Which footballer is nicknamed “CR7”?
*Answer:* Cristiano Ronaldo

### 6. [Medium]

Which player was known as The Answer?
*Answer:* Allen Iverson

### 7. [Medium]

What team did Tim Duncan spend his entire career with?
*Answer:* San Antonio Spurs

### 8. [Easy]

Who is known as “The King of Football”?
*Answer:* Pelé

### 9. [Easy]

What is the name of the rectangular areas where a serve must land?
*Answer:* Service box

### 10. [Easy]

What is the minimum number of games needed to win a standard tennis set?
*Answer:* Six

### 11. [Hard]

Which country won AFCON 2023? — Ivory Coast

### 12. [Hard]

Whose jersey number was retired across the entire NBA in 2022?
*Answer:* Bill Russell

### 13. [Medium]

In what year did the Open Era of tennis begin?
*Answer:* 1968

### 14. [Easy]

What are the four major tennis tournaments collectively known as?
*Answer:* The Grand Slams (Australian Open, French Open, Wimbledon, US Open)

### 15. [Hard]

Which country hosted the 2019 FIBA Basketball World Cup?
*Answer:* China

### 16. [Medium]

What is the official height of a standard tennis net at its center?
*Answer:* 3 feet

### 17. [Hard]

Which club won the 1999 Champions League? — Manchester United

### 18. [Medium]

Who won NBA MVP in 2016 unanimously?
*Answer:* Stephen Curry

### 19. [Hard]

Which club did Zidane retire from? — Real Madrid

### 20. [Medium]

What does PER stand for?
*Answer:* Player Efficiency Rating

### 21. [Medium]

Who has the highest single-game points total?
*Answer:* Wilt Chamberlain (100)

### 22. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which club did Ronaldo debut for before Man United?
   *Answer:* Sporting CP
2. Sporting CP is based in which capital?
   *Answer:* Lisbon
3. Which explorer reached India by sea, landing at Calicut in 1498?
   *Answer:* Vasco da Gama
4. Which Goan city is named for him with a football club?
   *Answer:* Vasco da Gama
5. Which Goan club has a rivalry with Dempo SC?
   *Answer:* Churchill Brothers

### 23. [Easy]

What color card is shown for a sending-off?
*Answer:* Red

### 24. [Hard]

Which player has scored the most goals in UEFA Champions League history?
*Answer:* Cristiano Ronaldo

### 25. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. How many ODI World Cups did Ponting win as Australia captain?
   *Answer:* Two (2003, 2007)
2. Ponting scored 140* in the 2003 final against which team?
   *Answer:* India
3. India's 2026 head coach who played in that final is who?
   *Answer:* Gautam Gambhir
4. Gambhir led which IPL franchise to its first two titles?
   *Answer:* Kolkata Knight Riders
5. Which river flows by KKR's home ground, Eden Gardens?
   *Answer:* Hooghly River

### 26. [Medium]

Who won the 1992 Olympic Dream Team gold?
*Answer:* USA

### 27. [Hard]

Which country hosted the first UEFA Euro? — France

### 28. [Hard]

Which player has won the NBA Defensive Player of the Year award four times?
*Answer:* Dikembe Mutombo

### 29. [Hard]

Which club won the 2004 Champions League? — Porto

### 30. [Hard]

Which player recorded the NBA's first quadruple-double with blocks?
*Answer:* Alvin Robertson

### 31. [Easy]

Which city hosted the 2020 Summer Olympic Games?
*Answer:* Tokyo, Japan

### 32. [Hard]

Which club won the inaugural UEFA Champions League (European Cup)?
*Answer:* Real Madrid

### 33. [Hard]

Which country hosted the FIFA World Cup in 1998?
*Answer:* France

### 34. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. How many Grand Slam singles titles did Serena win?
   *Answer:* 23
2. Which Australian spin legend wore jersey #23?
   *Answer:* Shane Warne
3. Warne captained which team to the inaugural 2008 IPL title?
   *Answer:* Rajasthan Royals
4. Rajasthan Royals play home games in which Pink City?
   *Answer:* Jaipur
5. How many players are on a polo team?
   *Answer:* Four

### 35. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Williamson led NZ to victory in the inaugural edition of which ICC tournament (2021)?
   *Answer:* World Test Championship
2. In which English city was that WTC final played?
   *Answer:* Southampton
3. Southampton FC's nickname is?
   *Answer:* The Saints
4. Which NFL team shares that nickname, based in Louisiana?
   *Answer:* New Orleans Saints
5. What is the Saints' home dome called?
   *Answer:* Caesars Superdome

### 36. [Hard]

Which player won the 2007 Ballon d'Or? — Kaká

### 37. [Hard]

Which club did Pirlo join after Milan? — Juventus

### 38. [Easy]

Which player has won the most Ballon d'Or awards?
*Answer:* Lionel Messi

### 39. [Medium]

Who scored the “Hand of God” goal?
*Answer:* Diego Maradona

### 40. [Hard]

Which country won the first Women's World Cup? — USA

### 41. [Medium]

Who coached the Chicago Bulls to six titles?
*Answer:* Phil Jackson

### 42. [Easy]

What term describes a match format involving two players on each side?
*Answer:* Doubles

### 43. [Hard]

Which player currently holds the highest career PER?
*Answer:* Nikola Jokić

### 44. [Hard]

Which player committed the most personal fouls in NBA history?
*Answer:* Robert Parish

### 45. [Hard]

Which goalkeeper captained Italy to the 2006 World Cup? — Buffon

### 46. [Hard]

Which nation has won the Copa América the most times?
*Answer:* Argentina

### 47. [Hard]

Which player won the 2006 Ballon d'Or? — Cannavaro

### 48. [Medium]

Who is Mr. Triple Double?
*Answer:* Russell Westbrook

### 49. [Medium]

Who is nicknamed “The Logo”?
*Answer:* Jerry West

### 50. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which country was Usain Bolt born in?
   *Answer:* Jamaica
2. Jamaica competes internationally in cricket as part of which team?
   *Answer:* West Indies
3. Who holds the record for highest individual Test score (400 not out)?
   *Answer:* Brian Lara
4. Lara's 400 came against which country?
   *Answer:* England
5. England's football team plays home games at which stadium?
   *Answer:* Wembley Stadium

### 51. [Easy]

How long is a standard football match (excluding extra time)?
*Answer:* 90 minutes

### 52. [Medium]

What spin causes the ball to dive sharply and bounce high?
*Answer:* Topspin

### 53. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which Olympic athletics record has stood since 1968?
   *Answer:* Men's Long Jump (Bob Beamon – 8.90m)
2. In which city was that record set?
   *Answer:* Mexico City
3. What was unusual about Mexico City's altitude that helped many performances?
   *Answer:* High altitude (~2,240m above sea level)
4. By how many centimetres did Beamon improve the previous world record?
   *Answer:* 55 cm
5. Who finally surpassed Beamon's world record in 1991?
   *Answer:* Mike Powell (8.95m)

### 54. [Hard]

Who became the first Indian-born player to appear in an NBA game?
*Answer:* Satnam Singh Bhullar

### 55. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Who captained Argentina at the 2022 World Cup?
   *Answer:* Lionel Messi
2. Messi won his first senior trophy defeating which rivals in the 2021 Copa América final?
   *Answer:* Brazil
3. Which Brazilian forward, famous for the elastico, mentored Messi at Barcelona?
   *Answer:* Ronaldinho
4. Ronaldinho played for which French club before Barcelona?
   *Answer:* Paris Saint-Germain
5. PSG plays home matches at which stadium?
   *Answer:* Parc des Princes

### 56. [Easy]

What color are the tennis balls universally used in professional tournaments today?
*Answer:* Optic Yellow

### 57. [Easy]

Which player is nicknamed “The Egyptian King”?
*Answer:* Mohamed Salah

### 58. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Neymar started his professional career at which club?
   *Answer:* Santos
2. Which legend made Santos famous worldwide?
   *Answer:* Pelé
3. How many FIFA World Cups did Pelé win?
   *Answer:* Three
4. Which country has won the most FIFA World Cups?
   *Answer:* Brazil
5. Which Brazilian won the 2007 Ballon d'Or?
   *Answer:* Kaká

### 59. [Easy]

What is a shot hit before the ball touches the ground called?
*Answer:* Volley

### 60. [Medium]

What is the premier international team competition in men's tennis called?
*Answer:* The Davis Cup

### 61. [Hard]

In what year was women's singles added to Wimbledon?
*Answer:* 1884

### 62. [Medium]

Which team drafted Kobe Bryant?
*Answer:* Charlotte Hornets

### 63. [Medium]

Who is the youngest male player to win a Grand Slam singles title?
*Answer:* Michael Chang

### 64. [Hard]

Which club did Thierry Henry leave to join Barcelona? — Arsenal

### 65. [Hard]

Which club did Kaká leave before joining Real Madrid? — Milan

### 66. [Easy]

What term describes the line that marks the back boundary of the court?
*Answer:* Baseline

### 67. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which was the first Olympic Games in which women were allowed to compete?
   *Answer:* Paris 1900
2. Which sport was the first in which women competed?
   *Answer:* Tennis (also golf)
3. Who became the first woman to win an Olympic gold medal?
   *Answer:* Charlotte Cooper
4. Which countries have appeared at every Summer Olympics since 1896?
   *Answer:* Greece and Australia
5. Which country has topped the Summer Olympic medal table the most times?
   *Answer:* United States

### 68. [Hard]

Which Grand Slam has been played on three different surfaces throughout its history?
*Answer:* US Open

### 69. [Hard]

What is the name of Liverpool's home stadium?
*Answer:* Anfield

### 70. [Hard]

Which player is nicknamed "O Fenômeno"? — Ronaldo

### 71. [Medium]

What surface is notoriously the slowest, producing higher bounces and longer rallies?
*Answer:* Clay

### 72. [Hard]

**Connection Chain — 10 linked questions (answer to each sets up the next):**

1. Who was Player of the Tournament in the 2003 ICC Cricket World Cup?
   *Answer:* Sachin Tendulkar
2. Who surpassed Tendulkar as highest run-scorer in ODI World Cup history?
   *Answer:* Virat Kohli
3. Against which team did Kohli score his 50th ODI century, breaking Tendulkar's record?
   *Answer:* New Zealand
4. Which New Zealand bowler dismissed Kohli after 117 runs in the 2023 World Cup semi-final?
   *Answer:* Tim Southee
5. Southee made his international debut in a T20 World Cup final against which country?
   *Answer:* India
6. Who was India's highest wicket-taker in that 2007 T20 World Cup final?
   *Answer:* Irfan Pathan
7. Pathan made his Test debut under which Indian captain?
   *Answer:* Sourav Ganguly
8. Ganguly scored his maiden Test century at which iconic ground?
   *Answer:* Lord's
9. Which bowler dismissed Ganguly after his 131 on Test debut at Lord's?
   *Answer:* Chris Lewis
10. Chris Lewis represented which country?
   *Answer:* England

### 73. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Juventus is based in which Italian city?
   *Answer:* Turin
2. Turin hosted the Winter Olympics in which year?
   *Answer:* 2006
3. Italy's 2006 World Cup captain was?
   *Answer:* Fabio Cannavaro
4. Cannavaro is one of few defenders to win which award?
   *Answer:* Ballon d'Or
5. Which magazine has presented the Ballon d'Or since 1956?
   *Answer:* France Football

### 74. [Hard]

Who won the first NBA MVP Award?
*Answer:* Bob Pettit

### 75. [Hard]

Which nation won the inaugural UEFA Nations League? — Portugal

### 76. [Easy]

What is it called when a server commits two consecutive serving errors?
*Answer:* Double fault

### 77. [Medium]

Which country has won the most FIFA World Cups?
*Answer:* Brazil

### 78. [Medium]

What is the width of a standard doubles tennis court?
*Answer:* 36 feet

### 79. [Easy]

What is the term for winning a point directly from a serve that the opponent cannot touch?
*Answer:* An ace

### 80. [Hard]

Which coach has the most regular-season wins in NBA history?
*Answer:* Don Nelson

### 81. [Hard]

Which player was selected immediately after Michael Jordan in the 1984 NBA Draft?
*Answer:* Sam Perkins

### 82. [Medium]

Which franchise relocated from Seattle to OKC?
*Answer:* SuperSonics

### 83. [Easy]

Which body governs world football?
*Answer:* FIFA

### 84. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Federer represents which Alpine nation?
   *Answer:* Switzerland
2. Which Swiss watch brand sponsors Federer and times Wimbledon?
   *Answer:* Rolex
3. Which Grand Slam is played on red clay?
   *Answer:* French Open
4. Who is the King of Clay with 14 French Open titles?
   *Answer:* Rafael Nadal
5. Nadal won singles gold at which 2008 Olympics?
   *Answer:* Beijing

### 85. [Easy]

What is awarded when a foul is committed inside the penalty box?
*Answer:* A penalty kick

### 86. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. How many titles did Jordan win with the Bulls?
   *Answer:* Six
2. Who hit six sixes in an over in a T20 World Cup match?
   *Answer:* Yuvraj Singh
3. Yuvraj hit those sixes off which English bowler?
   *Answer:* Stuart Broad
4. Broad played his final Test at which historic London ground?
   *Answer:* The Oval
5. The Oval hosted the first international cricket match (1880) vs which country?
   *Answer:* Australia

### 87. [Hard]

Which player won the first unanimous MVP award?
*Answer:* Stephen Curry

### 88. [Hard]

Which player has recorded the most career playoff triple-doubles?
*Answer:* LeBron James

### 89. [Hard]

Who won the first NBA Slam Dunk Contest?
*Answer:* Larry Nance Jr.

### 90. [Hard]

Which player has the most All-NBA First Team selections?
*Answer:* LeBron James

### 91. [Hard]

Who scored the "Hand of God" goal? — Maradona

### 92. [Hard]

Which stadium hosted the 2014 World Cup final? — Maracanã

### 93. [Hard]

Who holds the record for most consecutive matches won on a single surface (men's, Open Era)?
*Answer:* Rafael Nadal (81, clay)

### 94. [Hard]

Which franchise originally drafted Dirk Nowitzki?
*Answer:* Milwaukee Bucks

### 95. [Hard]

Who won the inaugural NBA Sixth Man of the Year Award?
*Answer:* Bobby Jones

### 96. [Easy]

What is the official title of the person who sits in the elevated chair to officiate?
*Answer:* Umpire

### 97. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. How many Olympic golds does Michael Phelps hold?
   *Answer:* 23
2. Which Australian cricket legend wore jersey #23?
   *Answer:* Shane Warne
3. Warne bowled the 'Ball of the Century' to dismiss which batsman?
   *Answer:* Mike Gatting
4. Which English captain led the 2010/11 Ashes win in Australia?
   *Answer:* Andrew Strauss
5. Strauss played county cricket for which London club?
   *Answer:* Middlesex

### 98. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Ajax is based in which Dutch city?
   *Answer:* Amsterdam
2. Ajax's stadium was renamed in 2018 for which figure?
   *Answer:* Johan Cruyff
3. Which French legend won the Ballon d'Or three times consecutively (1983-85)?
   *Answer:* Michel Platini
4. Platini later presided over which governing body?
   *Answer:* UEFA
5. UEFA's HQ is in which Swiss town?
   *Answer:* Nyon

### 99. [Medium]

Which club wears yellow and black as its traditional colors?
*Answer:* Borussia Dortmund

### 100. [Hard]

Who achieved a 'Boxed Set' of all Grand Slam titles (singles, doubles, mixed)?
*Answer:* Martina Navratilova

### 101. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which previous Olympics, awarded to Tokyo, was cancelled due to WWII?
   *Answer:* The 1940 Olympics
2. Which city hosted the first Olympics after WWII?
   *Answer:* London (1948)
3. Name two of the four sports Tokyo 2020 introduced to the programme.
   *Answer:* Skateboarding, Sport Climbing, Surfing, Karate (any two)
4. Which of those sports was not retained for Paris 2024?
   *Answer:* Karate
5. Which sport returns at Los Angeles 2028 after a 128-year absence?
   *Answer:* Cricket

### 102. [Hard]

Which player was selected immediately before Michael Jordan in the 1984 NBA Draft?
*Answer:* Sam Bowie

### 103. [Medium]

Which country has won the most Olympic men's basketball golds?
*Answer:* USA

### 104. [Hard]

Who is the only male player to win the Calendar Grand Slam twice in the Open Era?
*Answer:* Rod Laver

### 105. [Hard]

Which coach developed the Triangle Offense?
*Answer:* Tex Winter

### 106. [Medium]

Which player is nicknamed Joker?
*Answer:* Nikola Jokić

### 107. [Easy]

What is it called when a player wins a game on their opponent's serve?
*Answer:* Break

### 108. [Medium]

Who is the NBA all-time blocks leader?
*Answer:* Hakeem Olajuwon

### 109. [Hard]

Which country won the 2023 FIBA Basketball World Cup?
*Answer:* Germany

### 110. [Medium]

Who won the first NBA championship?
*Answer:* Philadelphia Warriors

### 111. [Hard]

Which player won three consecutive NBA MVP awards from 1984 to 1986?
*Answer:* Larry Bird

### 112. [Hard]

Which club is nicknamed "The Old Lady"? — Juventus

### 113. [Hard]

Which nation won the 1974 World Cup? — Germany (West Germany)

### 114. [Medium]

Who is known as The Greek Freak?
*Answer:* Giannis Antetokounmpo

### 115. [Hard]

Which country won the first FIFA World Cup? — Uruguay

### 116. [Hard]

Who is the all-time top scorer for Brazil?
*Answer:* Neymar

### 117. [Easy]

Which Grand Slam tournament is held annually in Melbourne?
*Answer:* Australian Open

### 118. [Hard]

Who is the all-time top scorer in FIFA World Cup history?
*Answer:* Miroslav Klose

### 119. [Medium]

Who is the NBA's all-time leading scorer?
*Answer:* LeBron James

### 120. [Medium]

Which football club is nicknamed “The Red Devils”?
*Answer:* Manchester United

### 121. [Medium]

What is the FIBA three-point distance?
*Answer:* 6.75 m

### 122. [Medium]

What is the technical name for the grip with the index knuckle on bevel 3, popular for forehands?
*Answer:* Eastern grip

### 123. [Hard]

**Connection Chain — 20 linked questions (answer to each sets up the next):**

1. Who won the FIFA World Cup in 2022?
   *Answer:* Argentina
2. Which legendary player captained Argentina to that title?
   *Answer:* Lionel Messi
3. Messi spent most of his club career at which Spanish club?
   *Answer:* Barcelona
4. Barcelona plays home matches at which stadium?
   *Answer:* Camp Nou
5. Camp Nou is located in which city?
   *Answer:* Barcelona
6. Which famous rivalry features Barcelona vs Real Madrid?
   *Answer:* El Clásico
7. Which club has won the most UEFA Champions League titles?
   *Answer:* Real Madrid
8. Which Portuguese superstar became Real Madrid's all-time leading scorer?
   *Answer:* Cristiano Ronaldo
9. Ronaldo is the all-time top scorer for which national team?
   *Answer:* Portugal
10. Portugal won which major tournament in 2016?
   *Answer:* UEFA Euro 2016
11. Which country hosted Euro 2016?
   *Answer:* France
12. France won the FIFA World Cup most recently in which year?
   *Answer:* 2018
13. Who scored four goals for France in the 2018 World Cup?
   *Answer:* Kylian Mbappé
14. Mbappé began his professional career at which club?
   *Answer:* AS Monaco
15. Monaco competes in which country's league?
   *Answer:* France (Ligue 1)
16. Which club has won the most Ligue 1 titles?
   *Answer:* Paris Saint-Germain
17. Which Brazilian star formed the famous 'MNM' trio at PSG?
   *Answer:* Neymar Jr.
18. Neymar won the Champions League with which club?
   *Answer:* Barcelona
19. Barcelona's biggest domestic rival is which club?
   *Answer:* Real Madrid
20. Which trophy do Barcelona and Real Madrid both compete for in Europe?
   *Answer:* UEFA Champions League

### 124. [Hard]

Which player has been ejected the most times in NBA history?
*Answer:* Rasheed Wallace

### 125. [Hard]

Which country hosted the 1994 World Cup? — USA

### 126. [Hard]

Which nation won the 1998 World Cup? — France

### 127. [Hard]

Which player scored 81 points against the Toronto Raptors in 2006?
*Answer:* Kobe Bryant

### 128. [Easy]

On which court surface is the French Open played?
*Answer:* Clay

### 129. [Medium]

What grip is universally used by pros to hit a flat first serve?
*Answer:* Continental grip

### 130. [Easy]

What score must a player reach to win a standard set tie-break?
*Answer:* Seven

### 131. [Easy]

What is the penalty called when a server steps on the baseline during a serve?
*Answer:* Foot fault

### 132. [Medium]

What year was the Australian Open first held?
*Answer:* 1905

### 133. [Hard]

Which player holds the NBA record for the most career turnovers?
*Answer:* LeBron James

### 134. [Medium]

What does VAR stand for?
*Answer:* Video Assistant Referee

### 135. [Medium]

Who has the most career triple-doubles?
*Answer:* Russell Westbrook

### 136. [Hard]

Who won the first NBA Finals MVP Award?
*Answer:* Jerry West

### 137. [Hard]

Which club has won the most UEFA Champions League titles? — Real Madrid

### 138. [Easy]

Which country won the FIFA World Cup in 2022?
*Answer:* Argentina

### 139. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Gayle's record 175* in IPL 2013 was for which team?
   *Answer:* Royal Challengers Bangalore
2. That innings came against which now-defunct franchise?
   *Answer:* Pune Warriors India
3. What stadium in Pune hosts international cricket?
   *Answer:* Maharashtra Cricket Association Stadium
4. Which visiting team beat India there in the 2017 Test?
   *Answer:* Australia
5. Which Australian spinner took 12 wickets in that match?
   *Answer:* Steve O'Keefe

### 140. [Medium]

Which NBA team plays at Madison Square Garden?
*Answer:* New York Knicks

### 141. [Hard]

Which player has the most assists in UEFA Champions League history?
*Answer:* Lionel Messi

### 142. [Hard]

Which player scored the winning goal in the 1999 Champions League final? — Solskjær

### 143. [Hard]

Which nation won UEFA Euro 2024?
*Answer:* Spain

### 144. [Hard]

Which player appeared in the most NBA Finals?
*Answer:* Bill Russell

### 145. [Medium]

Which player is called Chef Curry?
*Answer:* Stephen Curry

### 146. [Hard]

Which nation hosted Euro 2016? — France

### 147. [Easy]

What is the official match ball called in football?
*Answer:* (varies by tournament, e.g. the Adidas match ball)

### 148. [Hard]

Which female player pushed for equal prize money at Wimbledon in 2007?
*Answer:* Venus Williams

### 149. [Medium]

Which country won the FIBA World Cup 2023?
*Answer:* Germany

### 150. [Easy]

What is the term for a high, arching shot designed to go over an opponent's head?
*Answer:* Lob

### 151. [Medium]

Which female player holds the all-time record (amateur + Open era) for Grand Slam singles titles?
*Answer:* Margaret Court (24)

### 152. [Easy]

Which Grand Slam tournament is held annually in Melbourne? (Australian Open)
*Answer:* Australian Open

### 153. [Medium]

Who was the first unseeded player to win the Wimbledon men's singles title?
*Answer:* Goran Ivanišević (2001)

### 154. [Hard]

Which club did Xabi Alonso leave before Bayern? — Real Madrid

### 155. [Easy]

Which city hosted the 2024 Summer Olympic Games?
*Answer:* Paris, France

### 156. [Hard]

Who is the only tennis player to achieve a Golden Slam in a calendar year?
*Answer:* Steffi Graf

### 157. [Hard]

Which player scored 70 points in a game before turning 21?
*Answer:* Devin Booker

### 158. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Chhetri's farewell match in 2024 was against which country?
   *Answer:* Kuwait
2. Kuwait hosted the first edition of which multi-sport event in 1982?
   *Answer:* West Asian Games
3. The Asian Games were first held in 1951 in which city?
   *Answer:* New Delhi
4. Which spinner took all 10 wickets at Delhi's Feroz Shah Kotla in 1999?
   *Answer:* Anil Kumble
5. What is Kumble's nickname?
   *Answer:* Jumbo

### 159. [Medium]

Who popularized the skyhook?
*Answer:* Kareem Abdul-Jabbar

### 160. [Hard]

Which Indian player was drafted by the Sacramento Kings in 2015?
*Answer:* Satnam Singh

### 161. [Medium]

Who is the NBA all-time steals leader?
*Answer:* John Stockton

### 162. [Hard]

Who has the highest career points-per-game average in NBA history?
*Answer:* Michael Jordan

### 163. [Hard]

In what year did the Australian Open switch from grass to hard courts?
*Answer:* 1988

### 164. [Easy]

What term refers to the first point won after a deuce?
*Answer:* Advantage

### 165. [Easy]

Which city hosted the 2008 Summer Olympics?
*Answer:* Beijing, China

### 166. [Hard]

Which club is known as “The Old Lady”?
*Answer:* Juventus

### 167. [Medium]

What is the name of Barcelona's home stadium?
*Answer:* Camp Nou

### 168. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which city hosted the 2024 Summer Olympic Games?
   *Answer:* Paris, France
2. Paris became only the second city to host the Summer Olympics three times. Which was the first?
   *Answer:* London
3. Which athlete set an Olympic record of 6.25m in men's pole vault at Paris 2024?
   *Answer:* Armand “Mondo” Duplantis
4. Which country does Duplantis represent?
   *Answer:* Sweden
5. Besides Olympic gold, what major record did Duplantis continue to hold after Paris 2024?
   *Answer:* The men's pole vault world record

### 169. [Hard]

Before 1972, what color were standard tennis balls?
*Answer:* White or black

### 170. [Hard]

Which club first signed Cristiano Ronaldo professionally? — Sporting

### 171. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which franchise did LeBron lead to a 3-1 comeback title in 2016?
   *Answer:* Cleveland Cavaliers
2. LeBron then joined which LA franchise?
   *Answer:* Los Angeles Lakers
3. Which late Lakers legend wore #8 and #24?
   *Answer:* Kobe Bryant
4. Kobe won Olympic gold with the 'Redeem Team' at which 2008 host city?
   *Answer:* Beijing
5. Which racquet sport saw India win its first Thomas Cup gold in China?
   *Answer:* Badminton

### 172. [Hard]

Which female player won the 2017 Australian Open while eight weeks pregnant?
*Answer:* Serena Williams

### 173. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which club has won the most Champions League titles?
   *Answer:* Real Madrid
2. Which Croatian midfielder won five Champions Leagues with Real Madrid?
   *Answer:* Luka Modrić
3. Modrić captains which national team?
   *Answer:* Croatia
4. Croatia lost the 2018 World Cup final to which country?
   *Answer:* France
5. Which French striker won the 2022 Ballon d'Or?
   *Answer:* Karim Benzema

### 174. [Hard]

Which nation has won the Africa Cup of Nations the most times?
*Answer:* Egypt

### 175. [Medium]

Who won NBA MVP 2024-25?
*Answer:* Shai Gilgeous-Alexander

### 176. [Hard]

Which player won Olympic gold medals in three different decades?
*Answer:* LeBron James

### 177. [Hard]

In what year were tiebreaks formally introduced at Wimbledon?
*Answer:* 1971

### 178. [Hard]

Which goalkeeper won the Ballon d'Or? — Yashin

### 179. [Easy]

What surface is the French Open played on?
*Answer:* Clay

### 180. [Easy]

What is a powerful, overhead shot used to finish a point called?
*Answer:* Smash

### 181. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Lin Dan, the greatest badminton player, represents which country?
   *Answer:* China
2. Lin Dan beat which Malaysian rival in two Olympic finals?
   *Answer:* Lee Chong Wei
3. The Malaysia Open is held in which capital?
   *Answer:* Kuala Lumpur
4. Near KL, which sport has a street race in Singapore?
   *Answer:* Formula 1
5. What is unique about the Singapore GP?
   *Answer:* It's held at night

### 182. [Hard]

Who was the first male player to reach 100 ATP singles titles?
*Answer:* Jimmy Connors

### 183. [Medium]

In what year was the French Open first held?
*Answer:* 1891

### 184. [Medium]

What is the premier international team competition in women's tennis called?
*Answer:* The Billie Jean King Cup

### 185. [Hard]

Which player has the most World Cup goals? — Klose

### 186. [Hard]

Which player wore jersey number 45 after returning from retirement?
*Answer:* Michael Jordan

### 187. [Medium]

Who has the most career 3-pointers?
*Answer:* Stephen Curry

### 188. [Hard]

Which player won MVP in his rookie season?
*Answer:* Wes Unseld

### 189. [Hard]

Which club did Neymar leave to join PSG? — Barcelona

### 190. [Medium]

What is the technical term for a serve that hits the net cord but still lands in the correct service box?
*Answer:* Let

### 191. [Hard]

Which player has the most international appearances in men's football?
*Answer:* Bader Al-Mutawa (or Cristiano Ronaldo, depending on source)

### 192. [Hard]

Which nation won the 1966 World Cup? — England

### 193. [Hard]

Which player attempted the most free throws in NBA history?
*Answer:* Karl Malone

### 194. [Hard]

Who won the Ballon d'Or in 2025?
*Answer:* (check latest records — winner varies by source)

### 195. [Hard]

Which player scored the winning goal in the 2010 FIFA World Cup Final?
*Answer:* Andrés Iniesta

### 196. [Hard]

Which player won the 1987 Ballon d'Or? — Gullit

### 197. [Hard]

Which male player holds the record for most ATP Finals titles?
*Answer:* Novak Djokovic (7)

### 198. [Hard]

What is the French Open men's trophy named in honor of?
*Answer:* The Four Musketeers

### 199. [Medium]

Who won the FIFA World Cup in 2022?
*Answer:* Argentina

### 200. [Easy]

What is the term for the stroke played on the side opposite to the dominant hand?
*Answer:* Backhand

### 201. [Medium]

What material was traditionally used for high-end tennis strings?
*Answer:* Natural gut

### 202. [Hard]

Which nation won Euro 2004? — Greece

### 203. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. How many Champions League titles has Real Madrid won?
   *Answer:* 15
2. Real Madrid beat which German club in the 2024 final?
   *Answer:* Borussia Dortmund
3. Dortmund's stand is nicknamed?
   *Answer:* The Yellow Wall
4. Which cricket team is nicknamed the Canaries for yellow kit?
   *Answer:* Australia
5. Who captains Australia's men's Test team?
   *Answer:* Pat Cummins

### 204. [Medium]

In what year did the US Open begin?
*Answer:* 1881

### 205. [Hard]

Which country won Copa América 2021? — Argentina

### 206. [Hard]

Which player won NBA Finals MVP despite being on the losing team?
*Answer:* Jerry West

### 207. [Hard]

Which Grand Slam tournament continues to be played on its original surface (grass)?
*Answer:* Wimbledon

### 208. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which city hosted the 2008 Summer Olympics?
   *Answer:* Beijing, China
2. Which sprinter won gold in the 100m, 200m and 4x100m relay at Beijing 2008?
   *Answer:* Usain Bolt
3. What Olympic record did Bolt set in the 100m final at Beijing 2008?
   *Answer:* 9.69 seconds
4. At which Olympics did Bolt improve that record to 9.63 seconds?
   *Answer:* London 2012
5. Who currently holds the Olympic records in both the 100m and 200m?
   *Answer:* Usain Bolt

### 209. [Hard]

Which club has won the most English league titles?
*Answer:* Manchester United

### 210. [Easy]

Which trophy is awarded to the FIFA World Cup winners?
*Answer:* The FIFA World Cup Trophy

### 211. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Who captained Mumbai Indians in their inaugural 2008 season?
   *Answer:* Harbhajan Singh
2. Harbhajan was involved in 'Monkeygate' during a tour of which country?
   *Answer:* Australia
3. Which Sydney ground hosted that 2008 Test?
   *Answer:* Sydney Cricket Ground
4. What object is used to score in AFL, also used in rugby?
   *Answer:* Oval/rugby ball
5. How many points is a rugby try worth?
   *Answer:* Five

### 212. [Hard]

Which player won the NBA Finals MVP as a rookie?
*Answer:* Magic Johnson

### 213. [Medium]

Which player is famous for the Dream Shake?
*Answer:* Hakeem Olajuwon

### 214. [Medium]

Who was nicknamed Black Mamba?
*Answer:* Kobe Bryant

### 215. [Hard]

Which player won the Golden Boot at the 2014 World Cup? — Rodríguez

### 216. [Easy]

Which country is famous for the Premier League?
*Answer:* England

### 217. [Hard]

Which player holds the NBA record for most career rebounds?
*Answer:* Wilt Chamberlain

### 218. [Medium]

Which country hosted the 2014 FIFA World Cup?
*Answer:* Brazil

### 219. [Easy]

What term is used in tennis to represent a score of zero?
*Answer:* Love

### 220. [Hard]

Which nation won the 1938 World Cup? — Italy

### 221. [Hard]

Which manager was known as "The Special One"? — Mourinho

### 222. [Hard]

Which player was nicknamed “The Big O”?
*Answer:* Oscar Robertson

### 223. [Medium]

Who was the youngest NBA MVP?
*Answer:* Derrick Rose

### 224. [Hard]

Which country won Euro 1992? — Denmark

### 225. [Easy]

Which football club's motto is “You'll Never Walk Alone”?
*Answer:* Liverpool

### 226. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which club did Messi score his first senior goal for?
   *Answer:* Barcelona
2. Barcelona's biggest rivals are?
   *Answer:* Real Madrid
3. Which English midfielder joined Real Madrid in 2023?
   *Answer:* Jude Bellingham
4. Bellingham joined Real Madrid from which club?
   *Answer:* Borussia Dortmund
5. Dortmund's home stadium is?
   *Answer:* Signal Iduna Park

### 227. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which city hosted the 2020 Summer Olympic Games?
   *Answer:* Tokyo, Japan
2. Why were they held in 2021 instead of 2020?
   *Answer:* Due to the COVID-19 pandemic
3. Which new sport debuted at Tokyo 2020 and was also in Paris 2024?
   *Answer:* Skateboarding (also Surfing/Sport Climbing)
4. Which country topped the Tokyo 2020 medal table?
   *Answer:* United States
5. Which gymnast won bronze on balance beam at Tokyo 2020 after withdrawing from several events?
   *Answer:* Simone Biles

### 228. [Hard]

Which club did Ronaldinho join after Barcelona? — Milan

### 229. [Medium]

Which club has won the most Ligue 1 titles?
*Answer:* Paris Saint-Germain

### 230. [Hard]

Prior to 1988, which Grand Slam was played on grass before switching to hard courts?
*Answer:* Australian Open

### 231. [Medium]

What is the length of a standard tennis court from baseline to baseline?
*Answer:* 78 feet

### 232. [Hard]

Which player won Finals MVP after leading Dallas to the 2011 title?
*Answer:* Dirk Nowitzki

### 233. [Medium]

Which country won the first FIFA World Cup in 1930?
*Answer:* Uruguay

### 234. [Hard]

Which player missed the decisive penalty in the 1994 World Cup final? — Baggio

### 235. [Medium]

Which Masters 1000 event is often called the unofficial 'Fifth Grand Slam'?
*Answer:* Indian Wells

### 236. [Easy]

In a standard tennis game, what score comes immediately after 30?
*Answer:* 40

### 237. [Hard]

What was the original patented name of lawn tennis, given by Major Wingfield in 1873?
*Answer:* Sphairistikè

### 238. [Hard]

Which club is nicknamed “The Citizens”?
*Answer:* Manchester City

### 239. [Easy]

What is the primary piece of equipment used to strike the ball?
*Answer:* Racket

### 240. [Hard]

Who captained Spain to the 2010 World Cup? — Casillas

### 241. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Ronaldo won his first Ballon d'Or while at which club?
   *Answer:* Manchester United
2. Which manager signed Ronaldo for Man United in 2003?
   *Answer:* Sir Alex Ferguson
3. Ferguson previously managed which national team?
   *Answer:* Scotland
4. Which country defeated Scotland in the Euro 2024 opening match?
   *Answer:* Germany
5. Germany won the 2014 World Cup final against which country?
   *Answer:* Argentina

### 242. [Hard]

Which country won the inaugural FIBA Basketball World Cup in 1950?
*Answer:* Argentina

### 243. [Hard]

Which player has the nickname "Il Divin Codino"? — Baggio

### 244. [Medium]

Which legendary player captained Argentina to the 2022 World Cup title?
*Answer:* Lionel Messi

### 245. [Hard]

Which country has reached the most World Cup finals? — Germany

### 246. [Easy]

Which city is home to AC Milan?
*Answer:* Milan

### 247. [Medium]

Who won the 2025 NBA championship?
*Answer:* Oklahoma City Thunder

### 248. [Medium]

Who was the No.1 pick in 2003?
*Answer:* LeBron James

### 249. [Easy]

What does the term "love" mean in tennis scoring?
*Answer:* Zero

### 250. [Medium]

Which player was Finals MVP in 2023?
*Answer:* Nikola Jokić

### 251. [Hard]

Which player was nicknamed “Pistol”?
*Answer:* Pete Maravich

### 252. [Hard]

Who scored the fastest World Cup final goal? — Mbappé

### 253. [Hard]

Which male player holds the record for most consecutive weeks at World No. 1?
*Answer:* Roger Federer (237 weeks)

### 254. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Simone Biles competes in which Olympic sport?
   *Answer:* Artistic Gymnastics
2. On which apparatus does she have a signature dismount named after her?
   *Answer:* Balance Beam
3. The beam is 4 inches wide; how many inches high are cricket stumps (excl. bails)?
   *Answer:* 28 inches
4. 28 was the jersey number of which Indian left-arm spinner?
   *Answer:* Pragyan Ojha
5. Ojha won the Purple Cap in 2010 with which defunct franchise?
   *Answer:* Deccan Chargers

### 255. [Medium]

Which team did Shaquille O'Neal win three straight titles with?
*Answer:* Lakers

### 256. [Easy]

Which player is famous for the “Siuuu” celebration?
*Answer:* Cristiano Ronaldo

### 257. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Under which manager did Man United win 13 league titles?
   *Answer:* Sir Alex Ferguson
2. Ferguson led which Scottish club to a 1983 Cup Winners' Cup win over Real Madrid?
   *Answer:* Aberdeen
3. Aberdeen's primary kit color is?
   *Answer:* Red
4. Which F1 team is synonymous with racing red?
   *Answer:* Ferrari
5. Who is Ferrari's lead driver alongside Hamilton for 2026?
   *Answer:* Charles Leclerc

### 258. [Hard]

How many combined aces were served in the 2010 Isner-Mahut match?
*Answer:* 216

### 259. [Hard]

Which goalkeeper has the most clean sheets in Premier League history?
*Answer:* Petr Čech

### 260. [Medium]

What is the term for the two thin parallel strips only 'in' during doubles?
*Answer:* Alleys

### 261. [Easy]

What is the name of the central mesh barrier that divides the court?
*Answer:* Net

### 262. [Easy]

What term describes a match format involving one player on each side?
*Answer:* Singles

### 263. [Medium]

Who is the WNBA all-time leading scorer?
*Answer:* Diana Taurasi

### 264. [Hard]

Which club plays at Signal Iduna Park? — Dortmund

### 265. [Hard]

What is the name of Borussia Dortmund's home stadium?
*Answer:* Signal Iduna Park

### 266. [Easy]

What surface is Wimbledon played on?
*Answer:* Grass

### 267. [Hard]

Which player scored the winning goal in the 2010 World Cup final? — Iniesta

### 268. [Medium]

Which player is Portugal's all-time leading scorer?
*Answer:* Cristiano Ronaldo

### 269. [Hard]

Which coach has won the most NBA championships?
*Answer:* Red Auerbach

### 270. [Easy]

What is the term for a shot hit softly over the net, landing just on the other side?
*Answer:* Drop shot

### 271. [Medium]

Who is the youngest female player to win a Grand Slam singles title?
*Answer:* Martina Hingis

### 272. [Hard]

Which player scored the "Goal of the Century"? — Maradona

### 273. [Hard]

Which club did Luis Suárez join after Liverpool? — Barcelona

### 274. [Easy]

Which footballer is nicknamed “La Pulga”?
*Answer:* Lionel Messi

### 275. [Hard]

Which country won the first UEFA European Championship? — Soviet Union

### 276. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which major is always played at Augusta National?
   *Answer:* The Masters
2. Masters winner is presented with what garment?
   *Answer:* Green Jacket
3. Green links to which Saudi-backed breakaway golf league?
   *Answer:* LIV Golf
4. Which Australian golfer is LIV Golf's CEO?
   *Answer:* Greg Norman
5. Which trophy is contested between India and Australia in Test cricket?
   *Answer:* Border-Gavaskar Trophy

### 277. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Ali's 1974 fight vs Foreman in Zaire was billed as?
   *Answer:* The Rumble in the Jungle
2. Zaire is now known as?
   *Answer:* Democratic Republic of the Congo
3. DR Congo has won AFCON twice; which country hosted 2023's edition?
   *Answer:* Ivory Coast
4. Ivory Coast's football legend who starred for Chelsea is?
   *Answer:* Didier Drogba
5. Drogba scored the winning penalty in the 2012 CL final vs which club?
   *Answer:* Bayern Munich

### 278. [Hard]

Which player won the 1995 Ballon d'Or? — Weah

### 279. [Medium]

What is the maximum number of sets played in a men's singles match at a Grand Slam?
*Answer:* Five

### 280. [Medium]

Which franchise has the most NBA championships?
*Answer:* Boston Celtics

### 281. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Which IPL franchise did MS Dhoni lead to five titles?
   *Answer:* Chennai Super Kings
2. In which city is CSK's home ground located?
   *Answer:* Chennai
3. Which Tamil Nadu-born spinner was first Indian to 300 T20 wickets?
   *Answer:* Ravichandran Ashwin
4. Ashwin played county cricket for which English club?
   *Answer:* Worcestershire
5. What is Worcestershire's nickname?
   *Answer:* The Pears

### 282. [Hard]

Which city hosted the 2012 Champions League final? — Munich

### 283. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Mbappé rose to fame at which Ligue 1 club before PSG?
   *Answer:* Monaco
2. Monaco hosts which prestigious street-circuit race?
   *Answer:* Monaco Grand Prix
3. Which Brazilian F1 legend has the most Monaco GP wins (6)?
   *Answer:* Ayrton Senna
4. Senna died at the San Marino GP at which track in 1994?
   *Answer:* Imola
5. Which Italian club is nicknamed 'The Old Lady'?
   *Answer:* Juventus

### 284. [Medium]

Who has the most career assists?
*Answer:* John Stockton

### 285. [Easy]

How many players are on the field for one team at the start of a football match?
*Answer:* Eleven

### 286. [Hard]

Which country hosted UEFA Euro 2016?
*Answer:* France

### 287. [Hard]

Which player has the most All-Defensive Team selections in NBA history?
*Answer:* Kobe Bryant

### 288. [Medium]

What is the name of the electronic line-calling system using multiple cameras?
*Answer:* Hawk-Eye

### 289. [Hard]

Which player was nicknamed “The Iceman”?
*Answer:* George Gervin

### 290. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. Who is Bayern's all-time top scorer, nicknamed 'Der Bomber'?
   *Answer:* Gerd Müller
2. Müller scored the winning goal in the 1974 final against which team?
   *Answer:* Netherlands
3. The Dutch 1970s philosophy pioneered by Cruyff was called?
   *Answer:* Total Football
4. Cruyff played for Ajax and which Spanish club?
   *Answer:* Barcelona
5. Barcelona's youth academy that produced Messi is called?
   *Answer:* La Masia

### 291. [Medium]

Who won Rookie of the Year 2024?
*Answer:* Victor Wembanyama

### 292. [Hard]

**Connection Chain — 5 linked questions (answer to each sets up the next):**

1. With which team did Hamilton win six of his seven titles?
   *Answer:* Mercedes
2. Which German driver won four straight titles with Red Bull (2010-2013)?
   *Answer:* Sebastian Vettel
3. Vettel retired from F1 driving for which British team?
   *Answer:* Aston Martin
4. Aston Martin's color links to which green-jerseyed rugby team?
   *Answer:* South Africa (Springboks)
5. Who captained the Springboks to back-to-back World Cup wins (2019, 2023)?
   *Answer:* Siya Kolisi

### 293. [Easy]

What is the traditional court surface used at Wimbledon?
*Answer:* Grass

### 294. [Hard]

Who played in the longest tennis match in history at Wimbledon in 2010?
*Answer:* John Isner and Nicolas Mahut

### 295. [Medium]

What is the width of a standard singles tennis court?
*Answer:* 27 feet

### 296. [Medium]

What is the minimum number of points needed to win a standard tiebreak?
*Answer:* Seven

### 297. [Easy]

What is the term for a shot hit before the ball bounces on the court?
*Answer:* A volley

### 298. [Easy]

What is a legal serve that goes untouched by the receiver called?
*Answer:* Ace

### 299. [Easy]

What is the term for a 40-40 tie in a game?
*Answer:* Deuce

### 300. [Hard]

Which player was nicknamed “The Admiral”?
*Answer:* David Robinson

### 301. [Easy]

What is the score called when both players are tied at 40-40?
*Answer:* Deuce

### 302. [Hard]

**Connection Chain — 10 linked questions (answer to each sets up the next):**

1. Who was Player of the Match in the 2019 ICC Cricket World Cup Final?
   *Answer:* Ben Stokes
2. Ben Stokes was born in which country?
   *Answer:* New Zealand
3. Which NZ captain scored an unbeaten 152 in the inaugural WTC Final?
   *Answer:* Kane Williamson
4. Against which team did Williamson score that 152?
   *Answer:* India
5. Which Indian bowler was leading wicket-taker in that WTC Final?
   *Answer:* Mohammed Shami
6. Shami made his ODI debut against which country?
   *Answer:* Pakistan
7. Which Pakistani batter scored the first-ever T20I century?
   *Answer:* Ahmed Shehzad
8. Shehzad scored that century against which team?
   *Answer:* Bangladesh
9. Which Bangladesh cricketer was first to 6,000 ODI runs and 300 ODI wickets?
   *Answer:* Shakib Al Hasan
10. Shakib won the ICC Men's Cricketer of the Year award in which year?
   *Answer:* 2019

### 303. [Easy]

Which country is home to the club Boca Juniors?
*Answer:* Argentina

### 304. [Medium]

Who has the most NBA championships as a player?
*Answer:* Bill Russell (11)

### 305. [Medium]

What is the maximum duration allowed between points on the ATP/WTA shot clock?
*Answer:* 25 seconds

### 306. [Medium]

In what year was the first Wimbledon Championship held?
*Answer:* 1877

### 307. [Hard]

What is the name of Bayern Munich's home stadium?
*Answer:* Allianz Arena

### 308. [Easy]

What is the maximum number of regular substitutions allowed in most competitions today?
*Answer:* Five

### 309. [Medium]

Which club has won the most UEFA Champions League titles?
*Answer:* Real Madrid
"""

# Parsing logic
blocks = re.split(r'\n(?=(?:###\s*)?\d+\.\s*\[)', raw_text.strip())

parsed_items = []

for block in blocks:
    block = block.strip()
    if not block:
        continue
    
    # Extract number and difficulty
    m = re.match(r'^(?:###\s*)?(\d+)\.\s*\[(Easy|Medium|Hard)\](.*)', block, re.DOTALL)
    if not m:
        continue
    
    q_num = int(m.group(1))
    diff = m.group(2)
    content = m.group(3).strip()
    
    is_chain = "Connection Chain" in content
    
    parsed_items.append({
        "num": q_num,
        "difficulty": diff,
        "content": content,
        "is_chain": is_chain
    })

print(f"Parsed {len(parsed_items)} items.")

# Category rules
def determine_sport(item):
    if item["is_chain"]:
        return "Connection Chains (Multi-Question Sets)"
    
    c = item["content"].lower()
    
    # Check tennis keywords
    tennis_kw = ['grand slam', 'tennis', 'wimbledon', 'us open', 'australian open', 'french open', 'deuce', 'serve', 'baseline', 'volley', 'foot fault', 'tiebreak', 'tie-break', 'racket', 'racquet', 'davis cup', 'billie jean king cup', 'hawk-eye', 'optic yellow', 'ace', 'drop shot', 'backhand', 'forehand', 'clay', 'natural gut', 'advantage', 'break', 'sphairistikè', 'isner', 'mahut', 'stearns', 'hingis', 'navratilova', 'federer', 'nadal', 'djokovic', 'sampras', 'agassi', 'chang', 'goolagong', 'court', 'musketeers', 'alleys', 'service box', 'open era', 'atp', 'wta']
    if any(kw in c for kw in tennis_kw):
        return "Tennis"
    
    # Check basketball keywords
    nba_kw = ['nba', 'basketball', 'fiba', 'wnba', 'celtics', 'lakers', 'bulls', 'knicks', 'spurs', 'warriors', 'raptors', 'hornets', 'supersonics', 'mavericks', 'heat', 'bucks', 'kings', '76ers', 'thunder', 'per', 'triple-double', 'triple double', 'slam dunk', 'skyhook', 'dream shake', 'jordan', 'kobe', 'bryant', 'lebron', 'james', 'curry', 'iverson', 'duncan', 'wilt', 'chamberlain', 'jokić', 'jokic', 'mutombo', 'alvin robertson', 'giannis', 'antetokounmpo', 'westbrook', 'jerry west', 'magic johnson', 'bird', 'olajuwon', 'shaq', 'oneal', 'unseld', 'stockton', 'malone', 'rose', 'maravich', 'wembanyama', 'taurasi', 'auerbach', 'pettit', 'gervin', 'don nelson', 'tex winter', 'sam bowie', 'sam perkins', 'rasheed wallace', 'bobby jones', 'satnam', 'devin booker', 'shai gilgeous-alexander']
    if any(kw in c for kw in nba_kw):
        return "Basketball"
    
    # Check football/soccer keywords
    football_kw = ['football', 'soccer', 'fifa', 'uefa', 'champions league', 'copa américa', 'copa america', 'afcon', 'euro 20', 'euro 19', 'ballon d\'or', 'ballon d’or', 'world cup', 'premier league', 'la liga', 'serie a', 'ligue 1', 'real madrid', 'barcelona', 'manchester united', 'manchester city', 'liverpool', 'arsenal', 'chelsea', 'juventus', 'milan', 'inter', 'bayern', 'dortmund', 'porto', 'sporting', 'ajax', 'psg', 'boca juniors', 'messi', 'ronaldo', 'cr7', 'pelé', 'pele', 'maradona', 'zidane', 'kaká', 'kaka', 'pirlo', 'buffon', 'cannavaro', 'henry', 'solskjær', 'solskjaer', 'alonso', 'iniesta', 'suárez', 'suarez', 'mbappé', 'mbappe', 'klose', 'baggio', 'mourinho', 'casillas', 'weah', 'yashin', 'gullit', 'rodríguez', 'rodriguez', 'van basten', 'red devils', 'the old lady', 'hand of god', 'goal of the century', 'parc des princes', 'anfield', 'maracanã', 'maracana', 'allianz arena', 'signal iduna park', 'camp nou', 'penalty kick', 'red card', 'sending-off', 'substitutions', 'var', 'egyptian king', 'il divin codino', 'the citizens', 'siuuu', 'la pulga', 'o fenômeno']
    if any(kw in c for kw in football_kw):
        return "Football (Soccer)"
        
    # Check cricket keywords
    cricket_kw = ['cricket', 'ipl', 'test', 'odi', 't20', 'ashes', 'tendulkar', 'kohli', 'warne', 'ponting', 'gambhir', 'yuvraj', 'broad', 'lara', 'chhetri', 'kumble', 'dhoni', 'ashwin', 'harbhajan', 'border-gavaskar']
    if any(kw in c for kw in cricket_kw):
        return "Cricket"

    # Check athletics / Olympics keywords
    olympics_kw = ['olympic', 'athletics', '100m', '200m', 'long jump', 'pole vault', 'usain bolt', 'beamon', 'powell', 'duplantis', 'biles', 'gymnastics', 'tokyo 2020', 'paris 2024', 'beijing 2008', 'london 2012']
    if any(kw in c for kw in olympics_kw):
        return "Olympics & Athletics"

    return "Other Sports & General Knowledge"

# Assign sports
categorized = {}
for item in parsed_items:
    sport = determine_sport(item)
    diff = item["difficulty"]
    if sport not in categorized:
        categorized[sport] = {"Easy": [], "Medium": [], "Hard": []}
    categorized[sport][diff].append(item)

# Generate Markdown content
md_lines = []
md_lines.append("# Categorized Sports Quiz (By Sport & Difficulty)\n")
md_lines.append("This document contains all 309 sports quiz questions and connection chains from the master bank, categorized by **Sport / Topic** and sub-divided by **Difficulty Level (Easy, Medium, Hard)**.\n")

# Summary Table
md_lines.append("## Summary Table\n")
md_lines.append("| Sport / Category | Easy | Medium | Hard | Total |")
md_lines.append("| :--- | :---: | :---: | :---: | :---: |")

sport_order = [
    "Football (Soccer)",
    "Basketball",
    "Tennis",
    "Cricket",
    "Olympics & Athletics",
    "Other Sports & General Knowledge",
    "Connection Chains (Multi-Question Sets)"
]

grand_total = 0
for sp in sport_order:
    if sp in categorized:
        e = len(categorized[sp]["Easy"])
        m = len(categorized[sp]["Medium"])
        h = len(categorized[sp]["Hard"])
        tot = e + m + h
        grand_total += tot
        md_lines.append(f"| **{sp}** | {e} | {m} | {h} | **{tot}** |")

md_lines.append(f"| **TOTAL** | **-** | **-** | **-** | **{grand_total}** |\n")
md_lines.append("---\n")

# Detailed Questions
for sp in sport_order:
    if sp not in categorized:
        continue
    
    md_lines.append(f"## {sp}\n")
    
    for diff in ["Easy", "Medium", "Hard"]:
        items = categorized[sp][diff]
        if not items:
            continue
        
        md_lines.append(f"### {diff} ({len(items)} Questions)\n")
        
        for idx, item in enumerate(items, 1):
            md_lines.append(f"#### Q{item['num']}. [{diff}]")
            md_lines.append(f"{item['content']}\n")

md_content = "\n".join(md_lines)

with open("d:\\Case\\Categorized_Sports_Quiz.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Categorized_Sports_Quiz.md generated successfully!")

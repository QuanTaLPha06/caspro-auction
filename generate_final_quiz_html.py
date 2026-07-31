import json

# Read the generated 180 questions JSON
with open("d:\\Case\\questions_db.json", "r", encoding="utf-8") as f:
    questions_data = json.load(f)

questions_json_str = json.dumps(questions_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sports Connection Quiz Arena</title>
  <meta name="description" content="Ultimate Sports Connection & Trivia Quiz with 180 questions across Easy, Medium, and Hard difficulties. Test your sports knowledge in turn-based team play!">
  
  <!-- Modern Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Space+Grotesk:wght@400;600;700&family=Teko:wght@600;700&display=swap" rel="stylesheet">

  <style>
    /* Global CSS Tokens & Variables */
    :root {{
      --bg-dark: #070a12;
      --bg-card: rgba(15, 23, 42, 0.75);
      --bg-card-hover: rgba(30, 41, 59, 0.85);
      --border-color: rgba(255, 255, 255, 0.1);
      
      --cyan-neon: #00f2fe;
      --violet-neon: #7928ca;
      --magenta-neon: #ff007f;
      --gold-neon: #ffc83b;
      --emerald-neon: #00e676;
      --crimson-neon: #ff1744;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      
      --font-heading: 'Teko', sans-serif;
      --font-sub: 'Oswald', sans-serif;
      --font-body: 'Space Grotesk', sans-serif;
      
      --radius-sm: 8px;
      --radius-md: 16px;
      --radius-lg: 24px;
      --shadow-neon: 0 0 25px rgba(0, 242, 254, 0.25);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(121, 40, 202, 0.25) 0%, transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(0, 242, 254, 0.2) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.6) 0%, transparent 100%);
      background-attachment: fixed;
      color: var(--text-main);
      font-family: var(--font-body);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* Header & Navigation */
    header {{
      background: rgba(10, 15, 28, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .logo-box {{
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
    }}

    .logo-icon {{
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--cyan-neon), var(--violet-neon));
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }}

    .logo-text {{
      font-family: var(--font-heading);
      font-size: 2.2rem;
      font-weight: 700;
      letter-spacing: 1px;
      background: linear-gradient(90deg, #fff, var(--cyan-neon));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1;
    }}

    .logo-sub {{
      font-size: 0.75rem;
      color: var(--text-muted);
      letter-spacing: 2px;
      text-transform: uppercase;
    }}

    nav {{
      display: flex;
      gap: 8px;
      background: rgba(255, 255, 255, 0.05);
      padding: 6px;
      border-radius: 50px;
      border: 1px solid var(--border-color);
    }}

    .nav-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 8px 18px;
      font-family: var(--font-sub);
      font-size: 1.05rem;
      letter-spacing: 1px;
      border-radius: 30px;
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .nav-btn:hover {{
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.08);
    }}

    .nav-btn.active {{
      background: linear-gradient(135deg, var(--cyan-neon), var(--violet-neon));
      color: #fff;
      box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }}

    .pool-badge-bar {{
      display: flex;
      gap: 8px;
    }}

    .badge-pill {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-color);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-family: var(--font-sub);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .badge-pill.easy {{ border-color: var(--emerald-neon); color: var(--emerald-neon); }}
    .badge-pill.med {{ border-color: var(--gold-neon); color: var(--gold-neon); }}
    .badge-pill.hard {{ border-color: var(--crimson-neon); color: var(--crimson-neon); }}

    /* Main Container */
    main {{
      flex: 1;
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 2rem 1.5rem;
    }}

    /* Screen Views */
    .screen {{
      display: none;
      animation: fadeIn 0.4s ease forwards;
    }}

    .screen.active {{
      display: block;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* GLASS CARD */
    .glass-card {{
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      padding: 2rem;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
      position: relative;
      overflow: hidden;
    }}

    .glass-card::before {{
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--cyan-neon), transparent);
    }}

    /* SETUP SCREEN */
    .setup-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2rem;
      margin-top: 1.5rem;
    }}

    @media (max-width: 768px) {{
      .setup-grid {{ grid-template-columns: 1fr; }}
    }}

    .section-title {{
      font-family: var(--font-sub);
      font-size: 1.6rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 1rem;
      color: var(--cyan-neon);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .form-group {{
      margin-bottom: 1.25rem;
    }}

    .form-label {{
      display: block;
      font-size: 0.9rem;
      color: var(--text-muted);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}

    .form-input, .form-select {{
      width: 100%;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 12px 16px;
      border-radius: var(--radius-sm);
      font-family: var(--font-body);
      font-size: 1rem;
      outline: none;
      transition: all 0.3s ease;
    }}

    .form-input:focus, .form-select:focus {{
      border-color: var(--cyan-neon);
      box-shadow: 0 0 12px rgba(0, 242, 254, 0.3);
    }}

    .diff-selector {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }}

    .diff-btn {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-color);
      padding: 14px 10px;
      border-radius: var(--radius-sm);
      color: var(--text-muted);
      font-family: var(--font-sub);
      font-size: 1.1rem;
      cursor: pointer;
      text-align: center;
      transition: all 0.3s ease;
    }}

    .diff-btn:hover {{
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-main);
    }}

    .diff-btn.selected[data-diff="easy"] {{ background: rgba(0, 230, 118, 0.2); border-color: var(--emerald-neon); color: var(--emerald-neon); }}
    .diff-btn.selected[data-diff="medium"] {{ background: rgba(255, 200, 59, 0.2); border-color: var(--gold-neon); color: var(--gold-neon); }}
    .diff-btn.selected[data-diff="hard"] {{ background: rgba(255, 23, 68, 0.2); border-color: var(--crimson-neon); color: var(--crimson-neon); }}
    .diff-btn.selected[data-diff="all"] {{ background: rgba(0, 242, 254, 0.2); border-color: var(--cyan-neon); color: var(--cyan-neon); }}

    .btn-large {{
      width: 100%;
      background: linear-gradient(135deg, var(--cyan-neon), var(--violet-neon));
      border: none;
      color: #fff;
      font-family: var(--font-sub);
      font-size: 1.5rem;
      letter-spacing: 2px;
      padding: 16px;
      border-radius: var(--radius-md);
      cursor: pointer;
      box-shadow: 0 10px 30px rgba(0, 242, 254, 0.3);
      transition: all 0.3s ease;
      margin-top: 1rem;
      text-transform: uppercase;
    }}

    .btn-large:hover {{
      transform: translateY(-2px);
      box-shadow: 0 15px 40px rgba(0, 242, 254, 0.5);
    }}

    /* GAME ARENA SCREEN */
    .match-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.5rem;
      gap: 1rem;
    }}

    .team-score-card {{
      flex: 1;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 1rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.3s ease;
    }}

    .team-score-card.active-turn {{
      border-color: var(--cyan-neon);
      box-shadow: 0 0 20px rgba(0, 242, 254, 0.3);
      background: rgba(0, 242, 254, 0.05);
    }}

    .team-name {{
      font-family: var(--font-sub);
      font-size: 1.4rem;
      letter-spacing: 1px;
    }}

    .team-pts {{
      font-family: var(--font-heading);
      font-size: 2.8rem;
      color: var(--cyan-neon);
      line-height: 1;
    }}

    .vs-pill {{
      font-family: var(--font-heading);
      font-size: 2rem;
      color: var(--text-dim);
      padding: 0 10px;
    }}

    .timer-card {{
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 0.8rem 1.5rem;
      text-align: center;
      min-width: 140px;
    }}

    .timer-val {{
      font-family: var(--font-heading);
      font-size: 2.6rem;
      line-height: 1;
      color: var(--gold-neon);
    }}

    .timer-val.warning {{
      color: var(--crimson-neon);
      animation: pulse 1s infinite;
    }}

    @keyframes pulse {{
      0%, 100% {{ transform: scale(1); }}
      50% {{ transform: scale(1.08); }}
    }}

    /* QUESTION ARENA CARD */
    .question-top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .q-meta {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .diff-pill {{
      padding: 4px 12px;
      border-radius: 20px;
      font-family: var(--font-sub);
      font-size: 0.85rem;
      text-transform: uppercase;
    }}

    .diff-pill.easy {{ background: rgba(0, 230, 118, 0.2); color: var(--emerald-neon); border: 1px solid var(--emerald-neon); }}
    .diff-pill.medium {{ background: rgba(255, 200, 59, 0.2); color: var(--gold-neon); border: 1px solid var(--gold-neon); }}
    .diff-pill.hard {{ background: rgba(255, 23, 68, 0.2); color: var(--crimson-neon); border: 1px solid var(--crimson-neon); }}

    .sport-tag {{
      background: rgba(255, 255, 255, 0.08);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.85rem;
      color: var(--text-muted);
    }}

    .points-worth {{
      font-family: var(--font-sub);
      font-size: 1.2rem;
      color: var(--cyan-neon);
      background: rgba(0, 242, 254, 0.1);
      padding: 4px 14px;
      border-radius: 20px;
      border: 1px solid rgba(0, 242, 254, 0.3);
    }}

    .q-title {{
      font-family: var(--font-sub);
      font-size: 1.8rem;
      letter-spacing: 1px;
      margin-bottom: 0.5rem;
    }}

    .q-prompt {{
      color: var(--text-muted);
      font-size: 1rem;
      margin-bottom: 1.5rem;
    }}

    /* PROGRESSIVE CLUES GRID */
    .clues-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
      margin-bottom: 1.5rem;
    }}

    @media (max-width: 640px) {{
      .clues-grid {{ grid-template-columns: 1fr; }}
    }}

    .clue-box {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 1.25rem;
      min-height: 90px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      position: relative;
      transition: all 0.3s ease;
    }}

    .clue-box.revealed {{
      border-color: rgba(0, 242, 254, 0.4);
      background: rgba(0, 242, 254, 0.06);
    }}

    .clue-box.hidden-clue {{
      background: rgba(255, 255, 255, 0.02);
      border-style: dashed;
      cursor: pointer;
      opacity: 0.6;
    }}

    .clue-box.hidden-clue:hover {{
      opacity: 1;
      border-color: var(--cyan-neon);
    }}

    .clue-num {{
      font-family: var(--font-sub);
      font-size: 0.85rem;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }}

    .clue-text {{
      font-size: 1.1rem;
      font-weight: 600;
      color: var(--text-main);
    }}

    .clue-pts-tag {{
      position: absolute;
      top: 10px;
      right: 12px;
      font-family: var(--font-sub);
      font-size: 0.85rem;
      color: var(--gold-neon);
    }}

    /* ANSWER BOX */
    .answer-box {{
      display: none;
      background: linear-gradient(135deg, rgba(0, 230, 118, 0.1), rgba(0, 242, 254, 0.1));
      border: 2px solid var(--emerald-neon);
      border-radius: var(--radius-md);
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      animation: fadeIn 0.3s ease;
    }}

    .answer-box.active {{
      display: block;
    }}

    .ans-title {{
      font-family: var(--font-sub);
      color: var(--emerald-neon);
      font-size: 1.1rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 4px;
    }}

    .ans-text {{
      font-family: var(--font-sub);
      font-size: 1.8rem;
      color: #fff;
      margin-bottom: 8px;
    }}

    .ans-exp {{
      font-size: 0.95rem;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* ACTION CONTROLS BAR */
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 1rem;
    }}

    .btn {{
      padding: 12px 22px;
      border-radius: var(--radius-sm);
      font-family: var(--font-sub);
      font-size: 1.1rem;
      letter-spacing: 1px;
      border: none;
      cursor: pointer;
      transition: all 0.25s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .btn-correct {{
      background: var(--emerald-neon);
      color: #052e16;
      font-weight: 700;
      box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4);
    }}

    .btn-correct:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0, 230, 118, 0.6); }}

    .btn-incorrect {{
      background: rgba(255, 23, 68, 0.2);
      color: var(--crimson-neon);
      border: 1px solid var(--crimson-neon);
    }}

    .btn-incorrect:hover {{ background: var(--crimson-neon); color: #fff; }}

    .btn-clue {{
      background: rgba(0, 242, 254, 0.15);
      color: var(--cyan-neon);
      border: 1px solid var(--cyan-neon);
    }}

    .btn-clue:hover {{ background: var(--cyan-neon); color: #000; }}

    .btn-reveal {{
      background: rgba(255, 200, 59, 0.15);
      color: var(--gold-neon);
      border: 1px solid var(--gold-neon);
    }}

    .btn-reveal:hover {{ background: var(--gold-neon); color: #000; }}

    .btn-secondary {{
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-muted);
      border: 1px solid var(--border-color);
    }}

    .btn-secondary:hover {{ background: rgba(255, 255, 255, 0.12); color: #fff; }}

    /* QUESTION EXPLORER TABLE & CARDS */
    .explorer-bar {{
      display: flex;
      gap: 1rem;
      margin-bottom: 1.5rem;
      flex-wrap: wrap;
    }}

    .search-input {{
      flex: 1;
      min-width: 250px;
    }}

    .q-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
    }}

    .q-card-item {{
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      padding: 1.25rem;
      transition: all 0.3s ease;
    }}

    .q-card-item:hover {{
      border-color: var(--cyan-neon);
      transform: translateY(-3px);
    }}

    .used-badge {{
      background: rgba(255, 23, 68, 0.2);
      color: var(--crimson-neon);
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 10px;
      float: right;
    }}

    .unused-badge {{
      background: rgba(0, 230, 118, 0.2);
      color: var(--emerald-neon);
      font-size: 0.75rem;
      padding: 2px 8px;
      border-radius: 10px;
      float: right;
    }}

    /* SCOREBOARD LOG */
    .log-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
    }}

    .log-table th, .log-table td {{
      padding: 12px 16px;
      text-align: left;
      border-bottom: 1px solid var(--border-color);
    }}

    .log-table th {{
      font-family: var(--font-sub);
      color: var(--cyan-neon);
      text-transform: uppercase;
      letter-spacing: 1px;
    }}

    /* MODAL */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(8px);
      z-index: 200;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }}

    .modal-overlay.active {{
      display: flex;
    }}

    .modal-card {{
      background: var(--bg-card);
      border: 1px solid var(--cyan-neon);
      border-radius: var(--radius-lg);
      padding: 2.5rem;
      max-width: 500px;
      width: 100%;
      text-align: center;
      box-shadow: 0 0 50px rgba(0, 242, 254, 0.3);
    }}

    .winner-title {{
      font-family: var(--font-heading);
      font-size: 3.5rem;
      color: var(--gold-neon);
      line-height: 1;
      margin-bottom: 0.5rem;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border-color);
      padding: 1.5rem;
      text-align: center;
      color: var(--text-dim);
      font-size: 0.85rem;
      margin-top: auto;
    }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header>
    <div class="logo-box" onclick="showScreen('setup-screen')">
      <div class="logo-icon">🏆</div>
      <div>
        <div class="logo-text">SPORTS CONNECTION QUIZ</div>
        <div class="logo-sub">180 Categorized Questions • Easy • Medium • Hard</div>
      </div>
    </div>

    <nav>
      <button class="nav-btn active" id="nav-arena" onclick="showScreen('arena-screen')">🎮 Arena</button>
      <button class="nav-btn" id="nav-scores" onclick="showScreen('scores-screen')">📊 Scoreboard</button>
      <button class="nav-btn" id="nav-bank" onclick="showScreen('bank-screen')">📚 Question Bank</button>
      <button class="nav-btn" id="nav-settings" onclick="showScreen('settings-screen')">⚙️ Settings</button>
    </nav>

    <div class="pool-badge-bar">
      <div class="badge-pill easy">EASY: <span id="stat-easy">60/60</span></div>
      <div class="badge-pill med">MED: <span id="stat-med">60/60</span></div>
      <div class="badge-pill hard">HARD: <span id="stat-hard">60/60</span></div>
    </div>
  </header>

  <main>
    
    <!-- 1. SETUP / START MATCH SCREEN -->
    <div id="setup-screen" class="screen active">
      <div class="glass-card">
        <h2 class="section-title">⚡ Match Setup & Category Selection</h2>
        <p style="color: var(--text-muted); margin-bottom: 1.5rem;">Configure your team names, turn timer, and choose your question difficulty pool.</p>

        <div class="setup-grid">
          <div>
            <div class="form-group">
              <label class="form-label">Team 1 Name</label>
              <input type="text" id="input-team1" class="form-input" value="TITANS" placeholder="Enter Team 1 Name">
            </div>

            <div class="form-group">
              <label class="form-label">Team 2 Name</label>
              <input type="text" id="input-team2" class="form-input" value="WARRIORS" placeholder="Enter Team 2 Name">
            </div>

            <div class="form-group">
              <label class="form-label">Turn Countdown Timer</label>
              <select id="select-timer" class="form-select">
                <option value="0">Untimed (No Timer)</option>
                <option value="30">30 Seconds</option>
                <option value="60" selected>60 Seconds</option>
                <option value="90">90 Seconds</option>
              </select>
            </div>
          </div>

          <div>
            <div class="form-group">
              <label class="form-label">Select Difficulty Pool</label>
              <div class="diff-selector">
                <div class="diff-btn selected" data-diff="easy" onclick="selectDiff('easy')">
                  <div>EASY</div>
                  <div style="font-size:0.75rem; opacity:0.8;">60 Questions</div>
                </div>
                <div class="diff-btn" data-diff="medium" onclick="selectDiff('medium')">
                  <div>MEDIUM</div>
                  <div style="font-size:0.75rem; opacity:0.8;">60 Questions</div>
                </div>
                <div class="diff-btn" data-diff="hard" onclick="selectDiff('hard')">
                  <div>HARD</div>
                  <div style="font-size:0.75rem; opacity:0.8;">60 Questions</div>
                </div>
                <div class="diff-btn" data-diff="all" onclick="selectDiff('all')">
                  <div>ALL / MIX</div>
                  <div style="font-size:0.75rem; opacity:0.8;">180 Questions</div>
                </div>
              </div>
            </div>

            <div class="form-group" style="margin-top: 1.5rem;">
              <label class="form-label">Starting Team</label>
              <select id="select-start-team" class="form-select">
                <option value="team1">Team 1 Starts</option>
                <option value="team2">Team 2 Starts</option>
              </select>
            </div>
          </div>
        </div>

        <button class="btn-large" onclick="startMatch()">🚀 START MATCH NOW</button>
      </div>
    </div>

    <!-- 2. GAME ARENA SCREEN -->
    <div id="arena-screen" class="screen">
      <!-- MATCH SCORE BAR -->
      <div class="match-header">
        <div class="team-score-card active-turn" id="card-team1">
          <div>
            <div class="team-name" id="disp-team1-name">TITANS</div>
            <div style="font-size:0.8rem; color:var(--cyan-neon);" id="disp-team1-status">ACTIVE TURN</div>
          </div>
          <div class="team-pts" id="disp-team1-score">0</div>
        </div>

        <div class="vs-pill">VS</div>

        <div class="team-score-card" id="card-team2">
          <div>
            <div class="team-name" id="disp-team2-name">WARRIORS</div>
            <div style="font-size:0.8rem; color:var(--text-dim);" id="disp-team2-status">WAITING</div>
          </div>
          <div class="team-pts" id="disp-team2-score">0</div>
        </div>

        <div class="timer-card" id="timer-box">
          <div style="font-size:0.75rem; color:var(--text-muted); uppercase;">TURN TIMER</div>
          <div class="timer-val" id="disp-timer">60s</div>
        </div>
      </div>

      <!-- QUESTION ARENA CARD -->
      <div class="glass-card" id="question-card">
        <div class="question-top-bar">
          <div class="q-meta">
            <span class="diff-pill easy" id="q-diff-badge">EASY</span>
            <span class="sport-tag" id="q-sport-badge">⚽ Football</span>
            <span style="font-size:0.85rem; color:var(--text-dim);" id="q-id-badge">ID: E01</span>
          </div>
          <div class="points-worth" id="q-points-badge">4 PTS AVAILABLE</div>
        </div>

        <h2 class="q-title" id="q-title-text">Global Football Legends Connection</h2>
        <p class="q-prompt">Identify the underlying connection linking these progressive clues:</p>

        <!-- CLUES GRID -->
        <div class="clues-grid" id="clues-container">
          <!-- Dynamically populated -->
        </div>

        <!-- ANSWER SECTION -->
        <div class="answer-box" id="answer-box">
          <div class="ans-title">REVEALED CONNECTION & ANSWER:</div>
          <div class="ans-text" id="ans-text-content">Football GOATs / Ballon d'Or & World Cup Icons</div>
          <div class="ans-exp" id="ans-exp-content">All four are widely celebrated as the greatest football players of all time.</div>
        </div>

        <!-- ACTION CONTROLS -->
        <div class="controls-bar">
          <button class="btn btn-correct" onclick="handleTurnOutcome(true)">🟢 CORRECT (+<span id="btn-pts-val">4</span> PTS)</button>
          <button class="btn btn-incorrect" onclick="handleTurnOutcome(false)">🔴 INCORRECT / PASS</button>
          <button class="btn btn-clue" id="btn-reveal-clue" onclick="revealNextClue()">👁️ REVEAL NEXT CLUE</button>
          <button class="btn btn-reveal" onclick="toggleAnswer()">💡 REVEAL ANSWER</button>
          <button class="btn btn-secondary" onclick="undoLastTurn()">↩️ UNDO TURN</button>
          <button class="btn btn-secondary" onclick="skipQuestion()">⏭️ SKIP QUESTION</button>
        </div>
      </div>
    </div>

    <!-- 3. LIVE SCOREBOARD SCREEN -->
    <div id="scores-screen" class="screen">
      <div class="glass-card">
        <h2 class="section-title">📊 Live Scoreboard & Turn Log</h2>
        <div style="display:flex; gap:2rem; margin-bottom:1.5rem;">
          <div style="flex:1; background:rgba(0,242,254,0.1); border:1px solid var(--cyan-neon); padding:1rem; border-radius:12px;">
            <div id="summary-team1-name" style="font-family:var(--font-sub); font-size:1.5rem;">TITANS</div>
            <div id="summary-team1-score" style="font-family:var(--font-heading); font-size:3rem; color:var(--cyan-neon);">0 PTS</div>
          </div>
          <div style="flex:1; background:rgba(121,40,202,0.1); border:1px solid var(--violet-neon); padding:1rem; border-radius:12px;">
            <div id="summary-team2-name" style="font-family:var(--font-sub); font-size:1.5rem;">WARRIORS</div>
            <div id="summary-team2-score" style="font-family:var(--font-heading); font-size:3rem; color:var(--violet-neon);">0 PTS</div>
          </div>
        </div>

        <h3 style="font-family:var(--font-sub); color:var(--text-muted); margin-bottom:0.5rem;">MATCH TURN HISTORY</h3>
        <table class="log-table">
          <thead>
            <tr>
              <th>Turn #</th>
              <th>Team</th>
              <th>Question Title</th>
              <th>Clues Used</th>
              <th>Outcome</th>
              <th>Points</th>
            </tr>
          </thead>
          <tbody id="log-table-body">
            <tr>
              <td colspan="6" style="text-align:center; color:var(--text-dim);">No turns played yet in this match.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 4. QUESTION BANK EXPLORER -->
    <div id="bank-screen" class="screen">
      <div class="glass-card">
        <h2 class="section-title">📚 Question Bank Explorer (180 Questions)</h2>
        
        <div class="explorer-bar">
          <input type="text" id="search-bank" class="form-input search-input" placeholder="Search by sport, clue, keyword, or answer..." oninput="filterQuestionBank()">
          
          <select id="filter-diff" class="form-select" style="width: auto;" onchange="filterQuestionBank()">
            <option value="all">All Difficulties (180)</option>
            <option value="easy">Easy (60)</option>
            <option value="medium">Medium (60)</option>
            <option value="hard">Hard (60)</option>
          </select>

          <select id="filter-status" class="form-select" style="width: auto;" onchange="filterQuestionBank()">
            <option value="all">All Statuses</option>
            <option value="unused">Unused Only</option>
            <option value="used">Used Only</option>
          </select>
        </div>

        <div class="q-grid" id="q-bank-grid">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>

    <!-- 5. SETTINGS SCREEN -->
    <div id="settings-screen" class="screen">
      <div class="glass-card">
        <h2 class="section-title">⚙️ Question Pool Settings & State Management</h2>
        
        <div style="margin-bottom: 2rem;">
          <h3 style="font-family:var(--font-sub); color:var(--text-main); margin-bottom: 0.5rem;">Pool Usage Statistics</h3>
          <p style="color:var(--text-muted); margin-bottom: 1rem;">Questions are automatically marked as used in your browser's localStorage so you never get repeats across games.</p>
          
          <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:12px; border:1px solid var(--border-color);">
              <div style="color:var(--emerald-neon); font-family:var(--font-sub);">EASY POOL</div>
              <div id="settings-easy-count" style="font-size:1.8rem; font-family:var(--font-heading);">0 / 60 Used</div>
            </div>
            <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:12px; border:1px solid var(--border-color);">
              <div style="color:var(--gold-neon); font-family:var(--font-sub);">MEDIUM POOL</div>
              <div id="settings-med-count" style="font-size:1.8rem; font-family:var(--font-heading);">0 / 60 Used</div>
            </div>
            <div style="background:rgba(255,255,255,0.04); padding:1rem; border-radius:12px; border:1px solid var(--border-color);">
              <div style="color:var(--crimson-neon); font-family:var(--font-sub);">HARD POOL</div>
              <div id="settings-hard-count" style="font-size:1.8rem; font-family:var(--font-heading);">0 / 60 Used</div>
            </div>
          </div>
        </div>

        <div style="border-top:1px solid var(--border-color); padding-top:1.5rem;">
          <button class="btn btn-incorrect" style="font-size:1.2rem; padding:14px 24px;" onclick="resetQuestionPool()">🔄 RESET ALL USED QUESTION POOLS</button>
          <p style="color:var(--text-dim); font-size:0.85rem; margin-top:8px;">This will clear recorded used question IDs so all 180 questions become available again.</p>
        </div>
      </div>
    </div>

  </main>

  <!-- WINNER MODAL -->
  <div class="modal-overlay" id="winner-modal">
    <div class="modal-card">
      <div style="font-size:4rem; margin-bottom:0.5rem;">🏆</div>
      <div class="winner-title" id="modal-winner-name">TITANS VICTORY!</div>
      <p style="color:var(--text-muted); font-size:1.1rem; margin-bottom:1.5rem;" id="modal-winner-score">Final Score: 24 - 18</p>
      <button class="btn-large" onclick="closeWinnerModal()">CONTINUE / NEW MATCH</button>
    </div>
  </div>

  <footer>
    Sports Connection Quiz Arena • 180 Questions (60 Easy, 60 Medium, 60 Hard) • Built for High-Energy Sports Trivia
  </footer>

  <!-- EMBEDDED QUESTION DATABASE & JS LOGIC -->
  <script>
    // 180 Questions JSON Database
    const QUESTIONS_DB = {questions_json_str};

    // State Variables
    let gameState = {{
      team1Name: "TITANS",
      team2Name: "WARRIORS",
      team1Score: 0,
      team2Score: 0,
      activeTeam: 1, // 1 or 2
      selectedDiff: "easy",
      timerSec: 60,
      currentTimer: 60,
      timerInterval: null,
      currentQuestion: null,
      revealedCluesCount: 1,
      turnHistory: [],
      usedQuestionIds: new Set()
    }};

    // Load Used Question IDs from LocalStorage
    function loadStorage() {{
      const stored = localStorage.getItem("sports_quiz_used_ids");
      if (stored) {{
        try {{
          const arr = JSON.parse(stored);
          gameState.usedQuestionIds = new Set(arr);
        }} catch(e) {{
          console.error("Failed to parse storage", e);
        }}
      }}
      updatePoolBadges();
    }}

    function saveStorage() {{
      localStorage.setItem("sports_quiz_used_ids", JSON.stringify(Array.from(gameState.usedQuestionIds)));
      updatePoolBadges();
    }}

    function updatePoolBadges() {{
      const easyUsed = Array.from(gameState.usedQuestionIds).filter(id => id.startsWith("E")).length;
      const medUsed = Array.from(gameState.usedQuestionIds).filter(id => id.startsWith("M")).length;
      const hardUsed = Array.from(gameState.usedQuestionIds).filter(id => id.startsWith("H")).length;

      document.getElementById("stat-easy").textContent = `${{60 - easyUsed}}/60`;
      document.getElementById("stat-med").textContent = `${{60 - medUsed}}/60`;
      document.getElementById("stat-hard").textContent = `${{60 - hardUsed}}/60`;

      document.getElementById("settings-easy-count").textContent = `${{easyUsed}} / 60 Used`;
      document.getElementById("settings-med-count").textContent = `${{medUsed}} / 60 Used`;
      document.getElementById("settings-hard-count").textContent = `${{hardUsed}} / 60 Used`;
    }}

    // Screen Switching
    function showScreen(screenId) {{
      document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
      document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));

      document.getElementById(screenId).classList.add("active");
      
      if (screenId === "arena-screen") document.getElementById("nav-arena").classList.add("active");
      if (screenId === "scores-screen") {{
        document.getElementById("nav-scores").classList.add("active");
        renderScoresTable();
      }}
      if (screenId === "bank-screen") {{
        document.getElementById("nav-bank").classList.add("active");
        filterQuestionBank();
      }}
      if (screenId === "settings-screen") document.getElementById("nav-settings").classList.add("active");
    }}

    function selectDiff(diff) {{
      gameState.selectedDiff = diff;
      document.querySelectorAll(".diff-btn").forEach(b => b.classList.remove("selected"));
      document.querySelector(`.diff-btn[data-diff="${{diff}}"]`).classList.add("selected");
    }}

    // Start Match
    function startMatch() {{
      gameState.team1Name = document.getElementById("input-team1").value.trim() || "TITANS";
      gameState.team2Name = document.getElementById("input-team2").value.trim() || "WARRIORS";
      gameState.timerSec = parseInt(document.getElementById("select-timer").value, 10);
      gameState.activeTeam = document.getElementById("select-start-team").value === "team1" ? 1 : 2;
      
      gameState.team1Score = 0;
      gameState.team2Score = 0;
      gameState.turnHistory = [];

      updateScoreDisplay();
      loadNextQuestion();
      showScreen("arena-screen");
    }}

    function updateScoreDisplay() {{
      document.getElementById("disp-team1-name").textContent = gameState.team1Name;
      document.getElementById("disp-team2-name").textContent = gameState.team2Name;
      document.getElementById("disp-team1-score").textContent = gameState.team1Score;
      document.getElementById("disp-team2-score").textContent = gameState.team2Score;

      document.getElementById("summary-team1-name").textContent = gameState.team1Name;
      document.getElementById("summary-team2-name").textContent = gameState.team2Name;
      document.getElementById("summary-team1-score").textContent = `${{gameState.team1Score}} PTS`;
      document.getElementById("summary-team2-score").textContent = `${{gameState.team2Score}} PTS`;

      const card1 = document.getElementById("card-team1");
      const card2 = document.getElementById("card-team2");
      const stat1 = document.getElementById("disp-team1-status");
      const stat2 = document.getElementById("disp-team2-status");

      if (gameState.activeTeam === 1) {{
        card1.classList.add("active-turn");
        card2.classList.remove("active-turn");
        stat1.textContent = "ACTIVE TURN";
        stat1.style.color = "var(--cyan-neon)";
        stat2.textContent = "WAITING";
        stat2.style.color = "var(--text-dim)";
      }} else {{
        card2.classList.add("active-turn");
        card1.classList.remove("active-turn");
        stat2.textContent = "ACTIVE TURN";
        stat2.style.color = "var(--cyan-neon)";
        stat1.textContent = "WAITING";
        stat1.style.color = "var(--text-dim)";
      }}
    }}

    // Load Question from Pool
    function loadNextQuestion() {{
      let pool = [];
      if (gameState.selectedDiff === "all") {{
        pool = QUESTIONS_DB.filter(q => !gameState.usedQuestionIds.has(q.id));
      }} else {{
        pool = QUESTIONS_DB.filter(q => q.difficulty === gameState.selectedDiff && !gameState.usedQuestionIds.has(q.id));
      }}

      if (pool.length === 0) {{
        alert(`The ${{gameState.selectedDiff.toUpperCase()}} question pool is exhausted! Resetting pool...`);
        // Reset pool for this diff
        QUESTIONS_DB.forEach(q => {{
          if (gameState.selectedDiff === "all" || q.difficulty === gameState.selectedDiff) {{
            gameState.usedQuestionIds.delete(q.id);
          }}
        }});
        saveStorage();
        return loadNextQuestion();
      }}

      // Pick random question
      const randIdx = Math.floor(Math.random() * pool.length);
      gameState.currentQuestion = pool[randIdx];
      gameState.revealedCluesCount = 1;

      // Hide answer box
      document.getElementById("answer-box").classList.remove("active");

      // Render Question
      const q = gameState.currentQuestion;
      document.getElementById("q-diff-badge").textContent = q.difficulty.toUpperCase();
      document.getElementById("q-diff-badge").className = `diff-pill ${{q.difficulty}}`;
      document.getElementById("q-sport-badge").textContent = q.sport;
      document.getElementById("q-id-badge").textContent = `ID: ${{q.id}}`;
      document.getElementById("q-title-text").textContent = q.title;

      document.getElementById("ans-text-content").textContent = q.answer;
      document.getElementById("ans-exp-content").textContent = q.explanation;

      renderClues();
      startTimer();
    }}

    function renderClues() {{
      const container = document.getElementById("clues-container");
      container.innerHTML = "";

      const q = gameState.currentQuestion;
      const ptsWorth = 5 - gameState.revealedCluesCount; // Clue 1 = 4pts, Clue 2 = 3pts, Clue 3 = 2pts, Clue 4 = 1pt
      document.getElementById("q-points-badge").textContent = `${{ptsWorth}} PTS AVAILABLE`;
      document.getElementById("btn-pts-val").textContent = ptsWorth;

      q.clues.forEach((clueText, idx) => {{
        const clueNum = idx + 1;
        const clueBox = document.createElement("div");
        
        if (clueNum <= gameState.revealedCluesCount) {{
          clueBox.className = "clue-box revealed";
          clueBox.innerHTML = `
            <div class="clue-num">CLUE ${{clueNum}} (REVEALED)</div>
            <div class="clue-text">${{clueText}}</div>
            <div class="clue-pts-tag">${{5 - clueNum}} PTS</div>
          `;
        }} else {{
          clueBox.className = "clue-box hidden-clue";
          clueBox.onclick = () => revealClueNum(clueNum);
          clueBox.innerHTML = `
            <div class="clue-num">CLUE ${{clueNum}} (LOCKED)</div>
            <div class="clue-text" style="color:var(--text-dim); font-style:italic;">Click to reveal Clue ${{clueNum}}...</div>
            <div class="clue-pts-tag">${{5 - clueNum}} PTS</div>
          `;
        }}
        container.appendChild(clueBox);
      }});

      // Disable reveal button if all revealed
      const revealBtn = document.getElementById("btn-reveal-clue");
      if (gameState.revealedCluesCount >= 4) {{
        revealBtn.style.opacity = "0.5";
        revealBtn.disabled = true;
      }} else {{
        revealBtn.style.opacity = "1";
        revealBtn.disabled = false;
      }}
    }}

    function revealNextClue() {{
      if (gameState.revealedCluesCount < 4) {{
        gameState.revealedCluesCount++;
        renderClues();
      }}
    }}

    function revealClueNum(num) {{
      if (num > gameState.revealedCluesCount) {{
        gameState.revealedCluesCount = num;
        renderClues();
      }}
    }}

    function toggleAnswer() {{
      document.getElementById("answer-box").classList.toggle("active");
    }}

    // Timer Logic
    function startTimer() {{
      clearInterval(gameState.timerInterval);
      const timerBox = document.getElementById("timer-box");
      const disp = document.getElementById("disp-timer");

      if (gameState.timerSec === 0) {{
        timerBox.style.display = "none";
        return;
      }}

      timerBox.style.display = "block";
      gameState.currentTimer = gameState.timerSec;
      disp.textContent = `${{gameState.currentTimer}}s`;
      disp.classList.remove("warning");

      gameState.timerInterval = setInterval(() => {{
        gameState.currentTimer--;
        disp.textContent = `${{gameState.currentTimer}}s`;

        if (gameState.currentTimer <= 10) {{
          disp.classList.add("warning");
        }}

        if (gameState.currentTimer <= 0) {{
          clearInterval(gameState.timerInterval);
          alert(`⏰ Time's Up for ${{gameState.activeTeam === 1 ? gameState.team1Name : gameState.team2Name}}!`);
          handleTurnOutcome(false);
        }}
      }}, 1000);
    }}

    // Handle Turn Outcome
    function handleTurnOutcome(isCorrect) {{
      clearInterval(gameState.timerInterval);

      const ptsEarned = isCorrect ? (5 - gameState.revealedCluesCount) : 0;
      const activeTeamName = gameState.activeTeam === 1 ? gameState.team1Name : gameState.team2Name;

      if (isCorrect) {{
        if (gameState.activeTeam === 1) gameState.team1Score += ptsEarned;
        else gameState.team2Score += ptsEarned;
      }}

      // Record in History
      gameState.turnHistory.push({{
        turnNum: gameState.turnHistory.length + 1,
        teamName: activeTeamName,
        teamId: gameState.activeTeam,
        question: gameState.currentQuestion,
        cluesUsed: gameState.revealedCluesCount,
        isCorrect: isCorrect,
        pts: ptsEarned
      }});

      // Mark Question as Used
      gameState.usedQuestionIds.add(gameState.currentQuestion.id);
      saveStorage();

      // Switch Turn
      gameState.activeTeam = gameState.activeTeam === 1 ? 2 : 1;
      updateScoreDisplay();

      // Load next question
      loadNextQuestion();
    }}

    function undoLastTurn() {{
      if (gameState.turnHistory.length === 0) return;

      const lastTurn = gameState.turnHistory.pop();
      if (lastTurn.isCorrect) {{
        if (lastTurn.teamId === 1) gameState.team1Score -= lastTurn.pts;
        else gameState.team2Score -= lastTurn.pts;
      }}

      gameState.usedQuestionIds.delete(lastTurn.question.id);
      saveStorage();

      gameState.activeTeam = lastTurn.teamId;
      gameState.currentQuestion = lastTurn.question;
      gameState.revealedCluesCount = lastTurn.cluesUsed;

      updateScoreDisplay();
      renderClues();
      startTimer();
    }}

    function skipQuestion() {{
      loadNextQuestion();
    }}

    // Render Scores Table
    function renderScoresTable() {{
      const tbody = document.getElementById("log-table-body");
      if (gameState.turnHistory.length === 0) {{
        tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:var(--text-dim);">No turns played yet.</td></tr>`;
        return;
      }}

      tbody.innerHTML = "";
      gameState.turnHistory.forEach(t => {{
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>#${{t.turnNum}}</td>
          <td><strong>${{t.teamName}}</strong></td>
          <td>${{t.question.title}}</td>
          <td>${{t.cluesUsed}} / 4</td>
          <td><span style="color: ${{t.isCorrect ? 'var(--emerald-neon)' : 'var(--crimson-neon)'}}">${{t.isCorrect ? '✓ Correct' : '✗ Pass'}}</span></td>
          <td><strong>+${{t.pts}} PTS</strong></td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Filter Question Bank Explorer
    function filterQuestionBank() {{
      const query = document.getElementById("search-bank").value.toLowerCase();
      const diffFilter = document.getElementById("filter-diff").value;
      const statusFilter = document.getElementById("filter-status").value;

      const grid = document.getElementById("q-bank-grid");
      grid.innerHTML = "";

      const filtered = QUESTIONS_DB.filter(q => {{
        const isUsed = gameState.usedQuestionIds.has(q.id);

        if (diffFilter !== "all" && q.difficulty !== diffFilter) return false;
        if (statusFilter === "used" && !isUsed) return false;
        if (statusFilter === "unused" && isUsed) return false;

        if (query) {{
          const fullStr = `${{q.id}} ${{q.title}} ${{q.sport}} ${{q.answer}} ${{q.clues.join(" ")}}`.toLowerCase();
          if (!fullStr.includes(query)) return false;
        }}

        return true;
      }});

      filtered.forEach(q => {{
        const isUsed = gameState.usedQuestionIds.has(q.id);
        const card = document.createElement("div");
        card.className = "q-card-item";
        card.innerHTML = `
          <div>
            ${{isUsed ? '<span class="used-badge">USED</span>' : '<span class="unused-badge">AVAILABLE</span>'}}
            <span class="diff-pill ${{q.difficulty}}">${{q.difficulty.toUpperCase()}}</span>
            <span class="sport-tag" style="font-size:0.75rem; margin-left:6px;">${{q.sport}}</span>
          </div>
          <h4 style="font-family:var(--font-sub); font-size:1.2rem; margin:10px 0 4px 0;">${{q.title}}</h4>
          <p style="font-size:0.85rem; color:var(--cyan-neon); margin-bottom:8px;">Ans: ${{q.answer}}</p>
          <div style="font-size:0.8rem; color:var(--text-dim); border-top:1px solid rgba(255,255,255,0.05); padding-top:6px;">
            ${{q.clues[0]}}<br>
            ${{q.clues[1]}}
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function resetQuestionPool() {{
      if (confirm("Are you sure you want to reset all used question pools? All 180 questions will become available again.")) {{
        gameState.usedQuestionIds.clear();
        saveStorage();
        alert("Question pool successfully reset!");
      }}
    }}

    function closeWinnerModal() {{
      document.getElementById("winner-modal").classList.remove("active");
      showScreen("setup-screen");
    }}

    // Init App
    window.addEventListener("DOMContentLoaded", () => {{
      loadStorage();
    }});
  </script>

</body>
</html>
"""

# Write to Sports_Connection_Quiz.html
with open("d:\\Case\\Sports_Connection_Quiz.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Copy to index.html
with open("d:\\Case\\index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Sports_Connection_Quiz.html and index.html generated successfully!")

import json
import os

def generate_cascade_html():
    questions_file = "cascade_questions.json"
    with open(questions_file, "r", encoding="utf-8") as f:
        questions_data = json.load(f)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CASCADE - Sports Objective Feud</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Teko:wght@600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-dark: #070b12;
    --bg-card: #0f172a;
    --border-color: #1e293b;
    --accent-blue: #00d2ff;
    --accent-green: #10b981;
    --accent-gold: #fbbf24;
    --accent-red: #ef4444;
    --accent-purple: #a855f7;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --card-gradient: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    --gold-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    --purple-gradient: linear-gradient(135deg, #a855f7 0%, #7e22ce 100%);
    --font-heading: 'Teko', sans-serif;
    --font-sub: 'Oswald', sans-serif;
    --font-body: 'Space Grotesk', sans-serif;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
  }}

  body {{
    font-family: var(--font-body);
    background-color: var(--bg-dark);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow-x: hidden;
    background-image: 
      radial-gradient(circle at 50% 0%, rgba(0, 210, 255, 0.12) 0%, transparent 60%),
      radial-gradient(circle at 100% 100%, rgba(168, 85, 247, 0.08) 0%, transparent 50%);
  }}

  /* Global Nav */
  .top-nav {{
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    padding: 0.75rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
  }}

  .nav-brand {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: var(--font-heading);
    font-size: 2rem;
    letter-spacing: 2px;
    color: var(--text-main);
    text-transform: uppercase;
  }}

  .nav-brand span {{
    color: var(--accent-blue);
    text-shadow: 0 0 12px rgba(0, 210, 255, 0.5);
  }}

  .nav-links {{
    display: flex;
    gap: 0.75rem;
  }}

  .nav-btn {{
    background: #1e293b;
    color: var(--text-muted);
    border: 1px solid var(--border-color);
    padding: 0.4rem 0.9rem;
    border-radius: 6px;
    font-family: var(--font-sub);
    font-size: 0.95rem;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
  }}

  .nav-btn:hover, .nav-btn.active {{
    background: var(--accent-blue);
    color: #000;
    border-color: var(--accent-blue);
    font-weight: 600;
    box-shadow: 0 0 10px rgba(0, 210, 255, 0.4);
  }}

  /* Container */
  .main-container {{
    max-width: 1280px;
    width: 100%;
    margin: 0 auto;
    padding: 1.5rem;
    flex: 1;
    display: flex;
    flex-direction: column;
  }}

  /* SETUP SCREEN */
  #setup-screen {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    gap: 2rem;
    text-align: center;
  }}

  .setup-card {{
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 2.5rem;
    max-width: 650px;
    width: 100%;
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
  }}

  .setup-title {{
    font-family: var(--font-heading);
    font-size: 3.5rem;
    letter-spacing: 3px;
    line-height: 1;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #fff 0%, var(--accent-blue) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  .setup-subtitle {{
    color: var(--text-muted);
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }}

  .form-group {{
    margin-bottom: 1.5rem;
    text-align: left;
  }}

  .form-group label {{
    display: block;
    font-family: var(--font-sub);
    color: var(--accent-blue);
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
  }}

  .team-inputs {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }}

  .input-field {{
    width: 100%;
    background: #090e17;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    color: #fff;
    font-family: var(--font-body);
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
  }}

  .input-field:focus {{
    border-color: var(--accent-blue);
  }}

  .btn-start {{
    background: linear-gradient(135deg, #00d2ff 0%, #0072ff 100%);
    color: #000;
    border: none;
    padding: 1rem 3rem;
    font-family: var(--font-heading);
    font-size: 2rem;
    letter-spacing: 2px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
    width: 100%;
    margin-top: 1rem;
  }}

  .btn-start:hover {{
    transform: translateY(-2px);
    box-shadow: 0 0 30px rgba(0, 210, 255, 0.7);
  }}

  /* GAMEPLAY SCREEN */
  #game-screen {{
    display: none;
    flex-direction: column;
    gap: 1.25rem;
  }}

  /* Question Header Header */
  .q-header-card {{
    background: var(--card-gradient);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.25rem 1.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
  }}

  .q-header-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 5px;
    height: 100%;
    background: var(--accent-blue);
  }}

  .q-meta {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.3rem;
  }}

  .sport-badge {{
    background: rgba(0, 210, 255, 0.15);
    color: var(--accent-blue);
    border: 1px solid rgba(0, 210, 255, 0.3);
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-family: var(--font-sub);
    font-size: 0.85rem;
    letter-spacing: 1px;
    text-transform: uppercase;
  }}

  .q-tracker {{
    color: var(--text-muted);
    font-family: var(--font-sub);
    font-size: 0.95rem;
  }}

  .q-title {{
    font-family: var(--font-heading);
    font-size: 2.2rem;
    letter-spacing: 1px;
    line-height: 1.1;
    color: #fff;
  }}

  .q-subtitle {{
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-top: 0.2rem;
  }}

  /* Turn Status Banner */
  .turn-banner {{
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 0.75rem 1.25rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .current-turn-indicator {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-family: var(--font-sub);
    font-size: 1.25rem;
    letter-spacing: 1px;
  }}

  .turn-dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 10px var(--accent-green);
    animation: pulse 1.5s infinite;
  }}

  @keyframes pulse {{
    0% {{ transform: scale(0.95); opacity: 0.8; }}
    50% {{ transform: scale(1.15); opacity: 1; }}
    100% {{ transform: scale(0.95); opacity: 0.8; }}
  }}

  .guess-tracker-badge {{
    background: #1e293b;
    border: 1px solid var(--border-color);
    padding: 0.35rem 0.85rem;
    border-radius: 6px;
    font-size: 0.85rem;
    color: var(--text-muted);
  }}

  .guess-tracker-badge.eligible {{
    border-color: var(--accent-purple);
    color: var(--accent-purple);
  }}

  .guess-tracker-badge.locked {{
    border-color: var(--accent-red);
    color: var(--accent-red);
  }}

  /* PROMINENT TYPING ANSWER BAR */
  .typing-answer-section {{
    background: linear-gradient(135deg, rgba(0, 210, 255, 0.1) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 2px solid var(--accent-blue);
    border-radius: 14px;
    padding: 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    box-shadow: 0 0 25px rgba(0, 210, 255, 0.2);
  }}

  .typing-label {{
    font-family: var(--font-sub);
    font-size: 1.1rem;
    color: var(--accent-blue);
    letter-spacing: 1px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .typing-input-row {{
    display: flex;
    gap: 1rem;
  }}

  .big-type-input {{
    flex: 1;
    background: #090e17;
    border: 2px solid var(--border-color);
    border-radius: 10px;
    padding: 0.9rem 1.25rem;
    color: #fff;
    font-family: var(--font-body);
    font-size: 1.25rem;
    outline: none;
    transition: all 0.2s ease;
  }}

  .big-type-input:focus {{
    border-color: var(--accent-blue);
    box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
  }}

  .btn-submit-guess {{
    background: linear-gradient(135deg, #00d2ff 0%, #0072ff 100%);
    color: #000;
    border: none;
    padding: 0 2rem;
    font-family: var(--font-heading);
    font-size: 1.6rem;
    letter-spacing: 1px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
  }}

  .btn-submit-guess:hover {{
    transform: translateY(-2px);
    box-shadow: 0 0 20px rgba(0, 210, 255, 0.6);
  }}

  /* FEEDBACK POSITION TOAST/BANNER */
  .position-feedback-toast {{
    display: none;
    background: var(--gold-gradient);
    color: #000;
    border-radius: 10px;
    padding: 0.85rem 1.25rem;
    font-family: var(--font-heading);
    font-size: 2rem;
    letter-spacing: 2px;
    text-align: center;
    box-shadow: 0 0 25px rgba(251, 191, 36, 0.6);
    animation: toastPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  }}

  @keyframes toastPop {{
    from {{ transform: scale(0.7); opacity: 0; }}
    to {{ transform: scale(1); opacity: 1; }}
  }}

  /* Family Feud Board Grid */
  .board-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin: 0.5rem 0;
  }}

  @media(max-width: 768px) {{
    .board-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .answer-card {{
    background: #0e1726;
    border: 2px solid #1e293b;
    border-radius: 10px;
    height: 70px;
    display: flex;
    align-items: center;
    padding: 0 1.25rem;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }}

  .answer-card:hover {{
    border-color: var(--accent-blue);
    transform: translateY(-2px);
  }}

  .answer-card.revealed {{
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-color: var(--accent-gold);
    box-shadow: 0 0 15px rgba(251, 191, 36, 0.2);
  }}

  .answer-card.just-revealed {{
    animation: flashCard 0.6s ease;
  }}

  @keyframes flashCard {{
    0% {{ transform: scale(1); border-color: #fff; box-shadow: 0 0 30px #fff; }}
    50% {{ transform: scale(1.04); border-color: var(--accent-gold); box-shadow: 0 0 40px var(--accent-gold); }}
    100% {{ transform: scale(1); }}
  }}

  .card-rank {{
    font-family: var(--font-heading);
    font-size: 2.2rem;
    color: var(--accent-blue);
    width: 45px;
    text-align: center;
    line-height: 1;
  }}

  .answer-card.revealed .card-rank {{
    color: var(--accent-gold);
  }}

  .card-content {{
    flex: 1;
    padding: 0 1rem;
  }}

  .card-name {{
    font-family: var(--font-sub);
    font-size: 1.35rem;
    letter-spacing: 0.5px;
    color: #fff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  .card-detail {{
    font-size: 0.8rem;
    color: var(--text-muted);
  }}

  .card-unrevealed-text {{
    font-family: var(--font-heading);
    font-size: 1.8rem;
    color: #334155;
    letter-spacing: 2px;
  }}

  .card-points {{
    background: #1e293b;
    color: var(--accent-gold);
    border: 1px solid rgba(251, 191, 36, 0.4);
    font-family: var(--font-heading);
    font-size: 1.5rem;
    padding: 0.2rem 0.75rem;
    border-radius: 6px;
    min-width: 45px;
    text-align: center;
  }}

  .card-hidden-points {{
    background: #090e17;
    color: #334155;
    border: 1px solid #1e293b;
    font-family: var(--font-heading);
    font-size: 1.5rem;
    padding: 0.2rem 0.75rem;
    border-radius: 6px;
    min-width: 45px;
    text-align: center;
  }}

  /* Controls Section */
  .controls-bar {{
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: wrap;
  }}

  .btn-action {{
    background: #1e293b;
    color: #fff;
    border: 1px solid var(--border-color);
    padding: 0.65rem 1.25rem;
    border-radius: 8px;
    font-family: var(--font-sub);
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}

  .btn-action:hover {{
    background: #334155;
  }}

  .btn-strike {{
    background: rgba(239, 68, 68, 0.15);
    color: var(--accent-red);
    border-color: rgba(239, 68, 68, 0.4);
  }}

  .btn-strike:hover {{
    background: var(--accent-red);
    color: #fff;
  }}

  .btn-reveal {{
    background: rgba(251, 191, 36, 0.15);
    color: var(--accent-gold);
    border-color: rgba(251, 191, 36, 0.4);
  }}

  .btn-reveal:hover {{
    background: var(--accent-gold);
    color: #000;
  }}

  .btn-next {{
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: #fff;
    border: none;
    font-weight: 600;
  }}

  .btn-next:hover {{
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
  }}

  /* Scoreboard & Trump Card Section */
  .teams-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
  }}

  .team-card {{
    background: var(--card-gradient);
    border: 2px solid var(--border-color);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    transition: all 0.3s ease;
    position: relative;
  }}

  .team-card.active-turn {{
    border-color: var(--accent-green);
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.25);
  }}

  .team-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .team-name {{
    font-family: var(--font-heading);
    font-size: 1.6rem;
    letter-spacing: 1px;
    color: #fff;
  }}

  .team-score {{
    font-family: var(--font-heading);
    font-size: 2.2rem;
    color: var(--accent-gold);
    line-height: 1;
  }}

  .trump-section {{
    border-top: 1px solid var(--border-color);
    padding-top: 0.75rem;
  }}

  .btn-trump {{
    width: 100%;
    background: var(--purple-gradient);
    color: #fff;
    border: none;
    padding: 0.65rem 1rem;
    border-radius: 8px;
    font-family: var(--font-sub);
    font-size: 1rem;
    letter-spacing: 1px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
  }}

  .btn-trump:hover:not(:disabled) {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5);
  }}

  .btn-trump:disabled {{
    background: #1e293b;
    color: #475569;
    cursor: not-allowed;
    box-shadow: none;
    border: 1px solid #334155;
  }}

  .trump-count {{
    background: rgba(0,0,0,0.3);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.85rem;
  }}

  /* Strikes Display */
  .strikes-bar {{
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    font-family: var(--font-heading);
    font-size: 2rem;
    color: var(--accent-red);
    height: 35px;
  }}

  .strike-x {{
    animation: bounceIn 0.3s ease;
  }}

  @keyframes bounceIn {{
    0% {{ transform: scale(0); }}
    70% {{ transform: scale(1.3); }}
    100% {{ transform: scale(1); }}
  }}

  /* Modal Overlay */
  .modal-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.85);
    backdrop-filter: blur(8px);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }}

  .modal-box {{
    background: var(--bg-card);
    border: 2px solid var(--accent-blue);
    border-radius: 16px;
    padding: 2.5rem;
    max-width: 550px;
    width: 90%;
    text-align: center;
    box-shadow: 0 0 40px rgba(0, 210, 255, 0.4);
    animation: modalPop 0.3s ease;
  }}

  @keyframes modalPop {{
    from {{ transform: scale(0.8); opacity: 0; }}
    to {{ transform: scale(1); opacity: 1; }}
  }}

  .modal-title {{
    font-family: var(--font-heading);
    font-size: 3rem;
    color: var(--accent-gold);
    letter-spacing: 2px;
  }}

  .modal-msg {{
    font-size: 1.2rem;
    margin: 1rem 0 2rem 0;
    color: var(--text-main);
  }}

  /* Victory Screen */
  #victory-screen {{
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 75vh;
    text-align: center;
    gap: 2rem;
  }}

  .winner-card {{
    background: var(--card-gradient);
    border: 3px solid var(--accent-gold);
    border-radius: 20px;
    padding: 3rem;
    max-width: 600px;
    width: 100%;
    box-shadow: 0 0 50px rgba(251, 191, 36, 0.4);
  }}

  .winner-crown {{
    font-size: 4rem;
    margin-bottom: 0.5rem;
  }}

  .winner-name {{
    font-family: var(--font-heading);
    font-size: 4rem;
    color: var(--accent-gold);
    letter-spacing: 2px;
  }}

  .winner-score {{
    font-family: var(--font-sub);
    font-size: 2rem;
    color: var(--accent-blue);
    margin-bottom: 2rem;
  }}

  .standings-list {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    text-align: left;
    margin-bottom: 2rem;
  }}

  .standing-item {{
    background: #090e17;
    border: 1px solid var(--border-color);
    padding: 0.85rem 1.25rem;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    font-family: var(--font-sub);
    font-size: 1.2rem;
  }}
</style>
</head>
<body>

  <!-- Top Navigation -->
  <nav class="top-nav">
    <div class="nav-brand">
      ⚡ <span>CASCADE</span> SPORTS FEUD
    </div>
    <div class="nav-links">
      <a href="/" class="nav-btn">🏠 ALL GAMES HUB</a>
      <a href="/cascade" class="nav-btn active">CASCADE FEUD</a>
      <a href="/heads-up" class="nav-btn">HEADS UP!</a>
      <a href="/quiz" class="nav-btn">SPORTS QUIZ</a>
    </div>
  </nav>

  <div class="main-container">

    <!-- 1. SETUP SCREEN -->
    <div id="setup-screen">
      <div class="setup-card">
        <h1 class="setup-title">CASCADE</h1>
        <p class="setup-subtitle">Objective Sports Family Feud • Rank 1 to 8 • 3 Trump Cards Per Team</p>
        
        <div class="form-group">
          <label>Number of Teams</label>
          <select id="team-count-select" class="input-field" onchange="updateTeamInputs()">
            <option value="2" selected>2 Teams</option>
            <option value="3">3 Teams</option>
            <option value="4">4 Teams</option>
          </select>
        </div>

        <div class="form-group">
          <label>Team Names</label>
          <div id="team-inputs-container" class="team-inputs">
            <input type="text" id="team-name-0" class="input-field" value="Team Alpha">
            <input type="text" id="team-name-1" class="input-field" value="Team Beta">
          </div>
        </div>

        <div class="form-group">
          <label>Questions per Game</label>
          <select id="q-count-select" class="input-field">
            <option value="6">6 Questions (Quick Round)</option>
            <option value="12" selected>12 Questions (Standard Game)</option>
            <option value="24">24 Questions (Full Master Tournament)</option>
          </select>
        </div>

        <button class="btn-start" onclick="startGame()">START GAME</button>
      </div>
    </div>

    <!-- 2. GAMEPLAY SCREEN -->
    <div id="game-screen">
      
      <!-- Question Header -->
      <div class="q-header-card">
        <div>
          <div class="q-meta">
            <span id="sport-tag" class="sport-badge">FOOTBALL</span>
            <span id="question-tracker" class="q-tracker">QUESTION 1 OF 12</span>
          </div>
          <h2 id="q-title" class="q-title">All-Time Top Men's International Goalscorers</h2>
          <p id="q-subtitle" class="q-subtitle">Rank the top 8 all-time highest goal scorers in men's international football history.</p>
        </div>
      </div>

      <!-- Turn Status & Trump Eligibility Banner -->
      <div class="turn-banner">
        <div class="current-turn-indicator">
          <div class="turn-dot"></div>
          <span>CURRENT TURN: <strong id="active-team-display" style="color: var(--accent-green);">TEAM ALPHA</strong></span>
        </div>
        <div class="strikes-bar" id="strikes-display"></div>
        <div id="trump-eligibility-badge" class="guess-tracker-badge eligible">
          ⚡ TRUMP CARDS ALLOWED (0/2 Guesses Made)
        </div>
      </div>

      <!-- PROMINENT TYPING ANSWER INPUT AREA -->
      <div class="typing-answer-section">
        <div class="typing-label">
          <span>✍️ TYPE YOUR ANSWER BELOW:</span>
          <span style="font-size: 0.9rem; color: var(--text-muted);">Press Enter or click SUBMIT</span>
        </div>
        <div class="typing-input-row">
          <input type="text" id="guess-input" class="big-type-input" placeholder="Type player/country/team name..." onkeyup="handleKeySearch(event)">
          <button class="btn-submit-guess" onclick="submitTypedAnswer()">SUBMIT ANSWER [ENTER]</button>
        </div>
        <!-- POSITION FEEDBACK TOAST -->
        <div id="position-toast" class="position-feedback-toast">
          🎯 POSITION #1 REVEALED! Lionel Messi (+8 PTS)
        </div>
      </div>

      <!-- 8 Answer Cards Grid -->
      <div class="board-grid" id="board-grid">
        <!-- Rendered dynamically -->
      </div>

      <!-- Guesser / Host Controls -->
      <div class="controls-bar">
        <button class="btn-action btn-strike" onclick="addStrike()">❌ WRONG GUESS (STRIKE)</button>
        <button class="btn-action btn-reveal" onclick="revealAll()">👁️ REVEAL ALL</button>
        <button class="btn-action btn-next" onclick="nextQuestion()">NEXT QUESTION ➔</button>
      </div>

      <!-- Team Scoreboard & Trump Cards -->
      <div class="teams-container" id="teams-scoreboard">
        <!-- Rendered dynamically -->
      </div>

    </div>

    <!-- 3. VICTORY / FINAL SCREEN -->
    <div id="victory-screen">
      <div class="winner-card">
        <div class="winner-crown">🏆</div>
        <h1 class="winner-name" id="winner-team-name">TEAM ALPHA</h1>
        <p class="winner-score" id="winner-score-display">CHAMPIONS • 48 POINTS</p>
        
        <div class="standings-list" id="final-standings-list">
          <!-- Final scores -->
        </div>

        <button class="btn-start" onclick="resetToSetup()">PLAY NEW GAME</button>
      </div>
    </div>

  </div>

  <!-- Notification Modal -->
  <div id="modal-overlay" class="modal-overlay">
    <div class="modal-box">
      <h2 id="modal-title" class="modal-title">TRUMP CARD!</h2>
      <p id="modal-msg" class="modal-msg">Team Beta has hijacked the turn!</p>
      <button class="btn-action btn-next" style="margin: 0 auto;" onclick="closeModal()">CONTINUE</button>
    </div>
  </div>

  <script>
    // Embedded Cascade Questions Database
    const ALL_QUESTIONS = {json.dumps(questions_data, indent=2)};

    // Audio Controller (Web Audio API)
    class SoundFx {{
      constructor() {{
        this.ctx = null;
      }}
      init() {{
        if (!this.ctx) {{
          this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }}
      }}
      playCorrect() {{
        this.init();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, this.ctx.currentTime); // C5
        osc.frequency.exponentialRampToValueAtTime(659.25, this.ctx.currentTime + 0.1); // E5
        osc.frequency.exponentialRampToValueAtTime(783.99, this.ctx.currentTime + 0.2); // G5
        gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.4);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.4);
      }}
      playWrong() {{
        this.init();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, this.ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(90, this.ctx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.4, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + 0.3);
      }}
      playTrump() {{
        this.init();
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.setValueAtTime(554.37, now + 0.1);
        osc.frequency.setValueAtTime(659.25, now + 0.2);
        osc.frequency.setValueAtTime(880, now + 0.3);
        gain.gain.setValueAtTime(0.5, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.6);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(now + 0.6);
      }}
    }}

    const sound = new SoundFx();

    // Game State
    let gameState = {{
      teams: [],
      questions: [],
      currentQIndex: 0,
      activeTeamIndex: 0,
      currentQGuesses: 0,
      currentQTrumped: false,
      revealedAnswers: [],
      strikes: 0,
      lastRevealedIdx: null
    }};

    function updateTeamInputs() {{
      const count = parseInt(document.getElementById('team-count-select').value);
      const container = document.getElementById('team-inputs-container');
      container.innerHTML = '';
      const defaultNames = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta"];
      for (let i = 0; i < count; i++) {{
        const input = document.createElement('input');
        input.type = 'text';
        input.id = `team-name-${{i}}`;
        input.className = 'input-field';
        input.value = defaultNames[i] || `Team ${{i+1}}`;
        container.appendChild(input);
      }}
    }}

    function startGame() {{
      const teamCount = parseInt(document.getElementById('team-count-select').value);
      const qCount = parseInt(document.getElementById('q-count-select').value);

      gameState.teams = [];
      for (let i = 0; i < teamCount; i++) {{
        const name = document.getElementById(`team-name-${{i}}`).value.trim() || `Team ${{i+1}}`;
        gameState.teams.push({{
          id: i,
          name: name,
          score: 0,
          trumpsRemaining: 3
        }});
      }}

      // Shuffle and pick questions
      const shuffled = [...ALL_QUESTIONS].sort(() => Math.random() - 0.5);
      gameState.questions = shuffled.slice(0, qCount);
      gameState.currentQIndex = 0;
      gameState.activeTeamIndex = 0;

      document.getElementById('setup-screen').style.display = 'none';
      document.getElementById('victory-screen').style.display = 'none';
      document.getElementById('game-screen').style.display = 'flex';

      loadQuestion(0);
    }}

    function loadQuestion(index) {{
      if (index >= gameState.questions.length) {{
        showVictory();
        return;
      }}

      gameState.currentQIndex = index;
      gameState.currentQGuesses = 0;
      gameState.currentQTrumped = false;
      gameState.revealedAnswers = new Array(8).fill(false);
      gameState.strikes = 0;
      gameState.lastRevealedIdx = null;

      const q = gameState.questions[index];
      document.getElementById('sport-tag').innerText = q.sport.toUpperCase();
      document.getElementById('question-tracker').innerText = `QUESTION ${{index + 1}} OF ${{gameState.questions.length}}`;
      document.getElementById('q-title').innerText = q.title;
      document.getElementById('q-subtitle').innerText = q.subtitle;
      document.getElementById('guess-input').value = '';
      document.getElementById('position-toast').style.display = 'none';

      renderBoard();
      updateTurnDisplay();
      renderScoreboard();
    }}

    function renderBoard() {{
      const board = document.getElementById('board-grid');
      board.innerHTML = '';

      const q = gameState.questions[gameState.currentQIndex];
      q.answers.forEach((ans, idx) => {{
        const card = document.createElement('div');
        const isRevealed = gameState.revealedAnswers[idx];
        const isJustRevealed = (gameState.lastRevealedIdx === idx);
        card.className = `answer-card ${{isRevealed ? 'revealed' : ''}} ${{isJustRevealed ? 'just-revealed' : ''}}`;
        card.onclick = () => toggleReveal(idx);

        if (isRevealed) {{
          card.innerHTML = `
            <div class="card-rank">#${{ans.rank}}</div>
            <div class="card-content">
              <div class="card-name">${{ans.name}}</div>
              <div class="card-detail">${{ans.detail}}</div>
            </div>
            <div class="card-points">+${{ans.points}}</div>
          `;
        }} else {{
          card.innerHTML = `
            <div class="card-rank">#${{ans.rank}}</div>
            <div class="card-content">
              <div class="card-unrevealed-text">?????????</div>
            </div>
            <div class="card-hidden-points">${{ans.points}} PTS</div>
          `;
        }}
        board.appendChild(card);
      }});
    }}

    function showPositionToast(ans, rank) {{
      const toast = document.getElementById('position-toast');
      toast.style.display = 'block';
      toast.style.background = 'var(--gold-gradient)';
      toast.style.color = '#000';
      toast.innerText = `🎯 MATCH FOUND! POSITION #${{rank}} REVEALED: ${{ans.name}} (+${{ans.points}} PTS)`;
    }}

    function showWrongToast(typedText) {{
      const toast = document.getElementById('position-toast');
      toast.style.display = 'block';
      toast.style.background = 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)';
      toast.style.color = '#fff';
      toast.innerText = `❌ INCORRECT GUESS: "${{typedText}}" NOT FOUND IN TOP 8!`;
    }}

    function toggleReveal(idx) {{
      if (!gameState.revealedAnswers[idx]) {{
        gameState.revealedAnswers[idx] = true;
        gameState.lastRevealedIdx = idx;
        sound.playCorrect();
        
        const ans = gameState.questions[gameState.currentQIndex].answers[idx];
        showPositionToast(ans, ans.rank);

        // Award points to current active team
        gameState.teams[gameState.activeTeamIndex].score += ans.points;

        // Register guess made
        registerGuessMade();
        renderBoard();
        renderScoreboard();
      }}
    }}

    function submitTypedAnswer() {{
      const input = document.getElementById('guess-input');
      const val = input.value.toLowerCase().trim();
      if (!val) return;

      const answers = gameState.questions[gameState.currentQIndex].answers;
      let matchedIdx = -1;

      // Clean string helper for fuzzy matching
      const clean = (s) => s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/[^a-z0-9 ]/g, "");
      const cleanVal = clean(val);

      answers.forEach((ans, idx) => {{
        if (!gameState.revealedAnswers[idx]) {{
          const cleanName = clean(ans.name);
          const cleanDetail = clean(ans.detail);

          // Check if typed string matches or is contained in answer name/detail
          if (cleanName.includes(cleanVal) || cleanVal.includes(cleanName) || cleanDetail.includes(cleanVal)) {{
            matchedIdx = idx;
          }}
        }}
      }});

      if (matchedIdx !== -1) {{
        toggleReveal(matchedIdx);
        input.value = '';
      }} else {{
        showWrongToast(val);
        addStrike();
        input.value = '';
      }}
    }}

    function handleKeySearch(event) {{
      if (event.key === 'Enter') {{
        submitTypedAnswer();
      }}
    }}

    function registerGuessMade() {{
      gameState.currentQGuesses++;
      updateTurnDisplay();
      renderScoreboard();
    }}

    function addStrike() {{
      gameState.strikes++;
      sound.playWrong();
      registerGuessMade();

      // Rotate turn to next team
      gameState.activeTeamIndex = (gameState.activeTeamIndex + 1) % gameState.teams.length;
      updateTurnDisplay();
      renderScoreboard();
    }}

    function updateTurnDisplay() {{
      const activeTeam = gameState.teams[gameState.activeTeamIndex];
      document.getElementById('active-team-display').innerText = activeTeam.name;

      // Render Strikes
      const strikesContainer = document.getElementById('strikes-display');
      strikesContainer.innerHTML = '';
      for (let i = 0; i < gameState.strikes; i++) {{
        strikesContainer.innerHTML += `<span class="strike-x">❌</span>`;
      }}

      // Update Trump Card Eligibility Badge
      const badge = document.getElementById('trump-eligibility-badge');
      if (gameState.currentQGuesses < 2) {{
        badge.className = 'guess-tracker-badge eligible';
        badge.innerText = `⚡ TRUMP CARDS ALLOWED (${{gameState.currentQGuesses}}/2 Guesses Made)`;
      }} else {{
        badge.className = 'guess-tracker-badge locked';
        badge.innerText = `🔒 TRUMP LOCKED (${{gameState.currentQGuesses}} Guesses Made)`;
      }}
    }}

    function playTrumpCard(teamIdx) {{
      // Verification Rules:
      if (gameState.currentQGuesses >= 2) {{
        showModal("TRUMP CARD BLOCKED", `Cannot play Trump Card! The active team has already made ${{gameState.currentQGuesses}} guesses on this question (Limit is < 2).`);
        return;
      }}

      if (gameState.currentQTrumped) {{
        showModal("TRUMP CARD BLOCKED", "A Trump Card has already been played on this question! Counter-trumping is not permitted.");
        return;
      }}

      if (gameState.teams[teamIdx].trumpsRemaining <= 0) {{
        return;
      }}

      // Execute Trump Card!
      gameState.teams[teamIdx].trumpsRemaining--;
      gameState.currentQTrumped = true;
      gameState.activeTeamIndex = teamIdx;
      sound.playTrump();

      showModal("⚡ TRUMP CARD ACTIVATED!", `${{gameState.teams[teamIdx].name}} played a TRUMP CARD and hijacked the turn!`);
      
      updateTurnDisplay();
      renderScoreboard();
    }}

    function renderScoreboard() {{
      const container = document.getElementById('teams-scoreboard');
      container.innerHTML = '';

      const isEligible = (gameState.currentQGuesses < 2) && !gameState.currentQTrumped;

      gameState.teams.forEach((team, idx) => {{
        const isActive = (idx === gameState.activeTeamIndex);
        const card = document.createElement('div');
        card.className = `team-card ${{isActive ? 'active-turn' : ''}}`;

        const canTrump = !isActive && isEligible && (team.trumpsRemaining > 0);

        card.innerHTML = `
          <div class="team-header">
            <div class="team-name">${{team.name}} ${{isActive ? '👑' : ''}}</div>
            <div class="team-score">${{team.score}} PTS</div>
          </div>
          <div class="trump-section">
            <button class="btn-trump" ${{canTrump ? '' : 'disabled'}} onclick="playTrumpCard(${{idx}})">
              <span>⚡ PLAY TRUMP CARD</span>
              <span class="trump-count">${{team.trumpsRemaining}}/3 LEFT</span>
            </button>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    function revealAll() {{
      gameState.revealedAnswers = new Array(8).fill(true);
      sound.playCorrect();
      renderBoard();
    }}

    function nextQuestion() {{
      loadQuestion(gameState.currentQIndex + 1);
    }}

    function showVictory() {{
      document.getElementById('game-screen').style.display = 'none';
      document.getElementById('victory-screen').style.display = 'flex';

      // Sort teams by score
      const sorted = [...gameState.teams].sort((a, b) => b.score - a.score);
      const winner = sorted[0];

      document.getElementById('winner-team-name').innerText = winner.name;
      document.getElementById('winner-score-display').innerText = `CHAMPIONS • ${{winner.score}} TOTAL POINTS`;

      const standings = document.getElementById('final-standings-list');
      standings.innerHTML = '';
      sorted.forEach((team, rank) => {{
        const item = document.createElement('div');
        item.className = 'standing-item';
        item.innerHTML = `
          <span>#${{rank + 1}} ${{team.name}}</span>
          <span style="color: var(--accent-gold);">${{team.score}} PTS</span>
        `;
        standings.appendChild(item);
      }});
    }}

    function resetToSetup() {{
      document.getElementById('victory-screen').style.display = 'none';
      document.getElementById('setup-screen').style.display = 'flex';
    }}

    function showModal(title, msg) {{
      document.getElementById('modal-title').innerText = title;
      document.getElementById('modal-msg').innerText = msg;
      document.getElementById('modal-overlay').style.display = 'flex';
    }}

    function closeModal() {{
      document.getElementById('modal-overlay').style.display = 'none';
    }}
  </script>
</body>
</html>
"""
    with open("Cascade_Sports_Game.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Cascade_Sports_Game.html updated successfully!")

if __name__ == "__main__":
    generate_cascade_html()

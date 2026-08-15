import json

# Load 180 verified questions
with open(r'd:\Case\questions_180.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

json_str = json.dumps(questions, indent=2, ensure_ascii=False)

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sports Connection Quiz - Minimal PPT Slideshow</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <style>
    :root {{
      --bg-dark: #070a14;
      --slide-bg: #0d1322;
      --border-color: rgba(255, 255, 255, 0.08);
      
      --accent-easy: #00e676;
      --accent-medium: #ffb300;
      --accent-hard: #ff2d55;
      
      --sport-cricket: #ffc107;
      --sport-football: #00e5ff;
      --sport-tennis: #a6ff00;
      --sport-basketball: #ff6d00;
      --sport-f1: #ff3333;
      --sport-olympics: #ffd700;
      
      --text-main: #ffffff;
      --text-muted: #8e9baf;
      
      --font-heading: 'Outfit', sans-serif;
      --font-body: 'Inter', sans-serif;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }}

    html, body {{
      width: 100vw;
      height: 100vh;
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: var(--font-body);
      overflow: hidden;
    }}

    /* MAIN APP CONTAINER FOR FULLSCREEN SUPPORT */
    .app-container {{
      width: 100vw;
      height: 100vh;
      display: flex;
      flex-direction: column;
      background: radial-gradient(circle at 50% 30%, #111a30 0%, #070a14 100%);
      position: relative;
    }}

    .app-container.is-fullscreen {{
      position: fixed !important;
      inset: 0 !important;
      z-index: 99999 !important;
      width: 100vw !important;
      height: 100vh !important;
    }}

    /* MINIMAL PPT HEADER */
    .ppt-header {{
      height: 52px;
      padding: 0 1.8rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-color);
      background: rgba(7, 10, 20, 0.8);
      backdrop-filter: blur(10px);
      z-index: 10;
      flex-shrink: 0;
    }}

    .brand-group {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}

    .brand-logo {{
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      font-family: var(--font-heading);
      font-weight: 800;
      font-size: 0.85rem;
      letter-spacing: 1px;
      transition: color 0.3s ease;
    }}

    .brand-title {{
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 0.95rem;
      color: #cbd5e1;
    }}

    .header-center-info {{
      font-family: var(--font-heading);
      font-weight: 700;
      font-size: 0.9rem;
      color: var(--text-muted);
      letter-spacing: 0.5px;
    }}

    .header-right-tools {{
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }}

    .stat-badge {{
      font-size: 0.8rem;
      font-weight: 600;
      color: #94a3b8;
      background: rgba(255, 255, 255, 0.04);
      padding: 0.3rem 0.7rem;
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.06);
    }}

    .tool-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #cbd5e1;
      padding: 0.4rem 0.75rem;
      border-radius: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .tool-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
    }}

    /* SLIDE STAGE / CANVAS */
    .slide-stage {{
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 1.2rem;
      position: relative;
      overflow: hidden;
    }}

    .slide-card-deck {{
      width: 100%;
      max-width: 1000px;
      aspect-ratio: 16 / 9;
      max-height: calc(100vh - 130px);
      background: var(--slide-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: border-color 0.4s ease, box-shadow 0.4s ease;
    }}

    .app-container.is-fullscreen .slide-card-deck {{
      max-width: 1280px;
      max-height: calc(100vh - 120px);
    }}

    .slide-content-area {{
      width: 100%;
      height: 100%;
      padding: 2.2rem 3rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      transition: opacity 0.25s ease, transform 0.25s ease;
    }}

    /* INTRO SLIDE (SLIDE 1 OF PAIR) */
    .intro-slide {{
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      gap: 1.6rem;
    }}

    .slide-label-top {{
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--text-muted);
      transition: color 0.3s ease;
    }}

    .intro-sport-display {{
      font-family: var(--font-heading);
      font-size: 4rem;
      font-weight: 900;
      letter-spacing: 2px;
      display: flex;
      align-items: center;
      gap: 1.2rem;
      text-transform: uppercase;
      transition: color 0.3s ease, text-shadow 0.3s ease;
    }}

    .intro-diff-badge {{
      font-family: var(--font-heading);
      font-size: 1.8rem;
      font-weight: 800;
      padding: 0.5rem 2.5rem;
      border-radius: 40px;
      letter-spacing: 2px;
      text-transform: uppercase;
    }}

    .reveal-prompt-btn {{
      margin-top: 0.8rem;
      background: linear-gradient(135deg, #00b0ff, #0055ff);
      color: #fff;
      border: none;
      padding: 0.85rem 2.4rem;
      border-radius: 30px;
      font-family: var(--font-heading);
      font-size: 1.15rem;
      font-weight: 800;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(0, 176, 255, 0.35);
      transition: all 0.25s ease;
    }}

    .reveal-prompt-btn:hover {{
      transform: translateY(-2px) scale(1.03);
      box-shadow: 0 12px 30px rgba(0, 176, 255, 0.5);
    }}

    /* QUESTION SLIDE (SLIDE 2 OF PAIR) */
    .question-slide {{
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}

    .q-meta-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .q-badge-group {{
      display: flex;
      gap: 0.6rem;
    }}

    .q-pill {{
      padding: 0.3rem 0.8rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      transition: all 0.3s ease;
    }}

    /* CIRCULAR TIMER */
    .timer-widget {{
      position: relative;
      width: 48px;
      height: 48px;
      display: flex;
      justify-content: center;
      align-items: center;
    }}

    .timer-svg {{
      transform: rotate(-90deg);
      width: 48px;
      height: 48px;
    }}

    .timer-bg {{
      fill: none;
      stroke: rgba(255, 255, 255, 0.1);
      stroke-width: 4;
    }}

    .timer-progress {{
      fill: none;
      stroke: var(--accent-easy);
      stroke-width: 4;
      stroke-dasharray: 138;
      stroke-dashoffset: 0;
      stroke-linecap: round;
      transition: stroke-dashoffset 1s linear, stroke 0.3s ease;
    }}

    .timer-text {{
      position: absolute;
      font-family: var(--font-heading);
      font-weight: 800;
      font-size: 1.05rem;
      color: #fff;
    }}

    .timer-widget.alert .timer-progress {{
      stroke: var(--accent-hard) !important;
    }}

    .q-main-text {{
      font-family: var(--font-heading);
      font-size: 1.5rem;
      font-weight: 700;
      line-height: 1.35;
      color: #ffffff;
      margin: 0;
    }}

    .mcq-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.85rem;
    }}

    .mcq-card {{
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 10px;
      padding: 0.85rem 1.1rem;
      display: flex;
      align-items: center;
      gap: 0.8rem;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .mcq-card:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: var(--sport-accent, rgba(255, 255, 255, 0.3));
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3), 0 0 15px var(--sport-accent, transparent);
    }}

    .mcq-badge {{
      width: 32px;
      height: 32px;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.06);
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: var(--font-heading);
      font-weight: 800;
      font-size: 0.95rem;
      color: var(--text-muted);
      flex-shrink: 0;
      transition: all 0.3s ease;
    }}

    .mcq-label {{
      font-size: 0.98rem;
      font-weight: 500;
      color: #e2e8f0;
    }}

    .mcq-card.correct {{
      background: rgba(0, 230, 118, 0.15) !important;
      border-color: var(--accent-easy) !important;
    }}
    .mcq-card.correct .mcq-badge {{
      background: var(--accent-easy) !important;
      color: #000 !important;
    }}

    .mcq-card.incorrect {{
      background: rgba(255, 45, 85, 0.15) !important;
      border-color: var(--accent-hard) !important;
    }}
    .mcq-card.incorrect .mcq-badge {{
      background: var(--accent-hard) !important;
      color: #fff !important;
    }}

    .mcq-card.disabled {{
      pointer-events: none;
      opacity: 0.65;
    }}
    .mcq-card.correct.disabled, .mcq-card.incorrect.disabled {{
      opacity: 1;
    }}

    /* MINIMAL PPT FOOTER BAR */
    .ppt-footer {{
      height: 54px;
      padding: 0 1.8rem;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      border-top: 1px solid var(--border-color);
      background: rgba(7, 10, 20, 0.9);
      backdrop-filter: blur(10px);
      z-index: 10;
      flex-shrink: 0;
      position: relative;
    }}

    .progress-line {{
      position: absolute;
      top: 0;
      left: 0;
      height: 3px;
      background: #00b0ff;
      transition: width 0.3s ease, background 0.4s ease, box-shadow 0.4s ease;
    }}

    .footer-hints {{
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    .kbd-tag {{
      background: rgba(255, 255, 255, 0.08);
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      font-family: monospace;
      font-size: 0.75rem;
      color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}

    .footer-actions {{
      display: flex;
      gap: 0.6rem;
    }}

    /* GRID MODAL */
    .modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(4, 6, 12, 0.85);
      backdrop-filter: blur(8px);
      z-index: 1000;
      display: none;
      justify-content: center;
      align-items: center;
      padding: 2rem;
    }}

    .modal-card {{
      background: #0d1322;
      border: 1px solid var(--border-color);
      border-radius: 14px;
      width: 100%;
      max-width: 900px;
      max-height: 80vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}

    .modal-header {{
      padding: 1rem 1.5rem;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .modal-content {{
      padding: 1.2rem 1.5rem;
      overflow-y: auto;
      flex: 1;
    }}

    .filter-group {{
      display: flex;
      gap: 0.4rem;
      margin-bottom: 1rem;
      flex-wrap: wrap;
    }}

    .filter-btn {{
      padding: 0.35rem 0.9rem;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #94a3b8;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
    }}

    .filter-btn.active {{
      background: #00b0ff;
      color: #000;
      border-color: #00b0ff;
      font-weight: 700;
    }}

    .grid-layout {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(64px, 1fr));
      gap: 0.6rem;
    }}

    .grid-cell {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 0.4rem 0.2rem;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .grid-cell:hover {{
      background: rgba(255, 255, 255, 0.12);
    }}

    .grid-cell.active {{
      border-color: #00b0ff;
      background: rgba(0, 176, 255, 0.2);
    }}

    /* TOAST */
    .toast-box {{
      position: fixed;
      bottom: 70px;
      left: 50%;
      transform: translateX(-50%) translateY(15px);
      background: #1e293b;
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 0.6rem 1.4rem;
      border-radius: 20px;
      font-size: 0.85rem;
      font-weight: 600;
      z-index: 2000;
      opacity: 0;
      pointer-events: none;
      transition: all 0.25s ease;
    }}

    .toast-box.show {{
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }}
  </style>
</head>
<body>

  <div class="app-container" id="appContainer">
    <!-- PROGRESS BAR -->
    <div class="progress-line" id="progressLine" style="width: 0.27%;"></div>

    <!-- MINIMAL PPT HEADER -->
    <header class="ppt-header">
      <div class="brand-group">
        <a href="index.html" class="tool-btn" style="text-decoration:none; background:rgba(255,255,255,0.08); color:#cbd5e1;">
          <i class="fa-solid fa-house"></i> Hub
        </a>
        <div class="brand-logo" id="brandLogo">PPT DECK</div>
        <div class="brand-title">Sports Connection Quiz</div>
      </div>

      <div class="header-center-info" id="slideInfo">
        Slide 1 of 360 (Question 1 Intro)
      </div>

      <div class="header-right-tools">
        <div class="stat-badge">Score: <strong id="scoreVal">0</strong></div>
        <div class="stat-badge">Streak: <strong id="streakVal">0</strong></div>
        
        <button class="tool-btn" id="soundBtn" onclick="toggleSound()">
          <i class="fa-solid fa-volume-high" id="soundIcon"></i>
        </button>
        <button class="tool-btn" onclick="openGridModal()">
          <i class="fa-solid fa-grid-2"></i> Grid
        </button>
        <button class="tool-btn" onclick="toggleFullscreen()">
          <i class="fa-solid fa-expand" id="fsIcon"></i> Fullscreen
        </button>
        <button class="tool-btn" id="shuffleBtn" onclick="shuffleDeck()" style="background:rgba(0, 176, 255, 0.15); border-color:#00b0ff; color:#fff;">
          <i class="fa-solid fa-shuffle"></i> Shuffle
        </button>
      </div>
    </header>

    <!-- SLIDE CANVAS STAGE -->
    <main class="slide-stage">
      <div class="slide-card-deck" id="slideCardDeck">
        <div class="slide-content-area" id="slideContentArea">
          <!-- Slide rendered via JavaScript -->
        </div>
      </div>
    </main>

    <!-- MINIMAL FOOTER -->
    <footer class="ppt-footer">

      <div class="footer-actions">
        <button class="tool-btn" onclick="prevSlide()">
          <i class="fa-solid fa-chevron-left"></i> Previous
        </button>
        <button class="tool-btn" id="revealBtn" onclick="revealAnswerCurrent()" style="display:none; background:rgba(255,45,85,0.15); border-color:var(--accent-hard); color:#fff;">
          <i class="fa-solid fa-key"></i> Reveal Answer
        </button>
        <button class="tool-btn" id="nextBtn" onclick="nextSlide()" style="background:#00b0ff; color:#000; font-weight:700; border-color:#00b0ff; transition: all 0.3s ease;">
          Next Slide <i class="fa-solid fa-chevron-right"></i>
        </button>
      </div>
    </footer>
  </div>

  <!-- GRID MODAL -->
  <div class="modal-backdrop" id="gridModal">
    <div class="modal-card">
      <div class="modal-header">
        <div style="font-family:var(--font-heading); font-weight:700; font-size:1.1rem;">
          <i class="fa-solid fa-border-all"></i> Slide Deck Question Sorter
        </div>
        <button class="tool-btn" onclick="closeGridModal()"><i class="fa-solid fa-xmark"></i> Close</button>
      </div>
      <div class="modal-content">
        <div class="filter-group">
          <button class="filter-btn active" onclick="filterGrid('ALL', this)">All (180)</button>
          <button class="filter-btn" onclick="filterGrid('Easy', this)">Easy (60)</button>
          <button class="filter-btn" onclick="filterGrid('Medium', this)">Medium (60)</button>
          <button class="filter-btn" onclick="filterGrid('Hard', this)">Hard (60)</button>
          <button class="filter-btn" onclick="filterGrid('Cricket', this)">Cricket</button>
          <button class="filter-btn" onclick="filterGrid('Football', this)">Football</button>
          <button class="filter-btn" onclick="filterGrid('Tennis', this)">Tennis</button>
          <button class="filter-btn" onclick="filterGrid('Basketball', this)">Basketball</button>
        </div>
        <div class="grid-layout" id="gridContainer"></div>
      </div>
    </div>
  </div>

  <!-- TOAST -->
  <div class="toast-box" id="toast">Notification</div>

  <script>
    const RAW_QUESTIONS = {json_str};

    let deck = [...RAW_QUESTIONS];
    let questionIndex = 0;
    let isQuestionSlide = false; // false = Slide 1 (Intro), true = Slide 2 (Question)
    
    let timerSeconds = 30;
    let timerInterval = null;
    let isTimerRunning = false;
    
    let selectedOption = null;
    let answerRevealed = false;
    let score = 0;
    let streak = 0;
    let soundEnabled = true;
    let currentFilter = 'ALL';

    // Sound Synthesizer
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    let audioCtx = null;

    function playSound(type) {{
      if (!soundEnabled) return;
      try {{
        if (!audioCtx) audioCtx = new AudioCtx();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        const now = audioCtx.currentTime;
        if (type === 'tick') {{
          osc.type = 'sine';
          osc.frequency.setValueAtTime(600, now);
          gain.gain.setValueAtTime(0.03, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
          osc.start(now);
          osc.stop(now + 0.04);
        }} else if (type === 'warning') {{
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(800, now);
          gain.gain.setValueAtTime(0.06, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
          osc.start(now);
          osc.stop(now + 0.1);
        }} else if (type === 'correct') {{
          osc.type = 'sine';
          osc.frequency.setValueAtTime(523.25, now);
          osc.frequency.setValueAtTime(659.25, now + 0.08);
          gain.gain.setValueAtTime(0.1, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
          osc.start(now);
          osc.stop(now + 0.3);
        }} else if (type === 'wrong') {{
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(200, now);
          osc.frequency.setValueAtTime(140, now + 0.08);
          gain.gain.setValueAtTime(0.1, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
          osc.start(now);
          osc.stop(now + 0.25);
        }}
      }} catch (e) {{}}
    }}

    function toggleSound() {{
      soundEnabled = !soundEnabled;
      document.getElementById('soundIcon').className = soundEnabled ? 'fa-solid fa-volume-high' : 'fa-solid fa-volume-xmark';
      showToast(soundEnabled ? 'Sound Enabled' : 'Sound Muted');
    }}

    /* FULLSCREEN TOGGLE IMPLEMENTATION */
    function toggleFullscreen() {{
      const appContainer = document.getElementById('appContainer');
      const isFs = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement || appContainer.classList.contains('is-fullscreen');

      if (!isFs) {{
        appContainer.classList.add('is-fullscreen');
        const elem = document.documentElement;
        if (elem.requestFullscreen) {{
          elem.requestFullscreen().catch(() => {{}});
        }} else if (elem.webkitRequestFullscreen) {{
          elem.webkitRequestFullscreen();
        }} else if (elem.mozRequestFullScreen) {{
          elem.mozRequestFullScreen();
        }} else if (elem.msRequestFullscreen) {{
          elem.msRequestFullscreen();
        }}
        showToast('Entered Presentation Fullscreen Mode');
      }} else {{
        appContainer.classList.remove('is-fullscreen');
        if (document.exitFullscreen) {{
          document.exitFullscreen().catch(() => {{}});
        }} else if (document.webkitExitFullscreen) {{
          document.webkitExitFullscreen();
        }} else if (document.mozCancelFullScreen) {{
          document.mozCancelFullScreen();
        }} else if (document.msExitFullscreen) {{
          document.msExitFullscreen();
        }}
        showToast('Exited Fullscreen Mode');
      }}
    }}

    document.addEventListener('fullscreenchange', () => {{
      const appContainer = document.getElementById('appContainer');
      if (!document.fullscreenElement) {{
        appContainer.classList.remove('is-fullscreen');
      }}
    }});

    function getSportColor(sport) {{
      if (!sport) return '#00e5ff';
      const s = sport.toLowerCase();
      if (s.includes('tennis')) return 'var(--sport-tennis)';
      if (s.includes('football')) return 'var(--sport-football)';
      if (s.includes('cricket')) return 'var(--sport-cricket)';
      if (s.includes('basketball')) return 'var(--sport-basketball)';
      if (s.includes('f1') || s.includes('formula') || s.includes('motorsport')) return 'var(--sport-f1)';
      if (s.includes('olympic') || s.includes('athletics')) return 'var(--sport-olympics)';
      return '#00e5ff';
    }}

    function getSportHex(sport) {{
      if (!sport) return '#00e5ff';
      const s = sport.toLowerCase();
      if (s.includes('tennis')) return '#a6ff00';
      if (s.includes('football')) return '#00e5ff';
      if (s.includes('cricket')) return '#ffc107';
      if (s.includes('basketball')) return '#ff6d00';
      if (s.includes('f1') || s.includes('formula') || s.includes('motorsport')) return '#ff3333';
      if (s.includes('olympic') || s.includes('athletics')) return '#ffd700';
      return '#00e5ff';
    }}

    function getSportIcon(sport) {{
      const col = getSportColor(sport);
      switch(sport) {{
        case 'Cricket': return `<i class="fa-solid fa-baseball-bat-ball" style="color:${{col}}"></i>`;
        case 'Football': return `<i class="fa-solid fa-futbol" style="color:${{col}}"></i>`;
        case 'Tennis': return `<i class="fa-solid fa-table-tennis-paddle-ball" style="color:${{col}}"></i>`;
        case 'Basketball': return `<i class="fa-solid fa-basketball" style="color:${{col}}"></i>`;
        case 'Formula 1': return `<i class="fa-solid fa-flag-checkered" style="color:${{col}}"></i>`;
        case 'Olympics': return `<i class="fa-solid fa-award" style="color:${{col}}"></i>`;
        default: return `<i class="fa-solid fa-trophy" style="color:${{col}}"></i>`;
      }}
    }}

    function getSportBg(sport) {{
      if (!sport) return '';
      const s = sport.toLowerCase();
      if (s.includes('tennis')) return 'tennis_bg.jpg';
      if (s.includes('football')) return 'Football_bg.jpg';
      if (s.includes('cricket')) return 'Cricket_bg.jpg';
      if (s.includes('basketball')) return 'basketball_bg.jpg';
      if (s.includes('f1') || s.includes('formula') || s.includes('motorsport')) return 'f1_bg.jpg';
      if (s.includes('olympic') || s.includes('athletics')) return 'olympics_bg.jpg';
      return '';
    }}

    function getDiffColor(diff) {{
      switch(diff) {{
        case 'Easy': return 'var(--accent-easy)';
        case 'Medium': return 'var(--accent-medium)';
        case 'Hard': return 'var(--accent-hard)';
        default: return '#fff';
      }}
    }}

    function shuffleDeck() {{
      for (let i = deck.length - 1; i > 0; i--) {{
        const j = Math.floor(Math.random() * (i + 1));
        [deck[i], deck[j]] = [deck[j], deck[i]];
      }}
      questionIndex = 0;
      isQuestionSlide = false;
      showToast('Deck Shuffled!');
      renderSlide();
    }}

    function renderSlide() {{
      stopTimer();
      const area = document.getElementById('slideContentArea');
      const cardDeck = document.getElementById('slideCardDeck');
      const q = deck[questionIndex];

      const currentSlideNum = questionIndex * 2 + (isQuestionSlide ? 2 : 1);
      const totalSlides = deck.length * 2;
      
      const sportCol = getSportColor(q.sport);
      const sportHex = getSportHex(q.sport);
      const isDarkText = ['#a6ff00', '#00e5ff', '#ffc107', '#ffd700'].includes(sportHex);

      document.getElementById('slideInfo').innerText = `Slide ${{currentSlideNum}} of ${{totalSlides}} (${{isQuestionSlide ? 'Question' : 'Intro'}})`;
      
      const progressLine = document.getElementById('progressLine');
      if (progressLine) {{
        progressLine.style.width = `${{(currentSlideNum / totalSlides) * 100}}%`;
        progressLine.style.background = sportHex;
        progressLine.style.boxShadow = `0 0 12px ${{sportHex}}`;
      }}

      document.getElementById('scoreVal').innerText = score;
      document.getElementById('streakVal').innerText = streak;

      // Sync header elements to sport color
      const brandLogo = document.getElementById('brandLogo');
      if (brandLogo) {{
        brandLogo.style.color = sportHex;
        brandLogo.style.borderColor = sportHex + '40';
      }}

      // Sync Next button accent to sport color
      const nextBtn = document.getElementById('nextBtn');
      if (nextBtn) {{
        nextBtn.style.background = sportHex;
        nextBtn.style.borderColor = sportHex;
        nextBtn.style.color = isDarkText ? '#000' : '#fff';
        nextBtn.style.boxShadow = `0 4px 14px ${{sportHex}}40`;
      }}

      // Dynamic Sport Background with dynamic glow border matching sport color
      const bgImg = getSportBg(q.sport);
      cardDeck.style.borderColor = sportHex + '44';
      cardDeck.style.boxShadow = `0 20px 50px rgba(0, 0, 0, 0.5), 0 0 35px ${{sportHex}}20`;

      if (bgImg) {{
        cardDeck.style.backgroundImage = `linear-gradient(135deg, rgba(7, 10, 20, 0.85), rgba(13, 19, 34, 0.88)), url("${{bgImg}}")`;
        cardDeck.style.backgroundSize = 'cover';
        cardDeck.style.backgroundPosition = 'center';
      }} else {{
        cardDeck.style.backgroundImage = '';
      }}

      if (!isQuestionSlide) {{
        // SLIDE 1 OF PAIR: MINIMAL INTRO SLIDE (Text & Accents Synced to Sport Color)
        area.innerHTML = `
          <div class="intro-slide">
            <div class="slide-label-top" style="color: ${{sportHex}}; letter-spacing: 3px;">
              <i class="fa-solid fa-circle-dot" style="font-size: 0.7rem; margin-right: 0.4rem;"></i> QUESTION ${{questionIndex + 1}} OF ${{deck.length}} • INTRO
            </div>
            
            <div class="intro-sport-display" style="color: ${{sportCol}}; text-shadow: 0 0 30px ${{sportHex}}45;">
              ${{getSportIcon(q.sport)}} ${{q.sport}}
            </div>
            
            <div class="intro-diff-badge" style="background: ${{getDiffColor(q.difficulty)}}18; color: ${{getDiffColor(q.difficulty)}}; border: 1.5px solid ${{getDiffColor(q.difficulty)}};">
              ⚡ ${{q.difficulty}}
            </div>

            <button class="reveal-prompt-btn" onclick="nextSlide()" style="background: linear-gradient(135deg, ${{sportHex}}, ${{sportHex}}cc); color: ${{isDarkText ? '#000' : '#fff'}}; box-shadow: 0 8px 24px ${{sportHex}}40;">
              REVEAL QUESTION SLIDE <i class="fa-solid fa-play" style="font-size:0.9rem; margin-left:0.4rem;"></i>
            </button>
          </div>
        `;
        document.getElementById('revealBtn').style.display = 'none';
      }} else {{
        // SLIDE 2 OF PAIR: QUESTION SLIDE (MCQ + 30S TIMER - Synced Colors)
        selectedOption = null;
        answerRevealed = false;

        area.innerHTML = `
          <div class="question-slide">
            <div class="q-meta-header">
              <div class="q-badge-group">
                <span class="q-pill" style="background:${{getDiffColor(q.difficulty)}}18; color:${{getDiffColor(q.difficulty)}}; border:1px solid ${{getDiffColor(q.difficulty)}};">
                  ${{q.difficulty}}
                </span>
                <span class="q-pill" style="background:${{sportHex}}18; color:${{sportCol}}; border:1px solid ${{sportHex}}40; box-shadow: 0 0 12px ${{sportHex}}20;">
                  ${{getSportIcon(q.sport)}} ${{q.sport}}
                </span>
              </div>

              <div class="timer-widget" id="timerWidget">
                <svg class="timer-svg">
                  <circle class="timer-bg" cx="24" cy="24" r="22"></circle>
                  <circle class="timer-progress" id="timerProgress" cx="24" cy="24" r="22" style="stroke: ${{sportHex}};"></circle>
                </svg>
                <div class="timer-text" id="timerText">30</div>
              </div>
            </div>

            <div class="q-main-text">
              <span style="color: ${{sportCol}}; font-weight: 800; font-family: var(--font-heading); margin-right: 0.4rem;">Q${{questionIndex + 1}}.</span>
              ${{q.question}}
            </div>

            <div class="mcq-grid">
              ${{q.options.map((opt, idx) => `
                <div class="mcq-card" id="opt-${{idx}}" onclick="selectOption(${{idx}})" style="--sport-accent: ${{sportHex}};">
                  <div class="mcq-badge" style="color: ${{sportHex}}; border: 1px solid ${{sportHex}}35;">${{String.fromCharCode(65 + idx)}}</div>
                  <div class="mcq-label">${{opt}}</div>
                </div>
              `).join('')}}
            </div>
          </div>
        `;
        document.getElementById('revealBtn').style.display = 'inline-flex';
        startTimer();
      }}
    }}

    function nextSlide() {{
      if (!isQuestionSlide) {{
        isQuestionSlide = true;
        renderSlide();
      }} else {{
        if (questionIndex < deck.length - 1) {{
          questionIndex++;
          isQuestionSlide = false;
          renderSlide();
        }} else {{
          showToast('Deck Completed! Reshuffling...');
          shuffleDeck();
        }}
      }}
    }}

    function prevSlide() {{
      if (isQuestionSlide) {{
        isQuestionSlide = false;
        renderSlide();
      }} else {{
        if (questionIndex > 0) {{
          questionIndex--;
          isQuestionSlide = true;
          renderSlide();
        }}
      }}
    }}

    /* TIMER CONTROLS */
    function startTimer() {{
      stopTimer();
      timerSeconds = 30;
      isTimerRunning = true;
      updateTimerUI();

      timerInterval = setInterval(() => {{
        if (!isTimerRunning) return;
        timerSeconds--;
        updateTimerUI();

        if (timerSeconds <= 5 && timerSeconds > 0) {{
          playSound('warning');
        }} else {{
          playSound('tick');
        }}

        if (timerSeconds <= 0) {{
          stopTimer();
          playSound('wrong');
          revealAnswerCurrent();
          showToast('Time Up!');
          setTimeout(() => {{
            nextSlide();
          }}, 2000);
        }}
      }}, 1000);
    }}

    function stopTimer() {{
      if (timerInterval) clearInterval(timerInterval);
      isTimerRunning = false;
    }}

    function updateTimerUI() {{
      const text = document.getElementById('timerText');
      const progress = document.getElementById('timerProgress');
      const widget = document.getElementById('timerWidget');

      if (text) text.innerText = timerSeconds;
      if (progress) {{
        const offset = 138 - (138 * timerSeconds) / 30;
        progress.style.strokeDashoffset = offset;
      }}

      if (widget) {{
        if (timerSeconds <= 5) widget.classList.add('alert');
        else widget.classList.remove('alert');
      }}
    }}

    /* OPTION SELECTION */
    function selectOption(idx) {{
      if (answerRevealed || !isQuestionSlide) return;
      selectedOption = idx;
      revealAnswerCurrent();
    }}

    function revealAnswerCurrent() {{
      if (answerRevealed || !isQuestionSlide) return;
      answerRevealed = true;
      stopTimer();

      const q = deck[questionIndex];
      const correctIdx = q.correct;

      for (let i = 0; i < 4; i++) {{
        const optEl = document.getElementById(`opt-${{i}}`);
        if (!optEl) continue;
        optEl.classList.add('disabled');

        if (i === correctIdx) {{
          optEl.classList.add('correct');
        }} else if (i === selectedOption) {{
          optEl.classList.add('incorrect');
        }}
      }}

      if (selectedOption === correctIdx) {{
        score += 10;
        streak++;
        playSound('correct');
        showToast('Correct! +10 Points');
      }} else if (selectedOption !== null) {{
        streak = 0;
        playSound('wrong');
        showToast('Incorrect Answer!');
      }}

      document.getElementById('scoreVal').innerText = score;
      document.getElementById('streakVal').innerText = streak;
    }}

    /* GRID MODAL */
    function openGridModal() {{
      renderGridItems();
      document.getElementById('gridModal').style.display = 'flex';
    }}

    function closeGridModal() {{
      document.getElementById('gridModal').style.display = 'none';
    }}

    function filterGrid(filter, btn) {{
      currentFilter = filter;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      renderGridItems();
    }}

    function renderGridItems() {{
      const container = document.getElementById('gridContainer');
      container.innerHTML = '';

      deck.forEach((q, idx) => {{
        if (currentFilter !== 'ALL') {{
          if (currentFilter === 'Easy' || currentFilter === 'Medium' || currentFilter === 'Hard') {{
            if (q.difficulty !== currentFilter) return;
          }} else {{
            if (q.sport !== currentFilter) return;
          }}
        }}

        const cell = document.createElement('div');
        cell.className = `grid-cell ${{idx === questionIndex ? 'active' : ''}}`;
        cell.onclick = () => {{
          questionIndex = idx;
          isQuestionSlide = false;
          closeGridModal();
          renderSlide();
        }};

        cell.innerHTML = `
          <div style="font-family:var(--font-heading); font-weight:800; font-size:0.9rem;">Q${{idx + 1}}</div>
          <div style="font-size:0.6rem; font-weight:700; color:${{getDiffColor(q.difficulty)}};">
            ${{q.difficulty[0]}} • ${{q.sport.slice(0, 3)}}
          </div>
        `;
        container.appendChild(cell);
      }});
    }}

    function showToast(msg) {{
      const toast = document.getElementById('toast');
      toast.innerText = msg;
      toast.classList.add('show');
      setTimeout(() => {{
        toast.classList.remove('show');
      }}, 2500);
    }}

    /* KEYBOARD SHORTCUTS */
    document.addEventListener('keydown', (e) => {{
      if (document.getElementById('gridModal').style.display === 'flex') {{
        if (e.key === 'Escape') closeGridModal();
        return;
      }}

      if (e.code === 'Space' || e.key === 'ArrowRight') {{
        e.preventDefault();
        nextSlide();
      }} else if (e.key === 'ArrowLeft') {{
        e.preventDefault();
        prevSlide();
      }} else if (e.key === '1' || e.key === 'a' || e.key === 'A') {{
        selectOption(0);
      }} else if (e.key === '2' || e.key === 'b' || e.key === 'B') {{
        selectOption(1);
      }} else if (e.key === '3' || e.key === 'c' || e.key === 'C') {{
        selectOption(2);
      }} else if (e.key === '4' || e.key === 'd' || e.key === 'D') {{
        selectOption(3);
      }} else if (e.key === 'r' || e.key === 'R') {{
        revealAnswerCurrent();
      }} else if (e.key === 'f' || e.key === 'F') {{
        toggleFullscreen();
      }} else if (e.key === 'g' || e.key === 'G') {{
        openGridModal();
      }}
    }});

    // Initialize Deck on Load
    window.addEventListener('DOMContentLoaded', () => {{
      shuffleDeck();
    }});
  </script>
</body>
</html>
'''

# Write to Sports_Connection_Quiz.html
with open(r'd:\Case\Sports_Connection_Quiz.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Successfully regenerated clean PPT presentation slideshow for Sports_Connection_Quiz.html!")

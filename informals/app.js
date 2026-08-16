/**
 * EA SPORTS FC ULTIMATE WALKOUT & CARD REVEAL ENGINE
 * - Pure Vector SVG Flags (No CSS stripes or double flag stacking)
 * - Complete 99 Clean Player Database Integration
 * - Clean Node Hiding on Phase 4 Pedestal (No duplicate background logos)
 * - Image Error Fallbacks
 */

document.addEventListener('DOMContentLoaded', () => {

    /* ── DATABASE & STATE ──────────────────────────────────────────────── */
    const playersList = (typeof PLAYERS_DATABASE !== 'undefined' && PLAYERS_DATABASE.length > 0)
        ? PLAYERS_DATABASE
        : [
            {
                id: 'p_1',
                name: 'Thibaut Courtois',
                category: 'Goalkeepers (GK)',
                basePrice: '₹5M',
                nation: 'BELGIUM',
                flagImg: 'Flag_of_Belgium.svg',
                pos: 'GK', rating: 89,
                club: 'REAL MADRID', clubImg: 'assets/real_madrid.jpeg',
                league: 'LALIGA', leagueImg: 'LaLiga_EA_Sports_2023_Vertical_Logo.svg',
                cardImg: 'no_bg/Thibaut Courtois.png'
            }
        ];

    let activeFilteredPlayers = [...playersList];
    let currentIdx = 0;
    let activePlayer = activeFilteredPlayers[0];

    // Sequence & Step State
    let currentPhase = 0; // 0: reset, 1: flag, 2: stats/price, 3: badges, 4: card
    let sequenceRunning = false;
    let animationTimer = null;
    let counterInterval = null;
    let hasAnimatedRating = false;
    let soundEnabled = true;

    /* ── DOM ELEMENTS ──────────────────────────────────────────────────── */
    const stageViewport   = document.getElementById('stage-viewport');
    const stage3d         = document.getElementById('stage-3d');
    const screenFlash     = document.getElementById('screen-flash');
    const canvas          = document.getElementById('particle-canvas');
    const ctx             = canvas.getContext('2d');

    const nodeFlag        = document.getElementById('node-flag');
    const nodeStats       = document.getElementById('node-stats');
    const nodeBadges      = document.getElementById('node-badges');
    const nodeCard        = document.getElementById('node-card');

    const badgePosition   = document.getElementById('badge-position');
    const badgePrice      = document.getElementById('badge-price');
    const badgeRating     = document.getElementById('badge-rating');

    const textPos         = document.getElementById('text-pos');
    const textPrice       = document.getElementById('text-price');
    const textRating      = document.getElementById('text-rating');
    const textNation      = document.getElementById('text-nation');

    const flagImgElem     = document.getElementById('flag-img-element');

    const imgClub         = document.getElementById('img-club');
    const textClub        = document.getElementById('text-club');
    const imgLeague       = document.getElementById('img-league');
    const textLeague      = document.getElementById('text-league');

    const imgCard         = document.getElementById('img-card');
    const card3dWrapper   = document.getElementById('card-3d-wrapper');
    const cardPlayerName  = document.getElementById('card-player-name');
    const cardPlayerCat   = document.getElementById('card-player-category');

    const pedestalFlagImg = document.getElementById('pedestal-flag-img');
    const pedestalNation  = document.getElementById('pedestal-nation-text');
    const pedestalPriceTx = document.getElementById('pedestal-price-text');
    const pedestalClub    = document.getElementById('pedestal-club');
    const pedestalClubTx  = document.getElementById('pedestal-club-text');
    const pedestalLeague  = document.getElementById('pedestal-league');
    const pedestalLeagueTx= document.getElementById('pedestal-league-text');

    const btnPlay         = document.getElementById('btn-play');
    const btnPrev         = document.getElementById('btn-prev');
    const btnNext         = document.getElementById('btn-next');
    const btnStageNext    = document.getElementById('btn-stage-next');
    const stageBtnText    = document.getElementById('stage-btn-text');
    const playBtnText     = document.getElementById('play-btn-text');

    const inputSearch     = document.getElementById('input-search');
    const selectCategory  = document.getElementById('select-category');
    const selectPlayer    = document.getElementById('select-player');
    const playerCounter   = document.getElementById('player-counter');
    const btnSound        = document.getElementById('btn-sound');
    const btnFullscreen   = document.getElementById('btn-fullscreen');

    /* ── AUDIO SYNTHESIS ───────────────────────────────────────────────── */
    let audioCtx = null;

    function ensureAudio() {
        if (!soundEnabled) return;
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
    }

    function tone(freq, type = 'sine', vol = 0.1, dur = 0.12, delay = 0) {
        if (!soundEnabled || !audioCtx || audioCtx.state !== 'running') return;
        try {
            const osc  = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            const t    = audioCtx.currentTime + delay;
            osc.type = type;
            osc.frequency.setValueAtTime(freq, t);
            gain.gain.setValueAtTime(0.001, t);
            gain.gain.linearRampToValueAtTime(vol, t + 0.015);
            gain.gain.exponentialRampToValueAtTime(0.001, t + dur);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(t);
            osc.stop(t + dur);
        } catch(e) {}
    }

    function playSwell() {
        tone(60, 'sine', 0.18, 1.6);
        tone(110, 'triangle', 0.08, 1.6, 0.1);
    }

    function playTick(n) {
        tone(300 + n * 38, 'sine', 0.07, 0.07);
    }

    function playBlast() {
        [523.25, 659.25, 783.99, 1046.50].forEach((f, i) => {
            tone(f, 'triangle', 0.18, 1.2, i * 0.06);
        });
        tone(130, 'sine', 0.28, 0.55, 0.0);
        tone(65, 'sine', 0.22, 0.8, 0.05);
    }

    function playChord() {
        [220, 277.18, 329.63, 440].forEach((f, i) => {
            tone(f, 'triangle', 0.07, 2.2, i * 0.04);
        });
    }

    /* ── PARTICLES SYSTEM ──────────────────────────────────────────────── */
    let particles = [];
    let cw = 0, ch = 0;

    function resizeCanvas() {
        cw = stageViewport.clientWidth;
        ch = stageViewport.clientHeight;
        canvas.width  = cw;
        canvas.height = ch;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    class Particle {
        constructor(burst) { this.reset(burst); }
        reset(burst) {
            this.x = burst ? cw / 2 : Math.random() * cw;
            this.y = burst ? ch / 2 : Math.random() * ch;
            const angle = Math.random() * Math.PI * 2;
            const speed = burst ? Math.random() * 6 + 2 : Math.random() * 0.9 + 0.15;
            this.vx    = burst ? Math.cos(angle) * speed : (Math.random() - 0.5) * 0.35;
            this.vy    = burst ? Math.sin(angle) * speed : -Math.random() * 1.0 - 0.2;
            this.size  = Math.random() * (burst ? 3.5 : 2) + 0.8;
            this.life  = burst ? 1 : Math.random();
            this.decay = Math.random() * 0.013 + (burst ? 0.012 : 0.003);
            this.color = Math.random() > 0.3 ? '#F5C642' : '#FFF5B8';
        }
        update() {
            this.x += this.vx; this.y += this.vy;
            this.life -= this.decay;
            if (this.life <= 0) this.reset(false);
        }
        draw() {
            ctx.save();
            ctx.globalAlpha = Math.max(0, this.life) * 0.8;
            ctx.fillStyle   = this.color;
            ctx.shadowBlur  = 6; ctx.shadowColor = this.color;
            ctx.beginPath(); ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2); ctx.fill();
            ctx.restore();
        }
    }

    for (let i = 0; i < 60; i++) particles.push(new Particle(false));

    function burst() {
        for (let i = 0; i < 55; i++) particles.push(new Particle(true));
    }

    (function animLoop() {
        ctx.clearRect(0, 0, cw, ch);
        for (let i = particles.length - 1; i >= 0; i--) {
            particles[i].update();
            particles[i].draw();
            if (particles.length > 60 && particles[i].life <= 0) {
                particles.splice(i, 1);
            }
        }
        requestAnimationFrame(animLoop);
    })();

    /* ── DROPDOWNS & FILTERING ─────────────────────────────────────────── */
    function populatePlayerDropdown() {
        selectPlayer.innerHTML = '';
        activeFilteredPlayers.forEach((p, idx) => {
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = `${idx + 1}. ${p.name} (${p.pos} - ${p.basePrice})`;
            if (idx === currentIdx) opt.selected = true;
            selectPlayer.appendChild(opt);
        });
        playerCounter.textContent = `${currentIdx + 1} / ${activeFilteredPlayers.length}`;
    }

    function applyFilters() {
        const cat = selectCategory.value;
        const query = inputSearch.value.toLowerCase().trim();

        activeFilteredPlayers = playersList.filter(p => {
            let matchCat = true;
            if (cat !== 'ALL') {
                if (cat === 'LW') matchCat = (p.pos === 'LW' || p.pos === 'LM');
                else if (cat === 'RW') matchCat = (p.pos === 'RW' || p.pos === 'RM');
                else matchCat = (p.pos === cat);
            }
            let matchQuery = true;
            if (query) {
                matchQuery = p.name.toLowerCase().includes(query) ||
                             p.nation.toLowerCase().includes(query) ||
                             p.club.toLowerCase().includes(query) ||
                             p.league.toLowerCase().includes(query);
            }
            return matchCat && matchQuery;
        });

        if (activeFilteredPlayers.length === 0) {
            activeFilteredPlayers = [...playersList];
        }
        currentIdx = 0;
        applyPlayer(activeFilteredPlayers[0]);
        populatePlayerDropdown();
    }

    selectCategory.addEventListener('change', applyFilters);
    inputSearch.addEventListener('input', applyFilters);

    selectPlayer.addEventListener('change', (e) => {
        currentIdx = parseInt(e.target.value, 10);
        applyPlayer(activeFilteredPlayers[currentIdx]);
        startSequence();
    });

    /* ── APPLY PLAYER DATA ─────────────────────────────────────────────── */
    function applyPlayer(p) {
        activePlayer = p;

        // Flag: Vector SVG ONLY
        flagImgElem.src = p.flagImg;
        pedestalFlagImg.src = p.flagImg;
        textNation.innerText     = p.nation;
        pedestalNation.innerText = p.nation;

        // Position & Base Price
        textPos.innerText        = p.pos;
        textPrice.innerText      = p.basePrice;
        pedestalPriceTx.innerText= p.basePrice;

        // Badges
        imgClub.src   = p.clubImg;    textClub.innerText     = p.club;
        imgLeague.src = p.leagueImg;  textLeague.innerText   = p.league;

        // Card Image + fallback
        imgCard.onerror = () => {
            imgCard.onerror = null;
            imgCard.src = 'assets/courtois_card.jpeg';
        };
        imgCard.src = p.cardImg;

        cardPlayerName.innerText = p.name;
        cardPlayerCat.innerText  = p.category || `${p.pos} • ${p.basePrice}`;

        pedestalClub.src      = p.clubImg;   pedestalClubTx.innerText   = p.club;
        pedestalLeague.src    = p.leagueImg; pedestalLeagueTx.innerText  = p.league;

        playerCounter.textContent = `${currentIdx + 1} / ${activeFilteredPlayers.length}`;
        if (selectPlayer.options.length > currentIdx) {
            selectPlayer.selectedIndex = currentIdx;
        }
    }

    /* ── RATING COUNTER ANIMATION ──────────────────────────────────────── */
    function animateRating(target) {
        if (hasAnimatedRating) {
            textRating.innerText = target;
            badgeRating.classList.add('blast');
            return;
        }
        hasAnimatedRating = true;

        const START = 80;
        let cur = START;
        textRating.innerText = cur;
        badgeRating.classList.remove('blast', 'counting');
        badgeRating.classList.add('counting');

        counterInterval = setInterval(() => {
            cur++;
            textRating.innerText = cur;
            playTick(cur - START);

            if (cur >= target - 1) {
                clearInterval(counterInterval);
                counterInterval = null;

                setTimeout(() => {
                    badgeRating.classList.remove('counting');
                    badgeRating.classList.add('blast');
                    textRating.innerText = target;
                    flashScreen();
                    playBlast();
                    burst();
                }, 800);
            }
        }, 110);
    }

    function flashScreen() {
        screenFlash.classList.add('active');
        setTimeout(() => screenFlash.classList.remove('active'), 220);
    }

    function clearAllTimers() {
        if (animationTimer)  { clearTimeout(animationTimer);   animationTimer  = null; }
        if (counterInterval) { clearInterval(counterInterval); counterInterval = null; }
    }

    function resetStage() {
        clearAllTimers();
        hasAnimatedRating = false;
        sequenceRunning   = false;
        currentPhase      = 0;
        stage3d.classList.remove('animating');

        [nodeFlag, nodeStats, nodeBadges, nodeCard].forEach(n => n.classList.remove('visible'));
        badgePosition.classList.remove('visible');
        badgeRating.classList.remove('blast', 'counting');
        textRating.innerText = '—';

        playBtnText.innerText = 'START WALKOUT';
        stageBtnText.innerText = 'START WALKOUT';
    }

    /* ── PHASE REVEAL ENGINE ──────────────────────────────────────────── */
    function advancePhase() {
        ensureAudio();
        currentPhase++;

        if (currentPhase === 1) { // Phase 1: Flag ONLY
            sequenceRunning = true;
            stage3d.classList.add('animating');
            nodeFlag.classList.add('visible');
            nodeStats.classList.remove('visible');
            nodeBadges.classList.remove('visible');
            nodeCard.classList.remove('visible');
            playSwell();
            playBtnText.innerText = 'REPLAY WALKOUT';
            stageBtnText.innerText = 'NEXT: STATS ➔';
        }
        else if (currentPhase === 2) { // Phase 2: Stats & Rating
            nodeFlag.classList.add('visible');
            nodeStats.classList.add('visible');
            nodeBadges.classList.remove('visible');
            nodeCard.classList.remove('visible');
            setTimeout(() => badgePosition.classList.add('visible'), 120);
            animateRating(activePlayer.rating);
            stageBtnText.innerText = 'NEXT: CLUB ➔';
        }
        else if (currentPhase === 3) { // Phase 3: Club / League
            nodeFlag.classList.add('visible');
            nodeStats.classList.add('visible');
            nodeBadges.classList.add('visible');
            nodeCard.classList.remove('visible');
            playChord();
            stageBtnText.innerText = 'SHOW CARD ➔';
        }
        else if (currentPhase === 4) { // Phase 4: Card & Pedestal ONLY (hides nodeBadges, nodeFlag, nodeStats!)
            nodeFlag.classList.remove('visible');
            nodeStats.classList.remove('visible');
            nodeBadges.classList.remove('visible');
            nodeCard.classList.add('visible');

            flashScreen();
            burst();
            sequenceRunning = false;
            stageBtnText.innerText = 'NEXT PLAYER ➔';
        }
        else if (currentPhase > 4) { // Next Player
            nextPlayer();
        }
    }

    async function startSequence() {
        ensureAudio();
        resetStage();
        currentPhase = 0;
        advancePhase();

        // Auto-timer for seamless full walkout
        animationTimer = setTimeout(() => {
            if (currentPhase === 1) advancePhase(); // Go to 2
            animationTimer = setTimeout(() => {
                if (currentPhase === 2) advancePhase(); // Go to 3
                animationTimer = setTimeout(() => {
                    if (currentPhase === 3) advancePhase(); // Go to 4
                }, 2200);
            }, 2400);
        }, 1600);
    }

    function nextPlayer() {
        currentIdx = (currentIdx + 1) % activeFilteredPlayers.length;
        applyPlayer(activeFilteredPlayers[currentIdx]);
        startSequence();
    }

    function prevPlayer() {
        currentIdx = (currentIdx - 1 + activeFilteredPlayers.length) % activeFilteredPlayers.length;
        applyPlayer(activeFilteredPlayers[currentIdx]);
        startSequence();
    }

    /* ── CARD 3D TILT ─────────────────────────────────────────────────── */
    card3dWrapper.addEventListener('mousemove', e => {
        const r = card3dWrapper.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width  / 2) / r.width;
        const y = (e.clientY - r.top  - r.height / 2) / r.height;
        card3dWrapper.style.transform =
            `perspective(900px) rotateX(${-y * 18}deg) rotateY(${x * 18}deg) scale(1.04)`;
    });
    card3dWrapper.addEventListener('mouseleave', () => {
        card3dWrapper.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) scale(1)';
    });

    /* ── BUTTON & KEYBOARD LISTENERS ──────────────────────────────────── */
    btnPlay.addEventListener('click', startSequence);
    btnPrev.addEventListener('click', prevPlayer);
    btnNext.addEventListener('click', nextPlayer);

    // On-stage floating next button
    btnStageNext.addEventListener('click', () => {
        clearAllTimers();
        advancePhase();
    });

    // Sound toggle button
    btnSound.addEventListener('click', () => {
        soundEnabled = !soundEnabled;
        if (soundEnabled) {
            btnSound.style.color = 'var(--gold-primary)';
            ensureAudio();
        } else {
            btnSound.style.color = '#777';
        }
    });

    // Fullscreen toggle button
    btnFullscreen.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(() => {});
        } else {
            document.exitFullscreen().catch(() => {});
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', e => {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
        if (e.key === 'ArrowRight' || e.key === 'Space') {
            e.preventDefault();
            clearAllTimers();
            advancePhase();
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            prevPlayer();
        } else if (e.key === 'f' || e.key === 'F') {
            btnFullscreen.click();
        } else if (e.key === 'm' || e.key === 'M') {
            btnSound.click();
        }
    });

    // Initialize first player
    applyFilters();
    applyPlayer(activeFilteredPlayers[0]);
});

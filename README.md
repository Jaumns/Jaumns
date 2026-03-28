<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>João Bohn Costa – Software Engineer</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #0a0a0c;
    --surface: #111116;
    --border: #1e1e28;
    --accent: #00e5a0;
    --accent2: #7c6dfa;
    --text: #e8e8f0;
    --muted: #6b6b82;
    --card: #13131a;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* NOISE OVERLAY */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.6;
  }

  /* AMBIENT GLOW */
  .glow-top {
    position: fixed;
    top: -200px; left: 50%;
    transform: translateX(-50%);
    width: 700px; height: 400px;
    background: radial-gradient(ellipse, rgba(0,229,160,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }
  .glow-bottom {
    position: fixed;
    bottom: -200px; right: -100px;
    width: 500px; height: 400px;
    background: radial-gradient(ellipse, rgba(124,109,250,0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .wrapper {
    position: relative;
    z-index: 1;
    max-width: 760px;
    margin: 0 auto;
    padding: 60px 24px 80px;
  }

  /* HEADER */
  .header {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: start;
    gap: 24px;
    margin-bottom: 56px;
    animation: fadeUp 0.7s ease both;
  }

  .header-left { display: flex; flex-direction: column; gap: 10px; }

  .tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid rgba(0,229,160,0.2);
    padding: 4px 12px;
    border-radius: 2px;
    width: fit-content;
  }
  .tag::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: pulse 2s ease-in-out infinite;
  }

  h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 6vw, 3.4rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--text);
  }
  h1 span {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .subtitle {
    font-size: 13px;
    color: var(--muted);
    line-height: 1.6;
    max-width: 360px;
  }

  /* SOCIAL ICONS */
  .socials {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: flex-end;
  }

  .social-link {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px; height: 44px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--card);
    text-decoration: none;
    color: var(--muted);
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
  }
  .social-link::before {
    content: '';
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 0.25s ease;
    border-radius: 10px;
  }
  .social-link:hover { color: #fff; transform: translateY(-2px); border-color: transparent; }
  .social-link:hover::before { opacity: 1; }

  .social-link.email::before   { background: linear-gradient(135deg, #ea4335, #fbbc05); }
  .social-link.linkedin::before { background: linear-gradient(135deg, #0077b5, #00a0dc); }
  .social-link.instagram::before { background: linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888); }
  .social-link.spotify::before  { background: linear-gradient(135deg, #1DB954, #157f3b); }

  .social-link svg { width: 20px; height: 20px; position: relative; z-index: 1; fill: currentColor; }

  /* TOOLTIP */
  .social-link .tip {
    position: absolute;
    right: 54px;
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 4px 10px;
    font-size: 11px;
    border-radius: 4px;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    color: var(--text);
  }
  .social-link:hover .tip { opacity: 1; }

  /* DIVIDER */
  .divider {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 40px 0;
  }

  /* SECTION */
  section {
    margin-bottom: 40px;
    animation: fadeUp 0.7s ease both;
  }
  section:nth-child(2) { animation-delay: 0.1s; }
  section:nth-child(3) { animation-delay: 0.2s; }
  section:nth-child(4) { animation-delay: 0.3s; }
  section:nth-child(5) { animation-delay: 0.4s; }

  .section-label {
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  .section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 10px;
  }

  p {
    font-size: 13.5px;
    line-height: 1.8;
    color: #9999b5;
  }
  p strong { color: var(--text); font-weight: 400; }

  /* SKILLS */
  .skills-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 4px;
  }
  .skill-pill {
    font-size: 12px;
    padding: 6px 16px;
    border-radius: 3px;
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--muted);
    letter-spacing: 0.05em;
    transition: all 0.2s ease;
    cursor: default;
  }
  .skill-pill:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(0,229,160,0.05);
  }

  /* GOALS */
  .goals-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 4px;
  }
  .goal-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 13.5px;
    color: #9999b5;
    line-height: 1.6;
  }
  .goal-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent2);
    margin-top: 7px;
    flex-shrink: 0;
  }

  /* CONTACT CARD */
  .contact-card {
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    background: var(--card);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
  }
  .contact-info { font-size: 13px; color: var(--muted); }
  .contact-email {
    color: var(--text);
    font-size: 14px;
    margin-top: 2px;
    letter-spacing: 0.02em;
  }
  .contact-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 10px 20px;
    border-radius: 6px;
    background: var(--accent);
    color: #0a0a0c;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease;
  }
  .contact-btn:hover { background: #00ffc0; transform: translateY(-1px); }

  /* FOOTER */
  .footer {
    margin-top: 60px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.05em;
    flex-wrap: wrap;
    gap: 8px;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.8); }
  }

  @media (max-width: 520px) {
    .header { grid-template-columns: 1fr; }
    .socials { flex-direction: row; justify-content: flex-start; }
    .social-link .tip { display: none; }
  }
</style>
</head>
<body>
<div class="glow-top"></div>
<div class="glow-bottom"></div>

<div class="wrapper">

  <!-- HEADER -->
  <div class="header">
    <div class="header-left">
      <span class="tag">Software Engineering · UNIJUÍ</span>
      <h1>Hi, I'm <span>João</span> 👋</h1>
      <p class="subtitle">Building technology with a human‑centered approach — focused on integration, accessibility &amp; community impact.</p>
    </div>
    <div class="socials">
      <!-- Email -->
      <a class="social-link email" href="mailto:joaobohncostawork@email.com" title="Email" aria-label="Email">
        <span class="tip">Email</span>
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20 4H4C2.9 4 2 4.9 2 6v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
      </a>
      <!-- LinkedIn -->
      <a class="social-link linkedin" href="https://www.linkedin.com/in/jaumns" target="_blank" rel="noopener" title="LinkedIn" aria-label="LinkedIn">
        <span class="tip">LinkedIn</span>
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
      </a>
      <!-- Instagram -->
      <a class="social-link instagram" href="https://www.instagram.com/jaumnss/" target="_blank" rel="noopener" title="Instagram" aria-label="Instagram">
        <span class="tip">Instagram</span>
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
      </a>
      <!-- Spotify -->
      <a class="social-link spotify" href="https://open.spotify.com/user/wlgoih8yr7pimasv1bkz58gha?si=1bec960a3d534302" target="_blank" rel="noopener" title="Spotify" aria-label="Spotify">
        <span class="tip">Spotify</span>
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>
      </a>
    </div>
  </div>

  <div class="divider"></div>

  <!-- ABOUT -->
  <section>
    <div class="section-label">⚙ About</div>
    <p>
      I am a <strong>Software Engineering student at UNIJUÍ</strong>, currently focused on building a strong foundation in software development. My studies emphasize core programming concepts, with attention to clarity, consistency, and good development practices.
      <br/><br/>
      I have practical experience with <strong>JavaScript</strong> and <strong>HTML</strong>, along with version control using <strong>Git &amp; GitHub</strong>. I continuously develop my skills through academic activities and personal projects.
      <br/><br/>
      I am particularly interested in <strong>technology as a tool for social impact</strong>, aiming to design and contribute to projects with a human-centered approach — focused on integration, accessibility, and strengthening the Brazilian community.
    </p>
  </section>

  <!-- SKILLS -->
  <section>
    <div class="section-label">⚙ Skills</div>
    <div class="skills-grid">
      <span class="skill-pill">JavaScript</span>
      <span class="skill-pill">HTML</span>
      <span class="skill-pill">Git</span>
      <span class="skill-pill">GitHub</span>
      <span class="skill-pill">Problem Solving</span>
      <span class="skill-pill">Code Organization</span>
    </div>
  </section>

  <!-- FOCUS -->
  <section>
    <div class="section-label">📚 Current Focus</div>
    <p>
      At this stage, my priority is to <strong>consolidate fundamental knowledge</strong> in programming and software development — including problem-solving, code organization, and project structuring. Every line of code is a step toward building something that matters.
    </p>
  </section>

  <!-- GOALS -->
  <section>
    <div class="section-label">🎯 Goals</div>
    <div class="goals-list">
      <div class="goal-item"><div class="goal-dot"></div><span>Develop consistent and well-structured projects</span></div>
      <div class="goal-item"><div class="goal-dot"></div><span>Expand my knowledge in backend development</span></div>
      <div class="goal-item"><div class="goal-dot"></div><span>Contribute to initiatives with social and community impact</span></div>
    </div>
  </section>

  <!-- CONTACT -->
  <section>
    <div class="section-label">📫 Contact</div>
    <div class="contact-card">
      <div>
        <div class="contact-info">Feel free to reach out</div>
        <div class="contact-email">joaobohncostawork@email.com</div>
      </div>
      <a class="contact-btn" href="mailto:joaobohncostawork@email.com">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4C2.9 4 2 4.9 2 6v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        Send Email
      </a>
    </div>
  </section>

  <!-- FOOTER -->
  <div class="footer">
    <span>João Bohn Costa · Software Engineering · UNIJUÍ</span>
    <span>🇧🇷 Rio Grande do Sul, BR</span>
  </div>

</div>
</body>
</html>

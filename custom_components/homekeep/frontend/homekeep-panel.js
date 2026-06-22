const CHIPS = {
  time: {
    label: "Time",
    icon: "mdi:clock-outline",
    options: ["5 min", "10 min", "15 min", "20 min"],
  },
  energy: {
    label: "Energy",
    icon: "mdi:flash-outline",
    options: ["low", "quiet", "normal", "high"],
  },
  mood: {
    label: "Mood",
    icon: "mdi:weather-partly-cloudy",
    options: ["auto", "calm", "focused", "tired", "energized"],
  },
  goal: {
    label: "Goal",
    icon: "mdi:target",
    options: ["quick wins", "visible lift", "fresh start", "overdue care"],
  },
  area: {
    label: "Area",
    icon: "mdi:floor-plan",
    options: ["Any area", "Kitchen", "Entryway", "Bathroom", "Laundry", "Living room"],
  },
};

const BUNDLES = [
  {
    id: "kitchen-reset",
    title: "Kitchen Reset",
    duration: 15,
    context: { time: "15 min", energy: "normal", mood: "calm", goal: "visible lift", area: "Kitchen" },
    reason: "The kitchen has the clearest lift for a short reset.",
    greeting: "Good evening. I found a small kitchen reset that can make the room feel lighter.",
    impact: { label: "Big kitchen boost", home: 7, areaName: "Kitchen", areaBefore: 48, areaAfter: 72 },
    bonusKeeps: 4,
    chores: [
      { id: "clear-dishes", name: "Clear dishes", area: "Kitchen", minutes: 6, keeps: 8, keepLine: "clears the surfaces people notice first" },
      { id: "wipe-counters", name: "Wipe counters", area: "Kitchen", minutes: 5, keeps: 7, keepLine: "helps the kitchen feel ready again" },
      { id: "take-out-compost", name: "Take out compost", area: "Kitchen", minutes: 4, keeps: 5, keepLine: "keeps tomorrow from starting stale" },
    ],
  },
  {
    id: "entryway-fresh-start",
    title: "Entryway Fresh Start",
    duration: 10,
    context: { time: "10 min", energy: "low", mood: "tired", goal: "quick wins", area: "Entryway" },
    reason: "A light entryway pass gives the home a visible welcome point.",
    greeting: "Let's keep this light. The entryway has a small reset ready.",
    impact: { label: "Visible lift", home: 4, areaName: "Entryway", areaBefore: 52, areaAfter: 68 },
    bonusKeeps: 3,
    chores: [
      { id: "shake-entry-rug", name: "Shake entry rug", area: "Entryway", minutes: 4, keeps: 5, keepLine: "freshens the first step inside" },
      { id: "clear-entry-shelf", name: "Clear entry shelf", area: "Entryway", minutes: 6, keeps: 6, keepLine: "makes keys and mail easier to land" },
    ],
  },
  {
    id: "quiet-bathroom-refresh",
    title: "Quiet Bathroom Refresh",
    duration: 10,
    context: { time: "10 min", energy: "quiet", mood: "calm", goal: "fresh start", area: "Bathroom" },
    reason: "This stays contained and gives the bathroom a steady refresh.",
    greeting: "A calm little refresh is available when you want it.",
    impact: { label: "Steady bathroom lift", home: 5, areaName: "Bathroom", areaBefore: 57, areaAfter: 74 },
    bonusKeeps: 3,
    chores: [
      { id: "reset-bathroom-sink", name: "Reset bathroom sink", area: "Bathroom", minutes: 6, keeps: 7, keepLine: "brings the sink back to easy use" },
      { id: "replace-hand-towel", name: "Replace hand towel", area: "Bathroom", minutes: 4, keeps: 4, keepLine: "adds a clean finish" },
    ],
  },
  {
    id: "laundry-launch",
    title: "Laundry Launch",
    duration: 20,
    context: { time: "20 min", energy: "high", mood: "focused", goal: "overdue care", area: "Laundry" },
    reason: "Laundry is stale enough to be worth a fuller pass.",
    greeting: "There is enough room for a focused reset. Laundry is the best fit.",
    impact: { label: "Useful catch-up", home: 8, areaName: "Laundry", areaBefore: 43, areaAfter: 69 },
    bonusKeeps: 5,
    chores: [
      { id: "start-small-laundry-load", name: "Start a small laundry load", area: "Laundry", minutes: 8, keeps: 9, keepLine: "gets the cycle moving" },
      { id: "fold-dry-towels", name: "Fold dry towels", area: "Laundry", minutes: 8, keeps: 8, keepLine: "returns a useful stack to the home" },
      { id: "wipe-laundry-surface", name: "Wipe laundry surface", area: "Laundry", minutes: 4, keeps: 4, keepLine: "keeps the room ready for the next load" },
    ],
  },
  {
    id: "evening-reset",
    title: "Evening Reset",
    duration: 5,
    context: { time: "5 min", energy: "low", mood: "auto", goal: "quick wins", area: "Any area" },
    reason: "A tiny mixed-area reset keeps the evening gentle.",
    greeting: "A five-minute reset can still help the home feel cared for.",
    impact: { label: "Small home lift", home: 3, areaName: "Home", areaBefore: 74, areaAfter: 77 },
    bonusKeeps: 2,
    chores: [
      { id: "clear-coffee-table", name: "Clear coffee table", area: "Living room", minutes: 3, keeps: 4, keepLine: "opens the room back up" },
      { id: "gather-stray-cups", name: "Gather stray cups", area: "Kitchen", minutes: 2, keeps: 3, keepLine: "prevents a small morning pileup" },
    ],
  },
];

const NO_SUGGESTION = {
  greeting: "Nothing fits this moment yet.",
  message: "Try changing the time, energy, or area.",
};

const BONUS_CHORE = {
  id: "water-kitchen-herbs",
  name: "Water kitchen herbs",
  area: "Kitchen",
  minutes: 3,
  keeps: 4,
  keepLine: "keeps a tiny bit of green cared for",
};

class HomekeepPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.state = {
      view: "ready",
      selected: 0,
      expanded: false,
      refining: false,
      selector: null,
      noSuggestion: false,
      removed: [],
      toast: null,
      session: null,
      activeItemId: null,
      paused: false,
      elapsed: 0,
      completedOpen: false,
      bonusRevealed: false,
      finalSummary: null,
      completionFlash: null,
      context: { ...BUNDLES[0].context },
    };
  }

  connectedCallback() {
    if (!this.boundClick) {
      this.boundClick = (event) => this.handleClick(event);
      this.shadowRoot.addEventListener("click", this.boundClick);
    }
    this.render();
    this.timer = window.setInterval(() => {
      if (this.state.view === "session" && this.state.activeItemId && !this.state.paused) {
        this.state.elapsed += 1;
        this.render();
      }
    }, 1000);
  }

  disconnectedCallback() {
    if (this.boundClick) this.shadowRoot.removeEventListener("click", this.boundClick);
    window.clearInterval(this.timer);
    window.clearTimeout(this.refineTimer);
    window.clearTimeout(this.summaryTimer);
  }

  set hass(value) {
    this._hass = value;
  }

  get bundle() {
    return BUNDLES[this.state.selected];
  }

  visibleChores() {
    const removed = new Set(this.state.removed);
    return this.bundle.chores.filter((chore) => !removed.has(chore.id));
  }

  refine(nextState = {}) {
    Object.assign(this.state, nextState, { refining: true, selector: null });
    this.render();
    window.clearTimeout(this.refineTimer);
    this.refineTimer = window.setTimeout(() => {
      this.state.refining = false;
      this.render();
    }, 650);
  }

  shuffle() {
    const next = (this.state.selected + 1) % BUNDLES.length;
    this.refine({
      selected: next,
      context: { ...BUNDLES[next].context },
      expanded: false,
      removed: [],
      noSuggestion: false,
    });
  }

  chooseChip(key, value) {
    const context = { ...this.state.context, [key]: value };
    const selected = this.pickBundle(context);
    this.refine({
      context,
      selected,
      removed: [],
      noSuggestion: value === "Any area" && context.time === "20 min" && context.energy === "low",
    });
  }

  pickBundle(context) {
    let best = 0;
    let bestScore = -1;
    BUNDLES.forEach((bundle, index) => {
      let score = 0;
      Object.keys(context).forEach((key) => {
        if (bundle.context[key] === context[key]) score += 2;
      });
      if (context.area !== "Any area" && bundle.chores.some((chore) => chore.area === context.area)) score += 3;
      if (score > bestScore) {
        bestScore = score;
        best = index;
      }
    });
    return best;
  }

  removeChore(choreId) {
    const removedChore = this.bundle.chores.find((chore) => chore.id === choreId);
    this.state.removed = [...this.state.removed, choreId];
    this.state.toast = removedChore;
    this.render();
  }

  undoRemove() {
    if (!this.state.toast) return;
    this.state.removed = this.state.removed.filter((id) => id !== this.state.toast.id);
    this.state.toast = null;
    this.render();
  }

  startSession() {
    const chores = this.visibleChores().map((chore, index) => ({
      ...chore,
      status: "pending",
      recommended: index === 0,
    }));
    this.state.view = "session";
    this.state.session = { title: this.bundle.title, chores };
    this.state.activeItemId = null;
    this.state.elapsed = 0;
    this.state.paused = false;
    this.state.completedOpen = false;
    this.state.bonusRevealed = false;
    this.state.completionFlash = null;
    this.render();
  }

  startChore(choreId) {
    this.state.session.chores = this.state.session.chores.map((chore) => ({
      ...chore,
      status: chore.id === choreId ? "ongoing" : chore.status === "ongoing" ? "pending" : chore.status,
      recommended: false,
    }));
    this.state.activeItemId = choreId;
    this.state.elapsed = 0;
    this.state.paused = false;
    this.render();
  }

  completeChore(choreId) {
    const chore = this.state.session.chores.find((item) => item.id === choreId);
    this.state.session.chores = this.state.session.chores.map((item) => ({
      ...item,
      status: item.id === choreId ? "completed" : item.status,
    }));
    this.state.activeItemId = null;
    this.state.elapsed = 0;
    this.state.paused = false;
    this.state.completionFlash = chore;
    this.render();
    window.setTimeout(() => {
      this.state.completionFlash = null;
      this.render();
    }, 900);
  }

  revealBonus() {
    this.state.bonusRevealed = true;
    this.render();
  }

  acceptBonus() {
    this.state.session.chores.push({ ...BONUS_CHORE, status: "pending", recommended: true, bonus: true });
    this.state.bonusRevealed = false;
    this.render();
  }

  finishSession() {
    const completed = this.state.session.chores.filter((chore) => chore.status === "completed");
    this.state.finalSummary = {
      chores: completed,
      keeps: completed.reduce((total, chore) => total + chore.keeps, 0) + this.bundle.bonusKeeps,
      title: this.state.session.title,
    };
    this.state.view = "summary";
    this.render();
    window.clearTimeout(this.summaryTimer);
    this.summaryTimer = window.setTimeout(() => this.resetReady(), 2400);
  }

  resetReady() {
    this.state.view = "ready";
    this.state.session = null;
    this.state.finalSummary = null;
    this.state.expanded = false;
    this.state.removed = [];
    this.state.toast = null;
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `${this.styles()}<main>${this.renderMain()}</main>`;
  }

  renderMain() {
    if (this.state.view === "session") return this.renderSession();
    if (this.state.view === "summary") return this.renderSummary();
    return this.renderReady();
  }

  renderReady() {
    const bundle = this.bundle;
    const chores = this.visibleChores();
    const duration = chores.reduce((total, chore) => total + chore.minutes, 0);
    const areaNames = [...new Set(chores.map((chore) => chore.area))];
    const areaLine = areaNames.length === 1 ? `<span><ha-icon icon="mdi:floor-plan"></ha-icon>${areaNames[0]}</span>` : "";
    return `
      <section class="hero">
        <p class="eyebrow">Ready Now</p>
        <h1>${this.state.noSuggestion ? NO_SUGGESTION.greeting : bundle.greeting}</h1>
        <div class="chips">${Object.keys(CHIPS).map((key) => this.renderChip(key)).join("")}</div>
      </section>
      ${this.state.noSuggestion ? this.renderNoSuggestion() : `
      <section class="suggestion ${this.state.refining ? "refining" : ""}">
        <div class="refine-line">${this.state.refining ? "Finding a better fit..." : "Suggested Chore Bundle"}</div>
        <div class="suggestion-head">
          <div>
            <h2>${bundle.title}</h2>
            <p>${bundle.reason}</p>
          </div>
          <button class="icon-button" aria-label="Shuffle suggestion" title="Shuffle suggestion" data-action="shuffle">
            <ha-icon icon="mdi:shuffle-variant"></ha-icon>
          </button>
        </div>
        <div class="meta">
          <span><ha-icon icon="mdi:timer-outline"></ha-icon>${duration} min</span>
          ${areaLine}
          <span><ha-icon icon="mdi:heart-pulse"></ha-icon>${bundle.impact.areaName} ${bundle.impact.areaBefore} -> ${bundle.impact.areaAfter}</span>
        </div>
        <div class="impact">${bundle.impact.areaName} +${bundle.impact.areaAfter - bundle.impact.areaBefore} · ${bundle.impact.label}</div>
        ${this.state.expanded ? this.renderBundleDetails(chores, areaNames) : ""}
        <div class="actions">
          <button class="primary" data-action="start-session">Choose this reset</button>
          <button class="secondary" data-action="toggle-expand">${this.state.expanded ? "Show less" : "Show details"}</button>
        </div>
      </section>`}
      ${this.state.toast ? this.renderToast() : ""}
    `;
  }

  renderNoSuggestion() {
    return `
      <section class="suggestion quiet ${this.state.refining ? "refining" : ""}">
        <div class="suggestion-head">
          <div>
            <h2>${NO_SUGGESTION.greeting}</h2>
            <p>${NO_SUGGESTION.message}</p>
          </div>
          <button class="icon-button" aria-label="Shuffle suggestion" title="Shuffle suggestion" data-action="shuffle">
            <ha-icon icon="mdi:shuffle-variant"></ha-icon>
          </button>
        </div>
      </section>
    `;
  }

  renderChip(key) {
    const chip = CHIPS[key];
    const open = this.state.selector === key;
    return `
      <div class="chip-wrap">
        <button class="chip ${open ? "open" : ""}" data-chip="${key}">
          <ha-icon icon="${chip.icon}"></ha-icon>
          <span>${chip.label}</span>
          <strong>${this.state.context[key]}</strong>
        </button>
        ${open ? `<div class="selector">${chip.options.map((option) => `
          <button class="${this.state.context[key] === option ? "selected" : ""}" data-chip-value="${key}:${option}">${option}</button>
        `).join("")}</div>` : ""}
      </div>
    `;
  }

  renderBundleDetails(chores, areaNames) {
    const showArea = areaNames.length > 1;
    return `
      <div class="details">
        <div class="keeps-line"><span>+${this.bundle.bonusKeeps} Keeps bonus</span><span>The home gives a little back.</span></div>
        ${chores.map((chore) => `
          <article class="chore-row">
            <div>
              <strong>${chore.name}</strong>
              <span>${chore.minutes} min · +${chore.keeps} Keeps${showArea ? ` · ${chore.area}` : ""}</span>
              <small>${chore.keepLine}</small>
            </div>
            <button class="ghost-icon" aria-label="Remove ${chore.name}" title="Remove" data-remove="${chore.id}">
              <ha-icon icon="mdi:close"></ha-icon>
            </button>
          </article>
        `).join("")}
      </div>
    `;
  }

  renderSession() {
    const session = this.state.session;
    const remaining = session.chores.filter((chore) => chore.status !== "completed");
    const completed = session.chores.filter((chore) => chore.status === "completed");
    const allDone = remaining.length === 0;
    return `
      <section class="session-top">
        <p class="eyebrow">Chore Session</p>
        <h1>${allDone ? "That reset helped." : session.title}</h1>
        ${this.state.activeItemId ? this.renderTimer() : `<p class="support">Start with any Chore. Homekeep will keep the next step clear.</p>`}
      </section>
      ${this.state.completionFlash ? `<div class="flash">+${this.state.completionFlash.keeps} Keeps · That helped.</div>` : ""}
      <section class="session-list">
        ${remaining.map((chore, index) => this.renderSessionChore(chore, index)).join("")}
        ${completed.length ? this.renderCompletedSummary(completed) : ""}
      </section>
      ${allDone ? this.renderEnding() : ""}
    `;
  }

  renderTimer() {
    return `
      <div class="timer">
        <span>${this.formatTime(this.state.elapsed)}</span>
        <button class="secondary" data-action="toggle-pause">${this.state.paused ? "Resume" : "Pause"}</button>
      </div>
    `;
  }

  renderSessionChore(chore, index) {
    const ongoing = chore.status === "ongoing";
    const recommended = chore.recommended || (!this.state.activeItemId && index === 0);
    return `
      <article class="session-chore ${ongoing ? "ongoing" : ""}">
        <div>
          ${recommended ? `<span class="next">Suggested next</span>` : ""}
          <h2>${chore.name}</h2>
          <p>${chore.area} · ${chore.minutes} min · +${chore.keeps} Keeps</p>
        </div>
        <div class="row-actions">
          ${ongoing ? `<button class="primary" data-complete="${chore.id}">Complete</button>` : `<button class="secondary" data-start="${chore.id}">Start</button>`}
          <button class="ghost" title="Skip" aria-label="Skip ${chore.name}">Skip</button>
          <button class="ghost" title="Snooze" aria-label="Snooze ${chore.name}">Snooze</button>
        </div>
      </article>
    `;
  }

  renderCompletedSummary(completed) {
    return `
      <section class="completed">
        <button data-action="toggle-completed">
          <span>${completed.length} completed</span>
          <ha-icon icon="${this.state.completedOpen ? "mdi:chevron-up" : "mdi:chevron-down"}"></ha-icon>
        </button>
        ${this.state.completedOpen ? `<div>${completed.map((chore) => `<p>${chore.name} · +${chore.keeps} Keeps</p>`).join("")}</div>` : ""}
      </section>
    `;
  }

  renderEnding() {
    return `
      <section class="ending">
        <h2>The planned reset is complete.</h2>
        <p>Stop here with the room cared for, or add one small Bonus Chore.</p>
        ${this.state.bonusRevealed ? `
          <article class="bonus">
            <div>
              <strong>${BONUS_CHORE.name}</strong>
              <span>${BONUS_CHORE.area} · ${BONUS_CHORE.minutes} min · +${BONUS_CHORE.keeps} Keeps</span>
              <small>${BONUS_CHORE.keepLine}</small>
            </div>
            <button class="icon-button disabled" aria-label="Find another Bonus Chore" title="Redraw is not wired yet">
              <ha-icon icon="mdi:dice-3-outline"></ha-icon>
            </button>
          </article>
          <button class="secondary" data-action="accept-bonus">Add this one</button>
        ` : ""}
        <div class="actions">
          <button class="primary" data-action="finish">Done for now</button>
          <button class="secondary" data-action="reveal-bonus">One more</button>
        </div>
      </section>
    `;
  }

  renderSummary() {
    const summary = this.state.finalSummary;
    return `
      <section class="summary">
        <p class="eyebrow">Done for now</p>
        <h1>${summary.title} is complete.</h1>
        <p>${summary.chores.map((chore) => chore.name).join(", ")}.</p>
        <div class="impact">+${summary.keeps} Keeps · The home feels a little lighter.</div>
      </section>
    `;
  }

  renderToast() {
    return `
      <div class="toast">
        <span>Removed ${this.state.toast.name}</span>
        <button data-action="undo-remove">Undo</button>
        <button>Suggest less in short sessions</button>
      </div>
    `;
  }

  formatTime(seconds) {
    const minutes = String(Math.floor(seconds / 60)).padStart(2, "0");
    const rest = String(seconds % 60).padStart(2, "0");
    return `${minutes}:${rest}`;
  }

  styles() {
    return `
      <style>
        :host { display: block; min-height: 100vh; color: var(--primary-text-color, #1f2933); background: var(--primary-background-color, #f7f8f5); }
        main { max-width: 860px; margin: 0 auto; padding: clamp(20px, 5vw, 48px) 18px 32px; box-sizing: border-box; }
        button { font: inherit; }
        .hero, .session-top, .summary { text-align: center; padding: 26px 0 18px; }
        .eyebrow { margin: 0 0 10px; color: #5b6b61; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0; font-weight: 700; }
        h1 { margin: 0 auto; max-width: 760px; font-size: clamp(2rem, 6vw, 4.1rem); line-height: 1.02; font-weight: 750; letter-spacing: 0; }
        h2 { margin: 0; font-size: 1.25rem; letter-spacing: 0; }
        p { margin: 0; line-height: 1.45; }
        .chips { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-top: 26px; }
        .chip-wrap { position: relative; }
        .chip, .selector button, .secondary, .ghost, .primary, .completed button, .toast button { min-height: 42px; border-radius: 999px; border: 1px solid rgba(68, 83, 74, 0.2); background: rgba(255,255,255,0.76); color: inherit; padding: 0 14px; cursor: pointer; }
        .chip { display: flex; align-items: center; gap: 7px; }
        .chip ha-icon { width: 18px; color: #55756a; }
        .chip span { color: #637066; }
        .chip strong { font-weight: 700; }
        .chip.open { background: #e8f0eb; border-color: #7da58d; }
        .selector { position: absolute; z-index: 5; top: 48px; left: 0; min-width: 170px; padding: 8px; display: grid; gap: 6px; background: #ffffff; border: 1px solid rgba(68, 83, 74, 0.22); box-shadow: 0 18px 45px rgba(30, 45, 35, 0.15); border-radius: 8px; }
        .selector button { border-radius: 8px; text-align: left; background: #fff; }
        .selector .selected { background: #e9f3ee; }
        .suggestion, .session-list, .ending { margin-top: 18px; padding: 22px; border: 1px solid rgba(68, 83, 74, 0.18); border-radius: 8px; background: rgba(255,255,255,0.74); box-shadow: 0 20px 70px rgba(43, 58, 48, 0.08); }
        .suggestion.refining { filter: blur(0.5px); opacity: 0.78; }
        .refine-line { min-height: 20px; margin-bottom: 8px; color: #617064; font-size: 0.9rem; }
        .suggestion-head { display: grid; grid-template-columns: minmax(0, 1fr) 44px; gap: 16px; align-items: start; }
        .suggestion-head p, .support, .ending p { color: #5e6b62; margin-top: 6px; }
        .icon-button, .ghost-icon { width: 42px; height: 42px; border-radius: 50%; border: 1px solid rgba(68, 83, 74, 0.22); display: inline-flex; align-items: center; justify-content: center; background: #fff; cursor: pointer; }
        .icon-button.disabled { opacity: 0.55; cursor: default; }
        .meta { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 12px; }
        .meta span, .impact, .keeps-line { display: inline-flex; align-items: center; gap: 6px; min-height: 34px; padding: 0 10px; border-radius: 999px; background: #eef4ef; color: #315143; font-weight: 700; }
        .meta ha-icon { width: 17px; }
        .impact { background: #f4efe2; color: #69502b; }
        .details { margin-top: 16px; display: grid; gap: 10px; }
        .keeps-line { justify-content: space-between; border-radius: 8px; padding: 10px 12px; }
        .keeps-line span:last-child { color: #647064; font-weight: 500; }
        .chore-row, .session-chore, .bonus { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 12px; align-items: center; padding: 14px; border-radius: 8px; background: rgba(247, 248, 245, 0.92); }
        .chore-row span, .chore-row small, .session-chore p, .bonus span, .bonus small { display: block; color: #647064; margin-top: 4px; }
        .actions, .row-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; }
        .primary { border-color: #2f6f5d; background: #2f6f5d; color: #fff; font-weight: 750; }
        .secondary { background: #fff; font-weight: 700; }
        .ghost { min-width: 42px; padding: 0 12px; background: transparent; color: #5f6b63; }
        .session-list { display: grid; gap: 12px; }
        .session-chore.ongoing { outline: 2px solid #72a88d; background: #edf6f1; }
        .next { display: inline-block; margin-bottom: 6px; color: #2f6f5d; font-weight: 700; font-size: 0.82rem; }
        .timer { display: inline-flex; align-items: center; gap: 12px; margin-top: 16px; padding: 8px 8px 8px 18px; border-radius: 999px; background: #fff; box-shadow: 0 10px 28px rgba(43, 58, 48, 0.1); }
        .timer span { font-size: 1.5rem; font-variant-numeric: tabular-nums; font-weight: 800; }
        .flash { position: sticky; top: 12px; z-index: 3; margin: 0 auto 12px; width: fit-content; padding: 10px 16px; border-radius: 999px; color: #315143; background: #dff1e5; font-weight: 800; box-shadow: 0 12px 30px rgba(43, 58, 48, 0.12); }
        .completed { padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.68); }
        .completed button { width: 100%; display: flex; justify-content: space-between; align-items: center; background: transparent; border: 0; padding: 0; }
        .completed p { margin-top: 8px; color: #647064; }
        .ending { text-align: center; }
        .ending .actions { justify-content: center; }
        .bonus { margin: 16px 0 0; text-align: left; }
        .summary { min-height: 70vh; display: grid; align-content: center; justify-items: center; gap: 14px; }
        .toast { position: fixed; left: 50%; bottom: 24px; transform: translateX(-50%); display: flex; gap: 8px; align-items: center; max-width: calc(100vw - 28px); padding: 10px; border-radius: 8px; background: #1f2933; color: #fff; box-shadow: 0 18px 45px rgba(0,0,0,0.22); }
        .toast button { min-height: 36px; background: rgba(255,255,255,0.12); color: #fff; border-color: rgba(255,255,255,0.24); }
        @media (max-width: 620px) {
          main { padding-left: 12px; padding-right: 12px; }
          .suggestion, .session-list, .ending { padding: 16px; }
          .chore-row, .session-chore, .bonus { grid-template-columns: 1fr; }
          .row-actions, .actions { display: grid; grid-template-columns: 1fr 1fr; }
          .primary, .secondary, .ghost { width: 100%; }
          .toast { flex-wrap: wrap; justify-content: center; }
        }
      </style>
    `;
  }

  handleClick(event) {
    const target = event.target.closest("button");
    if (!target) return;
    const action = target.dataset.action;
    if (target.dataset.chip) {
      this.state.selector = this.state.selector === target.dataset.chip ? null : target.dataset.chip;
      this.render();
      return;
    }
    if (target.dataset.chipValue) {
      const [key, value] = target.dataset.chipValue.split(":");
      this.chooseChip(key, value);
      return;
    }
    if (target.dataset.remove) this.removeChore(target.dataset.remove);
    if (target.dataset.start) this.startChore(target.dataset.start);
    if (target.dataset.complete) this.completeChore(target.dataset.complete);
    if (action === "start-session") this.startSession();
    if (action === "toggle-expand") {
      this.state.expanded = !this.state.expanded;
      this.render();
    }
    if (action === "shuffle") this.shuffle();
    if (action === "toggle-pause") {
      this.state.paused = !this.state.paused;
      this.render();
    }
    if (action === "toggle-completed") {
      this.state.completedOpen = !this.state.completedOpen;
      this.render();
    }
    if (action === "reveal-bonus") this.revealBonus();
    if (action === "accept-bonus") this.acceptBonus();
    if (action === "finish") this.finishSession();
    if (action === "undo-remove") this.undoRemove();
  }
}

customElements.define("homekeep-panel", HomekeepPanel);

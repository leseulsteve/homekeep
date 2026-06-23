const CHIPS = {
  time: {
    label: "Time",
    icon: "mdi:clock-outline",
  },
  mood: {
    label: "Mood",
    icon: "mdi:weather-partly-cloudy",
    options: ["auto", "low", "quiet", "focused", "restless", "ready"],
  },
  area: {
    label: "Area",
    icon: "mdi:floor-plan",
    options: ["Auto", "Kitchen", "Entryway", "Bathroom", "Laundry", "Living room"],
  },
};

const BUNDLES = [
  {
    id: "kitchen-reset",
    title: "Kitchen Reset",
    duration: 15,
    context: { time: "15 min", capacity: "steady", mood: "focused", goal: "visible lift", area: "Kitchen" },
    reason: "The kitchen has the clearest lift for a short reset.",
    greeting: "Good evening. I found something small that can make the home feel lighter.",
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
    context: { time: "10 min", capacity: "low", mood: "low", goal: "quick wins", area: "Entryway" },
    reason: "A light entryway pass gives the home a visible welcome point.",
    greeting: "Let's keep this light. There is a small visible lift ready.",
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
    context: { time: "10 min", capacity: "low", mood: "quiet", goal: "fresh start", area: "Bathroom" },
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
    context: { time: "25 min", capacity: "strong", mood: "ready", goal: "overdue care", area: "Laundry" },
    reason: "Laundry is stale enough to be worth a fuller pass.",
    greeting: "There is enough room for a focused pass when you want one.",
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
    context: { time: "5 min", capacity: "low", mood: "auto", goal: "quick wins", area: "Auto" },
    reason: "A tiny mixed-area reset keeps the evening gentle.",
    greeting: "Five gentle minutes can still help the home feel cared for.",
    impact: { label: "Small home lift", home: 3, areaName: "Home", areaBefore: 74, areaAfter: 77 },
    bonusKeeps: 2,
    chores: [
      { id: "clear-coffee-table", name: "Clear coffee table", area: "Living room", minutes: 3, keeps: 4, keepLine: "opens the room back up" },
      { id: "gather-stray-cups", name: "Gather stray cups", area: "Kitchen", minutes: 2, keeps: 3, keepLine: "prevents a small morning pileup" },
    ],
  },
];

const TIME_AUTO = "Auto";

function inferCapacityFromMood(mood) {
  if (mood === "low" || mood === "quiet") return "low";
  if (mood === "restless") return "mobile";
  if (mood === "ready") return "strong";
  if (mood === "focused") return "steady";
  return "auto";
}

function inferGoalFromMood(mood) {
  if (mood === "low") return "quick wins";
  if (mood === "quiet") return "fresh start";
  if (mood === "focused") return "overdue care";
  if (mood === "restless") return "visible lift";
  if (mood === "ready") return "overdue care";
  return "visible lift";
}

function softenCapacity(capacity) {
  if (capacity === "strong" || capacity === "mobile") return "steady";
  if (capacity === "steady") return "low";
  return capacity;
}

const NO_SUGGESTION = {
  greeting: "Nothing fits this moment yet.",
  message: "Try changing the time, mood, or area.",
};

const OPTIONAL_CHORE_CANDIDATES = [
  {
    id: "water-kitchen-herbs",
    name: "Water kitchen herbs",
    area: "Kitchen",
    minutes: 3,
    keeps: 4,
    keepLine: "keeps a tiny bit of green cared for",
    healthImpact: 5,
    staleness: 3,
    fits: ["low", "quiet", "auto"],
  },
  {
    id: "straighten-entry-shoes",
    name: "Straighten entry shoes",
    area: "Entryway",
    minutes: 3,
    keeps: 4,
    keepLine: "keeps the doorway easy to cross",
    healthImpact: 6,
    staleness: 5,
    fits: ["low", "restless", "auto"],
  },
  {
    id: "wipe-bathroom-mirror",
    name: "Wipe bathroom mirror",
    area: "Bathroom",
    minutes: 4,
    keeps: 5,
    keepLine: "adds a small clean finish",
    healthImpact: 7,
    staleness: 4,
    fits: ["quiet", "focused", "auto"],
  },
  {
    id: "clear-mail-stack",
    name: "Clear the mail stack",
    area: "Entryway",
    minutes: 5,
    keeps: 6,
    keepLine: "keeps the landing spot from building up",
    healthImpact: 7,
    staleness: 7,
    fits: ["focused", "restless", "ready"],
  },
  {
    id: "wipe-stove-face",
    name: "Wipe stove front",
    area: "Kitchen",
    minutes: 4,
    keeps: 5,
    keepLine: "gives the kitchen one more clean edge",
    healthImpact: 8,
    staleness: 6,
    fits: ["focused", "ready", "auto"],
  },
  {
    id: "clear-living-room-blankets",
    name: "Fold living room blankets",
    area: "Living room",
    minutes: 4,
    keeps: 5,
    keepLine: "makes the room feel settled again",
    healthImpact: 5,
    staleness: 4,
    fits: ["low", "quiet", "auto"],
  },
  {
    id: "empty-dryer-lint",
    name: "Empty dryer lint",
    area: "Laundry",
    minutes: 2,
    keeps: 3,
    keepLine: "keeps the next load easier to start",
    healthImpact: 6,
    staleness: 6,
    fits: ["low", "focused", "ready"],
  },
];

const GREETINGS_BY_CONTEXT = {
  low: [
    "Let's keep this light. The home can still get a little care.",
    "A small, gentle pass can be enough for right now.",
  ],
  quiet: [
    "A quiet bit of care can fit here.",
    "There is a calm way to help the home right now.",
  ],
  focused: [
    "There is room for one useful pass.",
    "A clear reset can move the home forward.",
  ],
  high: [
    "There is room for one useful pass.",
    "A clear reset can move the home forward.",
  ],
  restless: [
    "A visible reset can give that restlessness somewhere useful to go.",
    "There is a small reset with some motion in it.",
  ],
  ready: [
    "The home has a fuller reset ready if you want to lean in.",
    "There is room to push a little where it matters.",
  ],
  short: [
    "A few minutes can still make the home feel lighter.",
    "Something small can still help.",
  ],
  default: [
    "Good evening. I found something small that can make the home feel lighter.",
    "The home has a useful place to start.",
  ],
};

function pickFrom(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function pickRightNowGreeting(context) {
  if (context.time === "5 min") return pickFrom(GREETINGS_BY_CONTEXT.short);
  const candidates = GREETINGS_BY_CONTEXT[context.mood] || GREETINGS_BY_CONTEXT.default;
  return pickFrom(candidates);
}

function timeOptionsForContext(context) {
  if (["low", "quiet"].includes(context.mood) || context.capacity === "low") {
    return [TIME_AUTO, "5 min", "10 min", "15 min"];
  }
  if (["focused", "restless", "ready"].includes(context.mood) || ["mobile", "strong"].includes(context.capacity)) {
    return [TIME_AUTO, "10 min", "15 min", "25 min"];
  }
  return [TIME_AUTO, "5 min", "10 min", "15 min", "25 min"];
}

function inferredTimeScore(context, bundleDuration) {
  if (["low", "quiet"].includes(context.mood) || context.capacity === "low") {
    if (bundleDuration <= 10) return 3;
    return bundleDuration <= 15 ? 1 : 0;
  }
  if (context.mood === "ready" || context.capacity === "strong") {
    return bundleDuration >= 15 ? 3 : 1;
  }
  if (context.mood === "restless") {
    return bundleDuration >= 10 && bundleDuration <= 20 ? 3 : 1;
  }
  if (context.mood === "focused") {
    return bundleDuration >= 10 && bundleDuration <= 15 ? 3 : 1;
  }
  return bundleDuration <= 15 ? 2 : 1;
}

function capacityFitScore(context, bundleCapacity) {
  if (context.capacity === "auto") return 1;
  if (context.capacity === bundleCapacity) return 2;
  if (context.capacity === "mobile" && ["steady", "strong"].includes(bundleCapacity)) return 1;
  if (context.capacity === "steady" && bundleCapacity === "mobile") return 1;
  return 0;
}

function timeFitScore(context, bundleDuration) {
  const selectedTime = context.time;
  if (selectedTime === TIME_AUTO) return inferredTimeScore(context, bundleDuration);
  const minutes = Number.parseInt(selectedTime, 10);
  if (!Number.isFinite(minutes)) return 0;
  if (bundleDuration <= minutes) return 2;
  return bundleDuration <= minutes + 5 ? 1 : 0;
}

function bundleHardRejects(context, bundle) {
  const selectedMinutes = context.time === TIME_AUTO ? null : Number.parseInt(context.time, 10);
  if (Number.isFinite(selectedMinutes) && bundle.duration > selectedMinutes + 5) return true;
  if (context.area !== "Auto" && !bundle.chores.some((chore) => chore.area === context.area)) return true;
  if (["low", "quiet"].includes(context.mood) && bundle.duration > 15) return true;
  return false;
}

function bundleHomeNeedScore(bundle) {
  const impactGain = Math.max(0, bundle.impact.areaAfter - bundle.impact.areaBefore);
  const lowStartingHealth = Math.max(0, 80 - bundle.impact.areaBefore);
  const staleHint = bundle.context.goal === "overdue care" ? 8 : 0;
  return impactGain * 1.4 + lowStartingHealth * 0.45 + staleHint;
}

function bundleUserFitScore(context, bundle) {
  let score = timeFitScore(context, bundle.duration) * 12 + capacityFitScore(context, bundle.context.capacity) * 8;
  if (bundle.context.mood === context.mood || context.mood === "auto") score += 10;
  if (bundle.context.goal === context.goal) score += 5;
  if (context.area !== "Auto" && bundle.chores.some((chore) => chore.area === context.area)) score += 18;
  if (context.area === "Auto" && bundle.impact.areaName !== "Home") score += 4;
  if (["low", "quiet"].includes(context.mood) && bundle.duration <= 10) score += 10;
  if (context.mood === "ready" && bundle.duration >= 15) score += 8;
  return score;
}

function bundleDiversityScore(bundle) {
  const areas = new Set(bundle.chores.map((chore) => chore.area));
  const firstWords = new Set(bundle.chores.map((chore) => chore.name.split(" ")[0]));
  let score = firstWords.size * 2;
  if (areas.size === 1) score += 4;
  if (areas.size > 2) score -= 5;
  return score;
}

function bundleRecommendationScore(context, bundle) {
  const homeNeed = bundleHomeNeedScore(bundle);
  const userFit = bundleUserFitScore(context, bundle);
  const careNudge = Math.min(homeNeed * 0.18, 10);
  const diversity = bundleDiversityScore(bundle);
  return userFit * 0.62 + homeNeed * 0.28 + careNudge + diversity;
}

function displayContextValue(value) {
  return value === "Auto" ? "Best fit" : value;
}

function contextFitLine(context, bundle, duration, areaNames, areaExplicit) {
  if (areaExplicit && context.area !== "Auto") return `Kept to ${context.area} because you picked it.`;
  const moodText = context.mood === "auto" ? "balanced" : context.mood;
  const timeText = context.time === TIME_AUTO ? `${duration}-minute` : context.time.replace(" min", "-minute");
  const areaText = context.area !== "Auto" ? context.area : areaNames.length === 1 ? areaNames[0] : "the home";
  return `Picked for a ${moodText} ${timeText} reset in ${areaText}.`;
}

function noSuggestionMessage(context) {
  if (context.area !== "Auto") return `Nothing fits ${context.area} with this mood right now.`;
  return NO_SUGGESTION.message;
}

function scoreOptionalChore(candidate, context, sessionArea) {
  let score = candidate.healthImpact + candidate.staleness;
  if (candidate.minutes <= 3) score += 4;
  else if (candidate.minutes <= 5) score += 2;
  if (["low", "quiet"].includes(context.mood) && candidate.minutes <= 4) score += 4;
  if (["focused", "ready"].includes(context.mood) && candidate.healthImpact >= 7) score += 3;
  if (context.mood === "restless" && candidate.area !== sessionArea) score += 2;
  if (candidate.fits.includes(context.mood) || candidate.fits.includes("auto")) score += 3;
  if (context.area !== "Auto" && candidate.area === context.area) score += 4;
  if (context.area === "Auto" && candidate.area === sessionArea) score += 2;
  return score;
}

function publicOptionalChore(candidate) {
  const { healthImpact, staleness, fits, ...chore } = candidate;
  return chore;
}

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
      session: null,
      activeItemId: null,
      paused: false,
      elapsed: 0,
      optionalOffered: false,
      finalSummary: null,
      completionFlash: null,
      context: {
        ...BUNDLES[0].context,
        time: TIME_AUTO,
        area: "Auto",
        capacity: inferCapacityFromMood(BUNDLES[0].context.mood),
        goal: inferGoalFromMood(BUNDLES[0].context.mood),
      },
      areaExplicit: false,
      timeExplicit: false,
      moodExplicit: false,
      rightNowGreeting: pickRightNowGreeting(BUNDLES[0].context),
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

  getChipOptions(key) {
    const options = key === "time" ? timeOptionsForContext(this.state.context) : CHIPS[key].options;
    if (key === "time" && !options.includes(this.state.context.time)) {
      return [this.state.context.time, ...options];
    }
    return options;
  }

  visibleChores() {
    const removed = new Set(this.state.removed);
    return this.bundle.chores.filter((chore) => !removed.has(chore.id));
  }

  hasRemovedPhysicalChore() {
    return this.bundle.chores.some((chore) => this.state.removed.includes(chore.id) && chore.minutes >= 6);
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
    const context = {
      ...this.state.context,
      time: this.state.timeExplicit ? this.state.context.time : TIME_AUTO,
      area: this.state.areaExplicit ? this.state.context.area : "Auto",
    };
    if (context.mood === "auto") {
      const nextIndex = (this.state.selected + 1) % BUNDLES.length;
      context.capacity = this.hasRemovedPhysicalChore() ? softenCapacity(BUNDLES[nextIndex].context.capacity) : BUNDLES[nextIndex].context.capacity;
      context.goal = BUNDLES[nextIndex].context.goal;
    } else {
      context.capacity = inferCapacityFromMood(context.mood);
      context.goal = inferGoalFromMood(context.mood);
    }
    if (this.hasRemovedPhysicalChore()) context.capacity = softenCapacity(context.capacity);
    const next = this.pickBundle(context, this.state.selected);
    this.refine({
      selected: next,
      context,
      areaExplicit: this.state.areaExplicit,
      timeExplicit: this.state.timeExplicit,
      moodExplicit: this.state.moodExplicit,
      expanded: false,
      removed: [],
      noSuggestion: false,
    });
  }

  chooseChip(key, value) {
    const context = { ...this.state.context, [key]: value };
    if (key === "mood") {
      context.capacity = inferCapacityFromMood(value);
      context.goal = inferGoalFromMood(value);
    }
    const areaExplicit = key === "area" ? value !== "Auto" : this.state.areaExplicit;
    const timeExplicit = key === "time" ? value !== TIME_AUTO : this.state.timeExplicit;
    const moodExplicit = key === "mood" ? value !== "auto" : this.state.moodExplicit;
    const selected = this.pickBundle(context);
    const shouldRegenerateGreeting = ["time", "mood"].includes(key);
    this.refine({
      context,
      areaExplicit,
      timeExplicit,
      moodExplicit,
      selected,
      rightNowGreeting: shouldRegenerateGreeting ? pickRightNowGreeting(context) : this.state.rightNowGreeting,
      removed: [],
      noSuggestion: context.area === "Living room" && context.mood === "ready",
    });
  }

  pickBundle(context, excludeIndex = null) {
    let best = 0;
    let bestScore = -1;
    BUNDLES.forEach((bundle, index) => {
      if (index === excludeIndex && BUNDLES.length > 1) return;
      if (bundleHardRejects(context, bundle)) return;
      const score = bundleRecommendationScore(context, bundle);
      if (score > bestScore) {
        bestScore = score;
        best = index;
      }
    });
    return best;
  }

  removeChore(choreId) {
    if (this.state.removed.includes(choreId)) return;
    this.state.removed = [...this.state.removed, choreId];
    this.render();
  }

  restoreChore(choreId) {
    this.state.removed = this.state.removed.filter((id) => id !== choreId);
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
    this.state.optionalOffered = false;
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

  markNextPendingRecommended() {
    let foundNext = false;
    this.state.session.chores = this.state.session.chores.map((chore) => {
      if (chore.status !== "pending" || foundNext) return { ...chore, recommended: false };
      foundNext = true;
      return { ...chore, recommended: true };
    });
  }

  completionFlashFor(chore, bundleJustCompleted) {
    if (bundleJustCompleted) {
      return {
        keeps: chore.keeps,
        level: "bundle",
        message: "Suggested reset complete. The home feels lighter.",
      };
    }
    if (chore.optional) {
      const optionalCompleted = this.state.session.chores.filter((item) => item.optional && item.status === "completed").length;
      const messages = [
        "A little extra care. Nice.",
        "That extra bit is adding up.",
        "You gave the home a real lift.",
      ];
      return {
        keeps: chore.keeps,
        level: `optional optional-${Math.min(optionalCompleted, 3)}`,
        message: messages[Math.min(optionalCompleted, messages.length) - 1],
      };
    }
    return {
      keeps: chore.keeps,
      level: "chore",
      message: "That helped.",
    };
  }

  completeChore(choreId) {
    const chore = this.state.session.chores.find((item) => item.id === choreId);
    this.state.session.chores = this.state.session.chores.map((item) => ({
      ...item,
      status: item.id === choreId ? "completed" : item.status,
      recommended: false,
    }));
    this.state.activeItemId = null;
    this.state.elapsed = 0;
    this.state.paused = false;
    const bundleJustCompleted = !chore.optional && !this.state.optionalOffered && !this.state.session.chores.some((item) => !item.optional && (item.status === "pending" || item.status === "ongoing"));
    this.state.completionFlash = this.completionFlashFor(chore, bundleJustCompleted);
    this.markNextPendingRecommended();
    this.offerOptionalChoresIfReady();
    this.render();
    window.setTimeout(() => {
      this.state.completionFlash = null;
      this.render();
    }, this.state.completionFlash.level === "chore" ? 900 : 1300);
  }

  skipChore(choreId) {
    const skippedActiveChore = this.state.activeItemId === choreId;
    this.state.session.chores = this.state.session.chores.map((item) => ({
      ...item,
      status: item.id === choreId ? "skipped" : item.status,
      recommended: false,
    }));
    if (skippedActiveChore) {
      this.state.activeItemId = null;
      this.state.elapsed = 0;
      this.state.paused = false;
    }
    if (!this.state.activeItemId) this.markNextPendingRecommended();
    this.render();
  }

  offerOptionalChoresIfReady() {
    if (this.state.optionalOffered) return;
    const plannedOpen = this.state.session.chores.some((chore) => !chore.optional && (chore.status === "pending" || chore.status === "ongoing"));
    if (plannedOpen) return;
    this.state.optionalOffered = true;
    const excluded = new Set([
      ...this.state.session.chores.map((chore) => chore.id),
      ...this.state.removed,
      ...this.state.session.chores.filter((chore) => chore.status === "skipped").map((chore) => chore.id),
    ]);
    const sessionArea = this.bundle.impact.areaName;
    const optionalChores = OPTIONAL_CHORE_CANDIDATES
      .filter((chore) => chore.minutes <= 5 && !excluded.has(chore.id))
      .map((chore) => ({ chore, score: scoreOptionalChore(chore, this.state.context, sessionArea) }))
      .sort((a, b) => b.score - a.score || a.chore.minutes - b.chore.minutes || a.chore.name.localeCompare(b.chore.name))
      .slice(0, 3)
      .map(({ chore }, index) => ({
        ...publicOptionalChore(chore),
        status: "pending",
        recommended: index === 0,
        optional: true,
      }));
    this.state.session.chores = [...this.state.session.chores, ...optionalChores];
  }

  finishSession() {
    const completed = this.state.session.chores.filter((chore) => chore.status === "completed");
    const intactBonus = this.state.removed.length === 0 ? this.bundle.bonusKeeps : 0;
    this.state.finalSummary = {
      chores: completed,
      keeps: completed.reduce((total, chore) => total + chore.keeps, 0) + intactBonus,
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
    const impactScope = areaNames.length === 1 ? areaNames[0] : bundle.impact.areaName;
    const healthGain = bundle.impact.areaAfter - bundle.impact.areaBefore;
    const fitLine = contextFitLine(this.state.context, bundle, duration, areaNames, this.state.areaExplicit);
    return `
      <section class="hero">
        <h1>${this.state.noSuggestion ? NO_SUGGESTION.greeting : this.state.rightNowGreeting}</h1>
        <div class="chips">
          ${Object.keys(CHIPS).map((key) => this.renderChip(key)).join("")}
          <button class="chip randomize" aria-label="Try another fit" title="Try another fit" data-action="shuffle">
            <ha-icon icon="mdi:shuffle-variant"></ha-icon>
          </button>
        </div>
      </section>
      ${this.state.noSuggestion ? this.renderNoSuggestion() : `
      <section class="suggestion ${this.state.refining ? "refining" : ""}">
        <div class="suggestion-head">
          <div>
            <h2>${bundle.title}</h2>
            <p>${bundle.reason}</p>
            <p class="fit-line">${fitLine}</p>
          </div>
          <button class="primary benefit-action" data-action="start-session" aria-label="Choose this reset">
            <span>
              <strong>${bundle.impact.areaName} ${bundle.impact.areaAfter - bundle.impact.areaBefore}</strong>
              <small>${bundle.impact.label}</small>
            </span>
            <ha-icon icon="mdi:arrow-right"></ha-icon>
          </button>
        </div>
        <div class="meta">
          <span><ha-icon icon="mdi:format-list-checks"></ha-icon>${chores.length} chores · ${duration} min</span>
          <span><ha-icon icon="mdi:heart-pulse"></ha-icon>${impactScope} ${healthGain}</span>
        </div>
        ${this.renderBundleDetails(this.bundle.chores, areaNames)}
      </section>`}
    `;
  }

  renderNoSuggestion() {
    return `
      <section class="suggestion quiet ${this.state.refining ? "refining" : ""}">
        <div class="suggestion-head">
          <div>
            <h2>${NO_SUGGESTION.greeting}</h2>
            <p>${noSuggestionMessage(this.state.context)}</p>
          </div>
        </div>
      </section>
    `;
  }

  renderChip(key) {
    const chip = CHIPS[key];
    const open = this.state.selector === key;
    const options = this.getChipOptions(key);
    const explicit = (key === "time" && this.state.timeExplicit) || (key === "area" && this.state.areaExplicit) || (key === "mood" && this.state.moodExplicit);
    const currentValue = displayContextValue(this.state.context[key]);
    return `
      <div class="chip-wrap">
        <button class="chip ${open ? "open" : ""} ${explicit ? "explicit" : "inferred"}" data-chip="${key}" aria-label="${chip.label}: ${currentValue}" title="${chip.label}">
          <ha-icon icon="${chip.icon}"></ha-icon>
          <strong>${currentValue}</strong>
        </button>
        ${open ? `<div class="selector">${options.map((option) => `
          <button class="${this.state.context[key] === option ? "selected" : ""}" data-chip-key="${key}" data-chip-value="${option}">${displayContextValue(option)}</button>
        `).join("")}</div>` : ""}
      </div>
    `;
  }

  renderBundleDetails(chores, areaNames) {
    const showArea = areaNames.length > 1;
    const removed = new Set(this.state.removed);
    const bonusAvailable = removed.size === 0;
    const includedCount = chores.length - removed.size;
    return `
      <div class="details">
        <div class="keeps-line ${bonusAvailable ? "" : "lost"}">
          <span>${bonusAvailable ? `${this.bundle.bonusKeeps} Keeps for the full reset` : `Full-reset Keeps not active`}</span>
          <span>${includedCount} of ${chores.length} included · ${bonusAvailable ? "The home gives a little back." : "Restore removed Chores to bring the reset back together."}</span>
        </div>
        ${chores.map((chore) => {
          const isRemoved = removed.has(chore.id);
          return `
          <article class="chore-row ${isRemoved ? "removed" : ""}">
            <div class="chore-choice">
              <ha-icon icon="${isRemoved ? "mdi:minus-circle-outline" : "mdi:check-circle-outline"}"></ha-icon>
              <div>
                <strong>${chore.name}</strong>
                <span>${isRemoved ? "Removed" : `${chore.minutes} min · ${chore.keeps} Keeps${showArea ? ` · ${chore.area}` : ""}`}</span>
                <small>${isRemoved ? "This will stay out of the session." : chore.keepLine}</small>
              </div>
            </div>
            <button class="ghost-icon" aria-label="${isRemoved ? `Restore ${chore.name}` : `Remove ${chore.name}`}" title="${isRemoved ? "Restore" : "Remove"}" ${isRemoved ? `data-restore="${chore.id}"` : `data-remove="${chore.id}"`}>
              <ha-icon icon="${isRemoved ? "mdi:undo" : "mdi:close"}"></ha-icon>
            </button>
          </article>
        `;
        }).join("")}
      </div>
    `;
  }

  renderSession() {
    const session = this.state.session;
    const remaining = session.chores.filter((chore) => chore.status === "pending" || chore.status === "ongoing");
    const skipped = session.chores.filter((chore) => chore.status === "skipped");
    const visibleChores = session.chores.filter((chore) => chore.status !== "skipped");
    const allDone = remaining.length === 0;
    const optionalVisible = this.state.optionalOffered && visibleChores.some((chore) => chore.optional);
    const supportText = this.state.optionalOffered
      ? "Stop here, or pick one more small thing."
      : "Start with any Chore. Homekeep will keep the next step clear.";
    return `
      <section class="session-top">
        <p class="eyebrow">Chore Session</p>
        <h1>${this.state.optionalOffered && !allDone ? "That reset helped. A few more fit." : allDone ? "That reset helped." : session.title}</h1>
        ${this.renderSessionProgress()}
        ${this.state.activeItemId ? this.renderTimer() : `<p class="support">${supportText}</p>`}
      </section>
      ${this.state.completionFlash ? `<div class="flash ${this.state.completionFlash.level}">${this.state.completionFlash.keeps} Keeps · ${this.state.completionFlash.message}</div>` : ""}
      <section class="session-list">
        ${visibleChores.map((chore, index) => `${optionalVisible && chore.optional && !visibleChores[index - 1]?.optional ? `${this.renderBundleMilestone()}${this.renderOptionalDivider()}` : ""}${chore.status === "completed" ? this.renderCompletedChore(chore) : this.renderSessionChore(chore, index)}`).join("")}
        ${skipped.length ? this.renderSkippedSummary(skipped) : ""}
        ${this.state.optionalOffered && !allDone ? this.renderSessionExit() : ""}
      </section>
      ${allDone ? this.renderEnding() : ""}
    `;
  }

  renderSessionProgress() {
    const planned = this.state.session.chores.filter((chore) => !chore.optional);
    const optional = this.state.session.chores.filter((chore) => chore.optional);
    const plannedDone = planned.filter((chore) => chore.status === "completed").length;
    const optionalDone = optional.filter((chore) => chore.status === "completed").length;
    const plannedText = `${plannedDone} of ${planned.length} planned done`;
    const optionalText = optional.length ? `${optionalDone} of ${optional.length} optional done` : "planned reset in progress";
    return `<p class="session-progress">${plannedText} · ${optionalText}</p>`;
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
    const skipLabel = chore.optional ? "Not now" : "Skip";
    return `
      <article class="session-chore ${ongoing ? "ongoing" : ""} ${chore.optional ? "optional-chore" : ""}">
        <div>
          ${recommended ? `<span class="next">${chore.optional ? "Optional next" : "Suggested next"}</span>` : chore.optional ? `<span class="next optional">Optional</span>` : ""}
          <h2>${chore.name}</h2>
          <p>${chore.area} · ${chore.minutes} min · ${chore.keeps} Keeps</p>
        </div>
        <div class="row-actions">
          ${ongoing ? `<button class="primary" data-complete="${chore.id}">Complete</button>` : `<button class="secondary" data-start="${chore.id}">Start</button>`}
          <button class="ghost" title="${skipLabel}" aria-label="${skipLabel} ${chore.name}" data-skip="${chore.id}">${skipLabel}</button>
        </div>
      </article>
    `;
  }

  renderCompletedChore(chore) {
    return `
      <article class="session-chore completed-chore ${chore.optional ? "optional-chore" : ""}">
        <div>
          <span class="next done">Nice, done</span>
          <h2>${chore.name}</h2>
          <p>${chore.area} · ${chore.minutes} min · ${chore.keeps} Keeps</p>
        </div>
        <div class="done-badge">
          <ha-icon icon="mdi:check"></ha-icon>
        </div>
      </article>
    `;
  }

  renderOptionalDivider() {
    return `
      <div class="optional-divider">
        <span>A few more that fit</span>
        <small>Picked for small effort, current fit, and useful home lift.</small>
      </div>
    `;
  }

  renderBundleMilestone() {
    return `
      <div class="milestone-row">
        <ha-icon icon="mdi:check-circle-outline"></ha-icon>
        <span>Suggested reset complete</span>
        <small>The home feels lighter.</small>
      </div>
    `;
  }

  renderSessionExit() {
    return `
      <div class="session-exit">
        <span>Stopping here counts.</span>
        <button class="primary" data-action="finish">Back to Right Now</button>
      </div>
    `;
  }

  renderSkippedSummary(skipped) {
    return `
      <section class="completed skipped">
        <span>${skipped.length} skipped</span>
      </section>
    `;
  }

  renderEnding() {
    return `
      <section class="ending">
        <h2>The session is complete.</h2>
        <p>Nice work. The home got a little lighter.</p>
        <div class="actions">
          <button class="primary" data-action="finish">Back to Right Now</button>
        </div>
      </section>
    `;
  }

  renderSummary() {
    const summary = this.state.finalSummary;
    return `
      <section class="summary">
        <p class="eyebrow">Session complete</p>
        <h1>${summary.title} is complete.</h1>
        <p>${summary.chores.map((chore) => chore.name).join(", ")}.</p>
        <div class="impact">${summary.keeps} Keeps · The home feels a little lighter.</div>
      </section>
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
        :host {
          --hk-bg: var(--primary-background-color, #101418);
          --hk-card: color-mix(in srgb, var(--card-background-color, #1b2026) 72%, transparent);
          --hk-card-strong: color-mix(in srgb, var(--card-background-color, #1b2026) 88%, transparent);
          --hk-row: rgba(255, 255, 255, 0.055);
          --hk-row-soft: rgba(255, 255, 255, 0.032);
          --hk-border: color-mix(in srgb, var(--divider-color, #59636d) 42%, transparent);
          --hk-border-soft: color-mix(in srgb, var(--divider-color, #59636d) 24%, transparent);
          --hk-text: var(--primary-text-color, #eef3f1);
          --hk-muted: var(--secondary-text-color, #aab5b0);
          --hk-accent: var(--accent-color, #5dbb9d);
          --hk-accent-soft: color-mix(in srgb, var(--accent-color, #5dbb9d) 18%, transparent);
          --hk-warm: #d6b56d;
          display: block;
          min-height: 100vh;
          color: var(--hk-text);
          background:
            radial-gradient(circle at 50% -15%, rgba(93, 187, 157, 0.12), transparent 36rem),
            var(--hk-bg);
        }
        main { max-width: 860px; margin: 0 auto; padding: clamp(22px, 5vw, 48px) 16px 32px; box-sizing: border-box; }
        button { font: inherit; }
        .hero, .session-top, .summary { text-align: center; padding: 26px 0 18px; }
        .eyebrow { margin: 0 0 10px; color: var(--hk-muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0; font-weight: 700; }
        h1 { margin: 0 auto; max-width: 760px; font-size: clamp(2rem, 6vw, 4rem); line-height: 1.04; font-weight: 760; letter-spacing: 0; }
        h2 { margin: 0; font-size: 1.32rem; line-height: 1.16; letter-spacing: 0; font-weight: 760; }
        p { margin: 0; line-height: 1.48; }
        .chips { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-top: 26px; }
        .chip-wrap { position: relative; }
        .chip, .selector button, .secondary, .ghost, .primary {
          min-height: 40px;
          border-radius: 999px;
          border: 1px solid var(--hk-border-soft);
          background: rgba(255,255,255,0.065);
          color: var(--hk-text);
          padding: 0 13px;
          cursor: pointer;
        }
        .chip { display: flex; align-items: center; gap: 8px; padding-left: 7px; backdrop-filter: blur(16px); }
        .chip.randomize { width: 40px; min-width: 40px; justify-content: center; padding: 0; background: var(--hk-accent-soft); border-color: color-mix(in srgb, var(--hk-accent) 42%, transparent); }
        .chip ha-icon {
          width: 26px;
          height: 26px;
          min-width: 26px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 999px;
          background: rgba(255,255,255,0.085);
          color: var(--hk-accent);
        }
        .chip.randomize ha-icon {
          width: 23px;
          height: 23px;
          min-width: 23px;
          --mdc-icon-size: 18px;
          background: color-mix(in srgb, var(--hk-accent) 24%, transparent);
        }
        .chip strong { font-size: 0.88rem; font-weight: 720; }
        .chip.inferred strong { color: color-mix(in srgb, var(--hk-text) 78%, var(--hk-muted)); }
        .chip.explicit { background: rgba(255,255,255,0.092); border-color: color-mix(in srgb, var(--hk-accent) 46%, transparent); }
        .chip.open { background: color-mix(in srgb, var(--hk-accent) 24%, transparent); border-color: color-mix(in srgb, var(--hk-accent) 58%, transparent); }
        .selector { position: absolute; z-index: 5; top: 48px; left: 0; min-width: 208px; padding: 8px; display: grid; gap: 6px; background: rgba(22, 27, 32, 0.96); border: 1px solid var(--hk-border); box-shadow: 0 18px 45px rgba(0, 0, 0, 0.34); border-radius: 8px; backdrop-filter: blur(18px); }
        .selector button { border-radius: 8px; text-align: left; background: transparent; color: var(--hk-text); line-height: 1.25; padding-block: 8px; }
        .selector .selected { background: var(--hk-accent-soft); border-color: color-mix(in srgb, var(--hk-accent) 42%, transparent); }
        .suggestion, .session-list, .ending { margin-top: 18px; padding: 22px; border: 1px solid var(--hk-border); border-radius: 8px; background: var(--hk-card); box-shadow: 0 22px 70px rgba(0, 0, 0, 0.22); backdrop-filter: blur(22px); }
        .suggestion.refining { filter: blur(0.45px); opacity: 0.82; }
        .suggestion-head { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 14px; align-items: start; }
        .suggestion-head p, .support, .session-progress, .ending p { color: var(--hk-muted); margin-top: 6px; }
        .session-progress { font-size: 0.9rem; font-weight: 720; }
        .fit-line { color: color-mix(in srgb, var(--hk-accent) 72%, var(--hk-muted)); font-size: 0.88rem; font-weight: 680; }
        .icon-button, .ghost-icon { width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--hk-border-soft); display: inline-flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.052); color: var(--hk-text); cursor: pointer; }
        .icon-button.disabled { opacity: 0.55; cursor: default; }
        .meta { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 12px; }
        .meta span, .impact, .keeps-line { display: inline-flex; align-items: center; gap: 6px; min-height: 32px; padding: 0 10px; border-radius: 999px; background: rgba(255,255,255,0.058); border: 1px solid var(--hk-border-soft); color: var(--hk-text); font-size: 0.86rem; font-weight: 700; }
        .meta ha-icon { width: 17px; color: var(--hk-accent); }
        .impact { background: rgba(214, 181, 109, 0.14); color: #edd390; }
        .details { margin-top: 14px; display: grid; gap: 8px; }
        .keeps-line { justify-content: space-between; border-radius: 8px; padding: 9px 11px; width: 100%; box-sizing: border-box; color: #ead7a6; background: rgba(214, 181, 109, 0.105); border-color: rgba(214, 181, 109, 0.22); }
        .keeps-line span:last-child { color: var(--hk-muted); font-weight: 560; }
        .chore-row, .session-chore { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 12px; align-items: center; padding: 12px; border-radius: 8px; background: var(--hk-row); border: 1px solid rgba(255,255,255,0.055); }
        .chore-choice { display: grid; grid-template-columns: 20px minmax(0, 1fr); gap: 10px; align-items: start; }
        .chore-choice ha-icon { width: 18px; margin-top: 1px; color: color-mix(in srgb, var(--hk-accent) 78%, var(--hk-muted)); opacity: 0.72; }
        .chore-row.removed { opacity: 0.72; background: var(--hk-row-soft); border-style: dashed; }
        .chore-row.removed strong { text-decoration: line-through; color: var(--hk-muted); }
        .chore-row.removed .chore-choice ha-icon { color: var(--hk-muted); }
        .keeps-line.lost { background: rgba(214, 181, 109, 0.075); color: #ddc483; border-color: rgba(214, 181, 109, 0.18); }
        .chore-row span, .chore-row small, .session-chore p { display: block; color: var(--hk-muted); margin-top: 4px; line-height: 1.36; }
        .chore-row small { font-size: 0.82rem; }
        .actions, .row-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 16px; }
        .primary { border-color: color-mix(in srgb, var(--hk-accent) 65%, transparent); background: color-mix(in srgb, var(--hk-accent) 72%, #10221e); color: #f7fffb; font-weight: 760; }
        .benefit-action { display: inline-flex; align-items: center; justify-content: space-between; gap: 18px; min-width: 196px; max-width: 248px; margin-left: auto; padding: 8px 12px 8px 16px; text-align: left; box-shadow: 0 10px 26px rgba(0,0,0,0.2); }
        .benefit-action span { display: grid; gap: 1px; }
        .benefit-action small { font-size: 0.78rem; line-height: 1.2; font-weight: 650; opacity: 0.84; }
        .benefit-action ha-icon { width: 19px; color: #f7fffb; }
        .secondary { background: rgba(255,255,255,0.075); font-weight: 720; }
        .ghost { min-width: 40px; padding: 0 12px; background: transparent; color: var(--hk-muted); }
        .session-list { display: grid; gap: 10px; }
        .session-chore.ongoing { outline: 2px solid color-mix(in srgb, var(--hk-accent) 62%, transparent); background: color-mix(in srgb, var(--hk-accent) 13%, transparent); }
        .optional-chore { background: rgba(255,255,255,0.04); border-style: dashed; }
        .milestone-row { display: grid; grid-template-columns: auto minmax(0, 1fr) auto; gap: 8px; align-items: center; padding: 10px 12px; border-radius: 8px; color: #dff5e8; background: color-mix(in srgb, var(--hk-accent) 13%, transparent); border: 1px solid color-mix(in srgb, var(--hk-accent) 28%, transparent); }
        .milestone-row ha-icon { width: 18px; color: var(--hk-accent); }
        .milestone-row span { font-weight: 780; }
        .milestone-row small { color: var(--hk-muted); }
        .optional-divider { display: grid; gap: 3px; margin: 8px 0 0; padding: 8px 2px 2px; color: var(--hk-text); }
        .optional-divider span { font-size: 0.9rem; font-weight: 780; }
        .optional-divider small { color: var(--hk-muted); line-height: 1.35; }
        .next { display: inline-block; margin-bottom: 6px; color: var(--hk-accent); font-weight: 740; font-size: 0.8rem; }
        .next.optional { color: var(--hk-muted); }
        .timer { display: inline-flex; align-items: center; gap: 12px; margin-top: 16px; padding: 8px 8px 8px 18px; border-radius: 999px; background: var(--hk-card-strong); border: 1px solid var(--hk-border-soft); box-shadow: 0 10px 28px rgba(0, 0, 0, 0.24); }
        .timer span { font-size: 1.45rem; line-height: 1; font-variant-numeric: tabular-nums; font-weight: 800; }
        .flash { position: sticky; top: 12px; z-index: 3; margin: 0 auto 12px; width: fit-content; padding: 10px 16px; border-radius: 999px; color: #f5fff9; background: color-mix(in srgb, var(--hk-accent) 52%, #163028); font-weight: 800; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.26); }
        .flash.bundle { padding-inline: 18px; background: color-mix(in srgb, var(--hk-accent) 68%, #18372d); box-shadow: 0 16px 38px rgba(0, 0, 0, 0.32); }
        .flash.optional { background: color-mix(in srgb, #d6b56d 30%, var(--hk-accent) 42%); }
        .flash.optional-2 { background: color-mix(in srgb, #d6b56d 42%, var(--hk-accent) 48%); box-shadow: 0 14px 34px rgba(0, 0, 0, 0.3); }
        .flash.optional-3 { padding-inline: 18px; background: color-mix(in srgb, #d6b56d 52%, var(--hk-accent) 50%); box-shadow: 0 16px 40px rgba(0, 0, 0, 0.34); }
        .completed-chore { background: color-mix(in srgb, var(--hk-accent) 10%, var(--hk-row)); border-color: color-mix(in srgb, var(--hk-accent) 34%, transparent); }
        .completed-chore h2 { color: color-mix(in srgb, var(--hk-text) 86%, var(--hk-accent)); }
        .done { color: #cfe9d9; }
        .done-badge { width: 38px; height: 38px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; color: #f5fff9; background: color-mix(in srgb, var(--hk-accent) 48%, #172d25); border: 1px solid color-mix(in srgb, var(--hk-accent) 56%, transparent); }
        .skipped { color: var(--hk-muted); }
        .session-exit { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 4px; padding: 12px; border-radius: 8px; background: rgba(255,255,255,0.045); border: 1px solid var(--hk-border-soft); }
        .session-exit span { color: var(--hk-muted); font-weight: 680; }
        .ending { text-align: center; }
        .ending .actions { justify-content: center; }
        .summary { min-height: 70vh; display: grid; align-content: center; justify-items: center; gap: 14px; }
        @media (max-width: 620px) {
          main { padding-left: 12px; padding-right: 12px; }
          .hero, .session-top, .summary { padding-top: 18px; }
          h1 { font-size: clamp(1.85rem, 9vw, 2.7rem); }
          .chips { margin-top: 18px; gap: 6px; }
          .suggestion, .session-list, .ending { margin-top: 14px; padding: 14px; }
          .suggestion-head { grid-template-columns: 1fr; }
          .meta { margin: 12px 0 10px; }
          .details { margin-top: 10px; gap: 6px; }
          .keeps-line { align-items: flex-start; gap: 4px; padding: 8px 10px; }
          .chore-row, .session-chore { grid-template-columns: 1fr; }
          .chore-row { padding: 10px; }
          .row-actions { display: grid; grid-template-columns: 1fr 1fr; }
          .milestone-row { grid-template-columns: auto minmax(0, 1fr); }
          .milestone-row small { grid-column: 2; }
          .session-exit { align-items: stretch; flex-direction: column; }
          .actions { justify-content: stretch; }
          .primary, .secondary, .ghost { width: 100%; }
          .benefit-action { width: 100%; max-width: none; margin-left: 0; }
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
    if (target.dataset.chipKey && target.dataset.chipValue) {
      this.chooseChip(target.dataset.chipKey, target.dataset.chipValue);
      return;
    }
    if (target.dataset.remove) this.removeChore(target.dataset.remove);
    if (target.dataset.restore) this.restoreChore(target.dataset.restore);
    if (target.dataset.start) this.startChore(target.dataset.start);
    if (target.dataset.complete) this.completeChore(target.dataset.complete);
    if (target.dataset.skip) this.skipChore(target.dataset.skip);
    if (action === "start-session") this.startSession();
    if (action === "shuffle") this.shuffle();
    if (action === "toggle-pause") {
      this.state.paused = !this.state.paused;
      this.render();
    }
    if (action === "finish") this.finishSession();
  }
}

customElements.define("homekeep-panel", HomekeepPanel);

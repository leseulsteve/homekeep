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
    title: "Kitchen Lift",
    duration: 15,
    context: { time: "15 min", capacity: "steady", mood: "focused", goal: "visible lift", area: "Kitchen" },
    reason: "The kitchen has the clearest lift for a short focused pass.",
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
      { id: "reset-bathroom-sink", name: "Clear bathroom sink", area: "Bathroom", minutes: 6, keeps: 7, keepLine: "brings the sink back to easy use" },
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
    title: "Evening Lift",
    duration: 5,
    context: { time: "5 min", capacity: "low", mood: "auto", goal: "quick wins", area: "Auto" },
    reason: "A tiny mixed-area pass keeps the evening gentle.",
    greeting: "Five gentle minutes can still help the home feel cared for.",
    impact: { label: "Small home lift", home: 3, areaName: "Home", areaBefore: 74, areaAfter: 77 },
    bonusKeeps: 2,
    chores: [
      { id: "clear-coffee-table", name: "Clear coffee table", area: "Living room", minutes: 3, keeps: 4, keepLine: "opens the room back up" },
      { id: "gather-stray-cups", name: "Gather stray cups", area: "Kitchen", minutes: 2, keeps: 3, keepLine: "prevents a small morning pileup" },
    ],
  },
];

const HOME_HEALTH = {
  label: "Home Care",
  trend: "Care moved through the home this week",
  status: "Steady with a few useful places to help",
  note: "The home is mostly steady, and it still has a little agenda. Kitchen and Laundry are the places asking loudest for care.",
  stats: [
    { icon: "mdi:home-outline", label: "4 areas watched" },
    { icon: "mdi:check-circle-outline", label: "8 helped lately" },
    { icon: "mdi:alert-circle-outline", label: "2 asking now" },
  ],
  areas: [
    {
      name: "Kitchen",
      status: "Could use care",
      trend: "Could use care",
      helped: ["Dishes stayed moving", "Counters were reset recently"],
      next: "A short counter and compost pass would help most.",
      lift: "Big lift available",
    },
    {
      name: "Bathroom",
      status: "Starting to build up",
      trend: "Steady, drifting down",
      helped: ["Fresh towel helped", "Sink stayed usable"],
      next: "A quiet sink refresh keeps this area easy.",
      lift: "Useful lift available",
    },
    {
      name: "Entryway",
      status: "Starting to build up",
      trend: "Visible lift available",
      helped: ["Shoes were straightened", "Landing shelf stayed lighter"],
      next: "The rug and shelf are the best small lift.",
      lift: "Visible lift available",
    },
    {
      name: "Laundry",
      status: "Could use care",
      trend: "Overdue care",
      helped: ["Washer cycle carried some care", "Dry towels are ready to fold"],
      next: "Starting a small load gives this area momentum.",
      lift: "Big lift available",
    },
  ],
};

const QUICK_AREA_TASKS = [
  {
    id: "quick-kitchen-counter",
    name: "Wipe one counter",
    area: "Kitchen",
    minutes: 5,
    keeps: 6,
    keepLine: "gives the kitchen a small clear place to land",
    impact: { label: "Quick kitchen help", home: 2, areaName: "Kitchen", areaBefore: 48, areaAfter: 56 },
  },
  {
    id: "quick-bathroom-sink",
    name: "Clear the bathroom sink",
    area: "Bathroom",
    minutes: 5,
    keeps: 6,
    keepLine: "keeps the sink easy to use",
    impact: { label: "Quick bathroom help", home: 2, areaName: "Bathroom", areaBefore: 57, areaAfter: 64 },
  },
  {
    id: "quick-entry-shelf",
    name: "Clear the entry shelf",
    area: "Entryway",
    minutes: 5,
    keeps: 6,
    keepLine: "makes the first landing spot easier",
    impact: { label: "Quick entryway help", home: 2, areaName: "Entryway", areaBefore: 52, areaAfter: 60 },
  },
  {
    id: "quick-laundry-lint",
    name: "Empty dryer lint",
    area: "Laundry",
    minutes: 2,
    keeps: 3,
    keepLine: "keeps the next load easier to start",
    impact: { label: "Quick laundry help", home: 1, areaName: "Laundry", areaBefore: 43, areaAfter: 49 },
  },
];

const WHILE_THERE_CANDIDATES = [
  {
    id: "wipe-stove-front",
    name: "Wipe stove front",
    area: "Kitchen",
    minutes: 3,
    keeps: 4,
    keepLine: "uses the same kitchen pass while you are there",
    healthImpact: 8,
    staleness: 6,
    fits: ["focused", "ready", "auto"],
    contexts: ["same-area", "same-setup"],
  },
  {
    id: "straighten-entry-shoes",
    name: "Straighten entry shoes",
    area: "Entryway",
    minutes: 2,
    keeps: 3,
    keepLine: "fits the same doorway moment",
    healthImpact: 6,
    staleness: 5,
    fits: ["low", "restless", "auto"],
    contexts: ["same-area", "same-route"],
  },
  {
    id: "wipe-bathroom-mirror",
    name: "Wipe bathroom mirror",
    area: "Bathroom",
    minutes: 3,
    keeps: 4,
    keepLine: "adds one small finish while you are there",
    healthImpact: 7,
    staleness: 4,
    fits: ["quiet", "focused", "auto"],
    contexts: ["same-area", "same-setup"],
  },
  {
    id: "empty-dryer-lint",
    name: "Empty dryer lint",
    area: "Laundry",
    minutes: 2,
    keeps: 3,
    keepLine: "fits naturally beside the laundry pass",
    healthImpact: 6,
    staleness: 6,
    fits: ["low", "focused", "ready"],
    contexts: ["same-area", "same-device"],
  },
  {
    id: "fold-living-room-blanket",
    name: "Fold living room blanket",
    area: "Living room",
    minutes: 2,
    keeps: 3,
    keepLine: "settles the same room while you are there",
    healthImpact: 5,
    staleness: 4,
    fits: ["low", "quiet", "auto"],
    contexts: ["same-area"],
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
  {
    id: "vacuum-entry-path",
    name: "Vacuum the entry path",
    area: "Entryway",
    minutes: 9,
    keeps: 8,
    keepLine: "uses the momentum from the visible entryway lift",
    healthImpact: 10,
    staleness: 8,
    fits: ["focused", "restless", "ready"],
    momentum: true,
  },
  {
    id: "fold-small-laundry-basket",
    name: "Fold a small laundry basket",
    area: "Laundry",
    minutes: 12,
    keeps: 10,
    keepLine: "turns the laundry momentum into a fuller finish",
    healthImpact: 11,
    staleness: 9,
    fits: ["focused", "ready"],
    momentum: true,
  },
];

const GREETINGS_BY_CONTEXT = {
  morning: [
    "Good morning.",
    "Morning check-in.",
  ],
  afternoon: [
    "Good afternoon.",
    "There is room this afternoon.",
  ],
  evening: [
    "Good evening.",
    "Evening can stay gentle.",
  ],
  night: [
    "Late day, lighter touch.",
    "Tonight can stay quiet.",
  ],
  low: [
    "Something small and gentle can still help.",
    "Let's keep this light.",
  ],
  quiet: [
    "A quiet bit of care can fit here.",
    "There is a calm way to help.",
  ],
  focused: [
    "There is room for one useful pass.",
    "A clear task bundle can move things forward.",
  ],
  high: [
    "There is room for one useful pass.",
    "A clear task bundle can move things forward.",
  ],
  restless: [
    "A visible lift can use that extra motion.",
    "A small task bundle has some movement in it.",
  ],
  ready: [
    "The home has a fuller bundle ready if you want to lean in.",
    "There is room to push a little where it matters.",
  ],
  short: [
    "A few minutes can still make the home feel lighter.",
    "Something small can still help.",
  ],
  default: [
    "I found something small that can make the home feel lighter.",
    "The home has a useful place to start.",
  ],
};

const GREETING_AREAS = {
  Auto: [
    "I found a useful place to start.",
    "The home has a useful place to start.",
  ],
  Kitchen: [
    "The kitchen has a clear lift ready.",
    "A kitchen pass would help right now.",
  ],
  Entryway: [
    "The entryway has a visible lift ready.",
    "A small entryway reset would help.",
  ],
  Bathroom: [
    "The bathroom has a contained refresh ready.",
    "A quiet bathroom pass would help.",
  ],
  Laundry: [
    "Laundry has momentum waiting.",
    "A laundry pass would move things along.",
  ],
  "Living room": [
    "The living room can open back up.",
    "A living room reset would help.",
  ],
};

const GREETING_TIMES = {
  [TIME_AUTO]: [
    "I matched it to this moment.",
    "It can fit this moment.",
  ],
  "5 min": [
    "Five minutes is enough.",
    "This can stay tiny.",
  ],
  "10 min": [
    "Ten minutes can make a dent.",
    "This can stay compact.",
  ],
  "15 min": [
    "A short pass can move things.",
    "There is room for a steady pass.",
  ],
  "25 min": [
    "There is room for a fuller pass.",
    "A fuller pass can help where it matters.",
  ],
};

function pickFrom(list) {
  return list[Math.floor(Math.random() * list.length)];
}

function currentDayPart(date = new Date()) {
  const hour = date.getHours();
  if (hour >= 5 && hour < 12) return "morning";
  if (hour >= 12 && hour < 17) return "afternoon";
  if (hour >= 17 && hour < 22) return "evening";
  return "night";
}

function pickRightNowGreeting(context, date = new Date()) {
  const dayPart = currentDayPart(date);
  const timeCandidates = GREETING_TIMES[context.time] || GREETING_TIMES[TIME_AUTO];
  if (context.time === "5 min") {
    return `${pickFrom(GREETINGS_BY_CONTEXT[dayPart])} ${pickFrom(GREETINGS_BY_CONTEXT.short)}`;
  }
  if (context.area !== "Auto") {
    const areaCandidates = GREETING_AREAS[context.area] || GREETING_AREAS.Auto;
    return `${pickFrom(GREETINGS_BY_CONTEXT[dayPart])} ${pickFrom([...areaCandidates, ...timeCandidates])}`;
  }
  const candidates = GREETINGS_BY_CONTEXT[context.mood] || GREETINGS_BY_CONTEXT.default;
  return `${pickFrom(GREETINGS_BY_CONTEXT[dayPart])} ${pickFrom([...candidates, ...timeCandidates])}`;
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

function scoreWhileThereTask(candidate, context, bundle, coreIds, bundleAreas, rejectedIds, removedIds) {
  if (coreIds.has(candidate.id)) return -Infinity;
  if (rejectedIds.has(candidate.id) && !removedIds.has(candidate.id)) return -Infinity;
  if (!bundleAreas.has(candidate.area)) return -Infinity;
  if (candidate.minutes > 5) return -Infinity;
  if (["low", "quiet"].includes(context.mood) && candidate.minutes > 3) return -Infinity;
  let score = candidate.healthImpact + candidate.staleness;
  if (candidate.minutes <= 2) score += 4;
  else if (candidate.minutes <= 4) score += 2;
  if (candidate.fits.includes(context.mood) || candidate.fits.includes("auto")) score += 4;
  if (candidate.area === bundle.impact.areaName) score += 4;
  if (context.area !== "Auto" && candidate.area === context.area) score += 3;
  if (candidate.contexts.includes("same-device") && bundle.context.goal === "overdue care") score += 3;
  if (candidate.contexts.includes("same-setup") && ["focused", "ready"].includes(context.mood)) score += 2;
  return score;
}

function pickWhileThereTask(bundle, context, rejectedIds = new Set(), removedIds = new Set()) {
  const coreIds = new Set(bundle.chores.map((chore) => chore.id));
  const bundleAreas = new Set(bundle.chores.map((chore) => chore.area));
  const best = WHILE_THERE_CANDIDATES
    .map((candidate) => ({ candidate, score: scoreWhileThereTask(candidate, context, bundle, coreIds, bundleAreas, rejectedIds, removedIds) }))
    .filter((entry) => Number.isFinite(entry.score))
    .sort((a, b) => b.score - a.score || a.candidate.minutes - b.candidate.minutes || a.candidate.name.localeCompare(b.candidate.name))[0];
  if (!best) return null;
  const { healthImpact, staleness, fits, contexts, ...task } = best.candidate;
  return { ...task, whileThere: true };
}

function displayContextValue(value) {
  return value === "Auto" ? "Best fit" : value;
}

function contextFitLine(context, bundle, duration, areaNames, areaExplicit) {
  if (areaExplicit && context.area !== "Auto") return `Kept to ${context.area} because you picked it.`;
  const moodText = context.mood === "auto" ? "balanced" : context.mood;
  const timeText = context.time === TIME_AUTO ? `${duration}-minute` : context.time.replace(" min", "-minute");
  const areaText = context.area !== "Auto" ? context.area : areaNames.length === 1 ? areaNames[0] : "the home";
  return `Picked for a ${moodText} ${timeText} task bundle in ${areaText}.`;
}

function noSuggestionMessage(context) {
  if (context.area !== "Auto") return `Nothing fits ${context.area} with this mood right now.`;
  return NO_SUGGESTION.message;
}

function scoreOptionalChore(candidate, context, sessionArea) {
  let score = candidate.healthImpact + candidate.staleness;
  if (candidate.minutes <= 3) score += 4;
  else if (candidate.minutes <= 5) score += 2;
  else if (candidate.momentum && ["focused", "restless", "ready"].includes(context.mood)) score += 3;
  if (["low", "quiet"].includes(context.mood) && candidate.minutes <= 4) score += 4;
  if (["focused", "ready"].includes(context.mood) && candidate.healthImpact >= 7) score += 3;
  if (context.mood === "restless" && candidate.area !== sessionArea) score += 2;
  if (candidate.fits.includes(context.mood) || candidate.fits.includes("auto")) score += 3;
  if (context.area !== "Auto" && candidate.area === context.area) score += 4;
  if (context.area === "Auto" && candidate.area === sessionArea) score += 2;
  return score;
}

function momentumEligible(context) {
  return ["focused", "restless", "ready"].includes(context.mood) || context.capacity === "strong" || context.capacity === "mobile";
}

function publicOptionalChore(candidate) {
  const { healthImpact, staleness, fits, ...chore } = candidate;
  return chore;
}

function quickAreaTaskFor(areaName) {
  return QUICK_AREA_TASKS.find((task) => task.area === areaName) || null;
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
      rejectedWhileThere: [],
      session: null,
      activeItemId: null,
      paused: false,
      elapsed: 0,
      optionalOffered: false,
      finalSummary: null,
      completionFlash: null,
      activeTab: "right-now",
      quickAreaTask: null,
      greetingDayPart: currentDayPart(),
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
    this.dayPartTimer = window.setInterval(() => this.refreshGreetingForDayPart(), 60000);
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
    window.clearInterval(this.dayPartTimer);
    window.clearTimeout(this.refineTimer);
    window.clearTimeout(this.summaryTimer);
  }

  set hass(value) {
    this._hass = value;
  }

  get bundle() {
    if (this.state.quickAreaTask) {
      const task = this.state.quickAreaTask;
      return {
        id: `quick-${task.area.toLowerCase().replaceAll(" ", "-")}`,
        title: `${task.area} Short Help`,
        duration: task.minutes,
        context: {
          ...this.state.context,
          time: `${task.minutes} min`,
          capacity: "low",
          goal: "quick wins",
          area: task.area,
        },
        reason: `Home Health asked for short help in ${task.area}.`,
        greeting: `${task.area} is asking for one short bit of help.`,
        impact: task.impact,
        bonusKeeps: 0,
        chores: [task],
      };
    }
    const bundle = BUNDLES[this.state.selected];
    const whileThereTask = pickWhileThereTask(bundle, this.state.context, new Set(this.state.rejectedWhileThere), new Set(this.state.removed));
    return whileThereTask ? { ...bundle, chores: [...bundle.chores, whileThereTask] } : bundle;
  }

  getChipOptions(key) {
    const options = key === "time" ? timeOptionsForContext(this.state.context) : CHIPS[key].options;
    if (key === "time" && !options.includes(this.state.context.time)) {
      return [this.state.context.time, ...options];
    }
    return options;
  }

  nextRightNowGreeting(context = this.state.context) {
    let greeting = pickRightNowGreeting(context);
    for (let attempt = 0; attempt < 4 && greeting === this.state.rightNowGreeting; attempt += 1) {
      greeting = pickRightNowGreeting(context);
    }
    return greeting;
  }

  refreshRightNowGreeting(context = this.state.context) {
    this.state.rightNowGreeting = this.nextRightNowGreeting(context);
    this.state.greetingDayPart = currentDayPart();
  }

  refreshGreetingForDayPart() {
    const dayPart = currentDayPart();
    if (dayPart === this.state.greetingDayPart) return;
    this.state.greetingDayPart = dayPart;
    if (this.state.view === "ready" && this.state.activeTab === "right-now") {
      this.refreshRightNowGreeting();
      this.render();
    }
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
      quickAreaTask: null,
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
    const rightNowGreeting = this.nextRightNowGreeting(context);
    this.refine({
      context,
      areaExplicit,
      timeExplicit,
      moodExplicit,
      selected,
      quickAreaTask: null,
      rightNowGreeting,
      greetingDayPart: currentDayPart(),
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
    const removedChore = this.bundle.chores.find((chore) => chore.id === choreId);
    this.state.removed = [...this.state.removed, choreId];
    if (removedChore?.whileThere && !this.state.rejectedWhileThere.includes(choreId)) {
      this.state.rejectedWhileThere = [...this.state.rejectedWhileThere, choreId];
    }
    this.render();
  }

  restoreChore(choreId) {
    this.state.removed = this.state.removed.filter((id) => id !== choreId);
    this.state.rejectedWhileThere = this.state.rejectedWhileThere.filter((id) => id !== choreId);
    this.render();
  }

  requestAreaHelp(areaName, mode = "short") {
    const shortHelp = mode === "short";
    const quickAreaTask = shortHelp ? quickAreaTaskFor(areaName) : null;
    if (shortHelp && !quickAreaTask) return;
    const context = {
      ...this.state.context,
      time: shortHelp ? "5 min" : TIME_AUTO,
      area: areaName,
      mood: shortHelp ? this.state.context.mood : "ready",
      capacity: shortHelp ? "low" : "strong",
      goal: shortHelp ? "quick wins" : "overdue care",
    };
    const selected = this.pickBundle(context);
    this.refine({
      activeTab: "right-now",
      context,
      selected,
      quickAreaTask,
      areaExplicit: true,
      timeExplicit: shortHelp,
      moodExplicit: !shortHelp,
      expanded: true,
      removed: [],
      noSuggestion: false,
      rightNowGreeting: shortHelp
        ? `${areaName} is asking for one short bit of help.`
        : `${areaName} could use a little more care. Right Now found a gentle pass.`,
      greetingDayPart: currentDayPart(),
    });
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
        message: "Suggested bundle complete. The home feels lighter.",
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
    const allowMomentum = momentumEligible(this.state.context);
    const optionalChores = OPTIONAL_CHORE_CANDIDATES
      .filter((chore) => !excluded.has(chore.id) && (chore.minutes <= 5 || (allowMomentum && chore.momentum && chore.minutes <= 12)))
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
  }

  resetReady() {
    this.state.view = "ready";
    this.state.session = null;
    this.state.finalSummary = null;
    this.state.expanded = false;
    this.state.removed = [];
    this.state.quickAreaTask = null;
    this.refreshRightNowGreeting();
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `${this.styles()}<main>${this.renderMain()}</main>`;
  }

  renderMain() {
    if (this.state.view === "session") return this.renderSession();
    if (this.state.view === "summary") return this.renderSummary();
    if (this.state.activeTab === "home-health") return `${this.renderTabs()}${this.renderHomeHealth()}`;
    return `${this.renderTabs()}${this.renderReady()}`;
  }

  renderTabs() {
    const tabs = [
      { id: "right-now", label: "Right Now", icon: "mdi:home-heart" },
      { id: "home-health", label: "Home Care", icon: "mdi:home-outline" },
    ];
    return `
      <nav class="tabs" aria-label="Homekeep sections">
        ${tabs.map((tab) => `
          <button class="${this.state.activeTab === tab.id ? "active" : ""}" data-tab="${tab.id}" aria-current="${this.state.activeTab === tab.id ? "page" : "false"}">
            <ha-icon icon="${tab.icon}"></ha-icon>
            <span>${tab.label}</span>
          </button>
        `).join("")}
      </nav>
    `;
  }

  renderHomeHealth() {
    return `
      <section class="health-hero">
        <div class="health-status">
          <span>${HOME_HEALTH.label}</span>
          <small>${HOME_HEALTH.trend}</small>
        </div>
        <div>
          <p class="eyebrow">Visual test</p>
          <h1>${HOME_HEALTH.status}</h1>
          <p class="support">${HOME_HEALTH.note}</p>
          <div class="meta health-stats" aria-label="Home care stats">
            ${HOME_HEALTH.stats.map((stat) => `<span class="meta-chip icon-chip"><ha-icon icon="${stat.icon}"></ha-icon><strong>${stat.label}</strong></span>`).join("")}
          </div>
        </div>
      </section>
      <section class="health-list" aria-label="Area care">
        ${HOME_HEALTH.areas.map((area) => this.renderAreaHealth(area)).join("")}
      </section>
    `;
  }

  renderAreaHealth(area) {
    return `
      <article class="area-card">
        <div class="area-head">
          <div>
            <h2>${area.name}</h2>
            <p>${area.status} · ${area.trend}</p>
          </div>
        </div>
        <div class="area-columns">
          <div>
            <span class="area-kicker">Helped lately</span>
            <div class="area-chip-row helped">
              ${area.helped.map((item) => `<span class="meta-chip icon-chip soft"><ha-icon icon="mdi:sparkles"></ha-icon><strong>${item}</strong></span>`).join("")}
            </div>
          </div>
          <div>
            <span class="area-kicker">Could help next</span>
            <p>${area.next}</p>
            <div class="area-actions" aria-label="${area.name} help options">
              <button class="secondary area-help" data-action="area-help" data-help-mode="short" data-area="${area.name}" aria-label="Ask for short help in ${area.name}">
                <ha-icon icon="mdi:timer-sand"></ha-icon>
                <span>Short help</span>
              </button>
              <button class="secondary area-help nudge" data-action="area-help" data-help-mode="care" data-area="${area.name}" aria-label="Ask Right Now for a care nudge in ${area.name}">
                <ha-icon icon="mdi:hand-heart"></ha-icon>
                <span>Care nudge</span>
              </button>
            </div>
          </div>
        </div>
      </article>
    `;
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
          <button class="primary benefit-action" data-action="start-session" aria-label="Start this bundle">
            <span>Start</span>
            <ha-icon icon="mdi:arrow-right"></ha-icon>
          </button>
        </div>
        <div class="meta">
          <span class="meta-chip icon-chip"><ha-icon icon="mdi:format-list-checks"></ha-icon><strong>${chores.length} tasks · ${duration} min</strong></span>
          <span class="meta-chip icon-chip"><ha-icon icon="mdi:home-outline"></ha-icon><strong>${impactScope} ${healthGain}</strong></span>
          <span class="meta-chip icon-chip"><ha-icon icon="mdi:target"></ha-icon><strong>${bundle.context.goal}</strong></span>
          ${bundle.bonusKeeps ? `<span class="meta-chip icon-chip warm"><ha-icon icon="mdi:sparkles"></ha-icon><strong>+${bundle.bonusKeeps} Keeps</strong></span>` : ""}
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
        <button class="chip icon-chip ${open ? "open" : ""} ${explicit ? "explicit" : "inferred"}" data-chip="${key}" aria-label="${chip.label}: ${currentValue}" title="${chip.label}">
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
    const coreRemoved = chores.some((chore) => !chore.whileThere && removed.has(chore.id));
    const bonusAvailable = !coreRemoved;
    const includedCount = chores.length - removed.size;
    return `
      <div class="details">
        <div class="keeps-line ${bonusAvailable ? "" : "lost"}">
          <span>${bonusAvailable ? `${this.bundle.bonusKeeps} bundle Keeps` : `Bundle Keeps not active`}</span>
          <span>${includedCount} of ${chores.length} included · ${bonusAvailable ? "The home gives a little back." : "Restore core Tasks to bring the bundle back together."}</span>
        </div>
        ${chores.map((chore) => {
          const isRemoved = removed.has(chore.id);
          return `
          <article class="chore-row ${isRemoved ? "removed" : ""} ${chore.whileThere ? "while-there" : ""}">
            <div class="chore-choice">
              <ha-icon icon="${isRemoved ? "mdi:minus-circle-outline" : chore.whileThere ? "mdi:map-marker-check-outline" : "mdi:check-circle-outline"}"></ha-icon>
              <div>
                ${chore.whileThere ? `<span class="row-kicker">While you're there</span>` : ""}
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
    const activeChores = visibleChores.filter((chore) => chore.status !== "completed");
    const completedChores = visibleChores.filter((chore) => chore.status === "completed");
    const orderedChores = [...activeChores, ...completedChores];
    const allDone = remaining.length === 0;
    const optionalVisible = this.state.optionalOffered && activeChores.some((chore) => chore.optional);
    const supportText = this.state.optionalOffered
      ? "Stop here, or pick one more small thing."
      : "Start with any Task. Homekeep will keep the next step clear.";
    return `
      <section class="session-top">
        <p class="eyebrow">Task Session</p>
        <h1>${this.state.optionalOffered && !allDone ? "That bundle helped. A few more fit." : allDone ? "That bundle helped." : session.title}</h1>
        ${this.renderSessionProgress()}
        <div class="session-live-slot">
          ${this.renderSessionTopAction(allDone, supportText)}
        </div>
        <div class="flash-slot">
          ${this.state.completionFlash ? `<div class="flash ${this.state.completionFlash.level}">${this.state.completionFlash.keeps} Keeps · ${this.state.completionFlash.message}</div>` : ""}
        </div>
      </section>
      <section class="session-list">
        ${orderedChores.map((chore, index) => `${optionalVisible && chore.optional && !orderedChores[index - 1]?.optional ? `${this.renderBundleMilestone()}${this.renderOptionalDivider()}` : ""}${chore.status === "completed" ? this.renderCompletedChore(chore) : this.renderSessionChore(chore, index)}`).join("")}
        ${skipped.length ? this.renderSkippedSummary(skipped) : ""}
      </section>
    `;
  }

  renderSessionTopAction(allDone, supportText) {
    if (allDone) {
      return `
        <div class="session-top-action">
          <span>The session is complete.</span>
          <button class="primary" data-action="finish">Back to Right Now</button>
        </div>
      `;
    }
    if (this.state.activeItemId) return this.renderTimer();
    if (this.state.optionalOffered) {
      return `
        <div class="session-top-action">
          <span>${supportText}</span>
          <button class="primary" data-action="finish">Done for now</button>
        </div>
      `;
    }
    return `<p class="support">${supportText}</p>`;
  }

  renderSessionProgress() {
    const planned = this.state.session.chores.filter((chore) => !chore.optional);
    const optional = this.state.session.chores.filter((chore) => chore.optional);
    const plannedDone = planned.filter((chore) => chore.status === "completed").length;
    const optionalDone = optional.filter((chore) => chore.status === "completed").length;
    const plannedText = `${plannedDone} of ${planned.length} planned done`;
    const optionalText = optional.length ? `${optionalDone} of ${optional.length} optional done` : "planned bundle in progress";
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
    const hasMomentumTask = this.state.session?.chores.some((chore) => chore.optional && chore.momentum);
    return `
      <div class="optional-divider">
        <span>${hasMomentumTask ? "Momentum fits one bigger task" : "A few more that fit"}</span>
        <small>${hasMomentumTask ? "The bundle is done. This is only here if you want to use the momentum." : "Picked for small effort, current fit, and useful home lift."}</small>
      </div>
    `;
  }

  renderBundleMilestone() {
    return `
      <div class="milestone-row">
        <ha-icon icon="mdi:check-circle-outline"></ha-icon>
        <span>Suggested bundle complete</span>
        <small>The home feels lighter.</small>
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

  renderSummary() {
    const summary = this.state.finalSummary;
    return `
      <section class="summary">
        <p class="eyebrow">Session complete</p>
        <h1>${summary.title} is complete.</h1>
        <p>${summary.chores.map((chore) => chore.name).join(", ")}.</p>
        <div class="impact">${summary.keeps} Keeps · The home feels a little lighter.</div>
        <button class="primary" data-action="dismiss-summary">Dismiss</button>
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
        .tabs { display: flex; justify-content: center; gap: 8px; margin: 0 auto 18px; padding: 4px; width: fit-content; max-width: 100%; border-radius: 999px; background: rgba(255,255,255,0.048); border: 1px solid var(--hk-border-soft); }
        .tabs button { min-height: 38px; display: inline-flex; align-items: center; gap: 7px; border: 0; border-radius: 999px; padding: 0 13px; color: var(--hk-muted); background: transparent; cursor: pointer; font: inherit; font-weight: 760; }
        .tabs button.active { color: var(--hk-text); background: var(--hk-accent-soft); box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--hk-accent) 30%, transparent); }
        .tabs ha-icon { width: 18px; --mdc-icon-size: 18px; color: var(--hk-accent); }
        .eyebrow { margin: 0 0 10px; color: var(--hk-muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0; font-weight: 700; }
        h1 { margin: 0 auto; max-width: 760px; font-size: clamp(2rem, 6vw, 4rem); line-height: 1.04; font-weight: 760; letter-spacing: 0; }
        .hero h1 { height: 2.08em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; text-wrap: balance; }
        .session-top h1 { min-height: 2.08em; display: flex; align-items: center; justify-content: center; text-wrap: balance; }
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
        .chip { display: flex; align-items: center; backdrop-filter: blur(16px); }
        .icon-chip { gap: 0; padding: 0; overflow: hidden; --hk-chip-icon-width: 40px; }
        .chip.randomize { width: 40px; min-width: 40px; justify-content: center; padding: 0; background: var(--hk-accent-soft); border-color: color-mix(in srgb, var(--hk-accent) 42%, transparent); }
        .icon-chip ha-icon {
          align-self: stretch;
          width: var(--hk-chip-icon-width);
          min-width: var(--hk-chip-icon-width);
          display: inline-flex;
          align-items: center;
          justify-content: center;
          background: rgba(255,255,255,0.1);
          color: var(--hk-accent);
        }
        .chip.icon-chip.explicit ha-icon { background: color-mix(in srgb, var(--hk-accent) 16%, rgba(255,255,255,0.08)); }
        .chip.icon-chip.open ha-icon {
          background: color-mix(in srgb, var(--hk-accent) 28%, rgba(255,255,255,0.08));
        }
        .chip.randomize ha-icon {
          width: 23px;
          height: 23px;
          min-width: 23px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 999px;
          --mdc-icon-size: 18px;
          color: var(--hk-accent);
        }
        .chip strong { font-size: 0.88rem; font-weight: 720; padding: 0 13px 0 10px; }
        .chip.inferred strong { color: color-mix(in srgb, var(--hk-text) 78%, var(--hk-muted)); }
        .chip.explicit { background: rgba(255,255,255,0.092); border-color: color-mix(in srgb, var(--hk-accent) 46%, transparent); }
        .chip.open { background: color-mix(in srgb, var(--hk-accent) 24%, transparent); border-color: color-mix(in srgb, var(--hk-accent) 58%, transparent); }
        .selector { position: absolute; z-index: 5; top: 48px; left: 0; min-width: 208px; padding: 8px; display: grid; gap: 6px; background: rgba(22, 27, 32, 0.96); border: 1px solid var(--hk-border); box-shadow: 0 18px 45px rgba(0, 0, 0, 0.34); border-radius: 8px; backdrop-filter: blur(18px); }
        .selector button { border-radius: 8px; text-align: left; background: transparent; color: var(--hk-text); line-height: 1.25; padding-block: 8px; }
        .selector .selected { background: var(--hk-accent-soft); border-color: color-mix(in srgb, var(--hk-accent) 42%, transparent); }
        .suggestion, .session-list, .ending { margin-top: 18px; padding: 22px; border: 1px solid var(--hk-border); border-radius: 8px; background: var(--hk-card); box-shadow: 0 22px 70px rgba(0, 0, 0, 0.22); backdrop-filter: blur(22px); }
        .health-hero { display: grid; grid-template-columns: auto minmax(0, 1fr); gap: 20px; align-items: center; padding: 24px 0 18px; }
        .health-hero h1 { margin: 0; text-align: left; font-size: clamp(2rem, 5vw, 3.55rem); }
        .health-status { width: 142px; min-height: 118px; border-radius: 8px; display: grid; align-content: center; gap: 8px; text-align: center; padding: 14px; box-sizing: border-box; background: color-mix(in srgb, var(--hk-accent) 18%, transparent); border: 1px solid color-mix(in srgb, var(--hk-accent) 42%, transparent); box-shadow: 0 18px 50px rgba(0, 0, 0, 0.24); }
        .health-status span { font-size: 1.05rem; line-height: 1.08; font-weight: 820; }
        .health-status small { color: var(--hk-muted); font-weight: 740; line-height: 1.25; }
        .health-list { display: grid; gap: 12px; margin-top: 8px; }
        .area-card { padding: 16px; border: 1px solid var(--hk-border); border-radius: 8px; background: var(--hk-card); box-shadow: 0 18px 54px rgba(0, 0, 0, 0.18); backdrop-filter: blur(22px); }
        .area-head { display: grid; gap: 10px; align-items: start; }
        .area-chip-row { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 8px; }
        .area-chip-row.helped { margin-top: 0; }
        .area-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .area-columns > div { padding: 11px; border-radius: 8px; background: rgba(255,255,255,0.042); border: 1px solid var(--hk-border-soft); }
        .area-kicker { display: block; margin-bottom: 6px; color: color-mix(in srgb, var(--hk-accent) 78%, var(--hk-muted)); font-size: 0.78rem; font-weight: 800; }
        .area-columns p { color: var(--hk-muted); font-size: 0.9rem; }
        .area-columns p + p { margin-top: 4px; }
        .area-actions { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
        .area-help { display: inline-flex; align-items: center; gap: 7px; min-height: 34px; padding: 0 11px; }
        .area-help ha-icon { width: 18px; --mdc-icon-size: 18px; color: var(--hk-accent); }
        .area-help.nudge { background: color-mix(in srgb, var(--hk-accent) 11%, transparent); }
        .suggestion.refining { filter: blur(0.45px); opacity: 0.82; }
        .suggestion-head { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 14px; align-items: start; }
        .suggestion-head p, .support, .session-progress, .ending p { color: var(--hk-muted); margin-top: 6px; }
        .session-progress { font-size: 0.9rem; font-weight: 720; }
        .session-live-slot { min-height: 58px; display: grid; place-items: center; }
        .flash-slot { min-height: 50px; display: grid; place-items: center; margin-top: 2px; }
        .fit-line { color: color-mix(in srgb, var(--hk-accent) 72%, var(--hk-muted)); font-size: 0.88rem; font-weight: 680; }
        .icon-button, .ghost-icon { width: 40px; height: 40px; border-radius: 50%; border: 1px solid var(--hk-border-soft); display: inline-flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.052); color: var(--hk-text); cursor: pointer; }
        .icon-button.disabled { opacity: 0.55; cursor: default; }
        .meta { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 12px; }
        .meta-chip, .impact, .keeps-line { display: inline-flex; align-items: center; gap: 6px; min-height: 32px; padding: 0 10px; border-radius: 999px; background: rgba(255,255,255,0.058); border: 1px solid var(--hk-border-soft); color: var(--hk-text); font-size: 0.86rem; font-weight: 700; }
        .meta-chip.icon-chip { --hk-chip-icon-width: 34px; gap: 0; padding: 0; overflow: hidden; }
        .meta-chip strong { padding: 0 10px 0 9px; font-size: inherit; font-weight: inherit; }
        .meta-chip.warm { background: rgba(214, 181, 109, 0.105); color: #ead7a6; border-color: rgba(214, 181, 109, 0.22); }
        .meta-chip.warm ha-icon { color: #ead7a6; }
        .meta-chip.soft { background: rgba(255,255,255,0.042); color: var(--hk-muted); }
        .meta-chip.soft ha-icon { color: color-mix(in srgb, var(--hk-accent) 68%, var(--hk-muted)); }
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
        .chore-row.while-there { background: color-mix(in srgb, var(--hk-row) 82%, var(--hk-accent) 10%); border-style: dashed; }
        .row-kicker { display: inline-block; margin: 0 0 3px; color: color-mix(in srgb, var(--hk-accent) 76%, var(--hk-muted)); font-size: 0.76rem; line-height: 1.15; font-weight: 780; }
        .keeps-line.lost { background: rgba(214, 181, 109, 0.075); color: #ddc483; border-color: rgba(214, 181, 109, 0.18); }
        .chore-row span, .chore-row small, .session-chore p { display: block; color: var(--hk-muted); margin-top: 4px; line-height: 1.36; }
        .chore-row small { font-size: 0.82rem; }
        .actions, .row-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 16px; }
        .primary { border-color: color-mix(in srgb, var(--hk-accent) 65%, transparent); background: color-mix(in srgb, var(--hk-accent) 72%, #10221e); color: #f7fffb; font-weight: 760; }
        .benefit-action { display: inline-flex; align-items: center; justify-content: center; gap: 9px; min-width: 112px; margin-left: auto; padding: 8px 13px 8px 16px; box-shadow: 0 10px 26px rgba(0,0,0,0.2); }
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
        .timer { display: inline-flex; align-items: center; gap: 12px; padding: 8px 8px 8px 18px; border-radius: 999px; background: var(--hk-card-strong); border: 1px solid var(--hk-border-soft); box-shadow: 0 10px 28px rgba(0, 0, 0, 0.24); }
        .timer span { font-size: 1.45rem; line-height: 1; font-variant-numeric: tabular-nums; font-weight: 800; }
        .flash { width: fit-content; padding: 10px 16px; border-radius: 999px; color: #f5fff9; background: color-mix(in srgb, var(--hk-accent) 52%, #163028); font-weight: 800; box-shadow: 0 12px 30px rgba(0, 0, 0, 0.26); }
        .flash.bundle { padding-inline: 18px; background: color-mix(in srgb, var(--hk-accent) 68%, #18372d); box-shadow: 0 16px 38px rgba(0, 0, 0, 0.32); }
        .flash.optional { background: color-mix(in srgb, #d6b56d 30%, var(--hk-accent) 42%); }
        .flash.optional-2 { background: color-mix(in srgb, #d6b56d 42%, var(--hk-accent) 48%); box-shadow: 0 14px 34px rgba(0, 0, 0, 0.3); }
        .flash.optional-3 { padding-inline: 18px; background: color-mix(in srgb, #d6b56d 52%, var(--hk-accent) 50%); box-shadow: 0 16px 40px rgba(0, 0, 0, 0.34); }
        .completed-chore { background: color-mix(in srgb, var(--hk-accent) 10%, var(--hk-row)); border-color: color-mix(in srgb, var(--hk-accent) 34%, transparent); }
        .completed-chore h2 { color: color-mix(in srgb, var(--hk-text) 86%, var(--hk-accent)); }
        .done { color: #cfe9d9; }
        .done-badge { width: 38px; height: 38px; border-radius: 999px; display: inline-flex; align-items: center; justify-content: center; color: #f5fff9; background: color-mix(in srgb, var(--hk-accent) 48%, #172d25); border: 1px solid color-mix(in srgb, var(--hk-accent) 56%, transparent); }
        .skipped { color: var(--hk-muted); }
        .ending { text-align: center; }
        .ending .actions { justify-content: center; }
        .summary { min-height: 70vh; display: grid; align-content: center; justify-items: center; gap: 14px; }
        @media (max-width: 620px) {
          main { padding-left: 12px; padding-right: 12px; }
          .hero, .session-top, .summary { padding-top: 18px; }
          .tabs { margin-bottom: 12px; }
          .tabs button { padding: 0 10px; }
          h1 { font-size: clamp(1.85rem, 9vw, 2.7rem); }
          .session-top h1 { min-height: 2.18em; }
          .health-hero { grid-template-columns: 1fr; justify-items: center; text-align: center; gap: 14px; padding-top: 16px; }
          .health-hero h1 { text-align: center; font-size: clamp(1.8rem, 8vw, 2.5rem); }
          .health-status { width: 124px; min-height: 108px; }
          .area-columns { grid-template-columns: 1fr; }
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
    if (target.dataset.tab) {
      const returningToRightNow = target.dataset.tab === "right-now" && this.state.activeTab !== "right-now";
      this.state.activeTab = target.dataset.tab;
      this.state.selector = null;
      if (returningToRightNow) this.refreshRightNowGreeting();
      this.render();
      return;
    }
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
    if (action === "area-help") this.requestAreaHelp(target.dataset.area, target.dataset.helpMode);
    if (action === "shuffle") this.shuffle();
    if (action === "toggle-pause") {
      this.state.paused = !this.state.paused;
      this.render();
    }
    if (action === "dismiss-summary") this.resetReady();
    if (action === "finish") this.finishSession();
  }
}

customElements.define("homekeep-panel", HomekeepPanel);

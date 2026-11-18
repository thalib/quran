function round(n) {
  return Math.round(n);
}

function normalizeResult(r) {
  const status =
    r && (r.status || r.category || r.classification || r.result)
      ? String(
          r.status || r.category || r.classification || r.result,
        ).toLowerCase()
      : r && r.correct
        ? "correct"
        : r && r.answered === false
          ? "unanswered"
          : "incorrect";
  return {
    ...r,
    status,
    correct: status === "correct",
    answered: status !== "unanswered",
  };
}

export function extractResults(input) {
  if (input == null) return [];
  if (Array.isArray(input)) {
    if (
      input.length &&
      input[0] &&
      (input[0].status || input[0].correct !== undefined || input[0].word)
    ) {
      return input.map(normalizeResult);
    }
    return [];
  }
  if (Array.isArray(input.results)) return input.results.map(normalizeResult);
  if (Array.isArray(input.items)) return input.items.map(normalizeResult);
  if (Array.isArray(input.words)) return input.words.map(normalizeResult);
  if (Array.isArray(input.details)) return input.details.map(normalizeResult);
  return [];
}

export function summarize(resultsInput) {
  const results = extractResults(resultsInput);
  const total = results.length;
  const correct = results.filter((r) => r.correct).length;
  const unanswered = results.filter((r) => r.status === "unanswered").length;
  const incorrect = total - correct - unanswered;
  const attempted = correct + incorrect;
  const overallScore = total > 0 ? round((correct / total) * 100) : 0;
  const attemptedAccuracy =
    attempted > 0 ? round((correct / attempted) * 100) : 0;
  return {
    total,
    totalWords: total,
    attempted,
    attemptedAnswers: attempted,
    correct,
    correctAnswers: correct,
    incorrect,
    incorrectAnswers: incorrect,
    unanswered,
    unansweredWords: unanswered,
    unansweredCount: unanswered,
    overallScore,
    overall: overallScore,
    score: overallScore,
    percentage: overallScore,
    attemptedAccuracy,
    attempted_accuracy: attemptedAccuracy,
  };
}

export function calculateScore(input) {
  return summarize(input);
}

export function calculateScores(input) {
  return summarize(input);
}

export function scoreResults(input) {
  return summarize(input);
}

export function getScore(input) {
  return summarize(input);
}

export function calculateOverallScore(input) {
  return summarize(input).overallScore;
}

export function verseNumberFromResult(r) {
  const w = r && r.word ? r.word : r;
  if (w && typeof w.id === "string") {
    const parts = w.id.split(":");
    if (parts.length >= 2) return Number(parts[1]);
  }
  if (w && w.verseNumber != null) return Number(w.verseNumber);
  if (w && w.verse != null) return Number(w.verse);
  if (r && r.verseNumber != null) return Number(r.verseNumber);
  if (r && r.verse != null) return Number(r.verse);
  return null;
}

export function calculateVerseScores(input) {
  const results = extractResults(input);
  const groups = new Map();
  for (const r of results) {
    const vn = verseNumberFromResult(r);
    if (!groups.has(vn)) groups.set(vn, []);
    groups.get(vn).push(r);
  }
  const out = [];
  for (const [verseNumber, rs] of groups.entries()) {
    const s = summarize(rs);
    out.push({
      verseNumber,
      verse: verseNumber,
      ...s,
    });
  }
  out.sort((a, b) => (a.verseNumber || 0) - (b.verseNumber || 0));
  return out;
}

export function scoreByVerse(input) {
  return calculateVerseScores(input);
}

export function verseScores(input) {
  return calculateVerseScores(input);
}

export const calculate = summarize;

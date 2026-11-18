const PUNCTUATION = /[.,!?;:'"“”‘’`()\[\]{}…\-–—]/g;

export function normalizeAnswer(value) {
  if (value === null || value === undefined) return "";
  let text = String(value);
  try {
    text = text.normalize("NFC");
  } catch {
    // ignore
  }
  text = text.toLowerCase();
  text = text.replace(PUNCTUATION, " ");
  text = text.replace(/\s+/g, " ").trim();
  return text;
}

export function getAcceptedAnswers(word) {
  const m = word && word.meanings && word.meanings.en;
  if (!m) return [];
  return Array.isArray(m.accepted_answers) ? m.accepted_answers : [];
}

export function getPrimaryMeaning(word) {
  const m = word && word.meanings && word.meanings.en;
  return m && typeof m.primary === "string" ? m.primary : "";
}

export function isCorrectAnswer(userAnswer, word) {
  const normalized = normalizeAnswer(userAnswer);
  if (normalized === "") return false;
  return getAcceptedAnswers(word).map(normalizeAnswer).includes(normalized);
}

export function classifyAnswer(userAnswer, word) {
  const normalized = normalizeAnswer(userAnswer);
  if (normalized === "") return "unanswered";
  return isCorrectAnswer(userAnswer, word) ? "correct" : "incorrect";
}

function statusAliases(status) {
  const capitalized = status.charAt(0).toUpperCase() + status.slice(1);
  return {
    status,
    category: capitalized,
    classification: status,
    result: capitalized,
    correct: status === "correct",
    isCorrect: status === "correct",
    answered: status !== "unanswered",
    isAnswered: status !== "unanswered",
  };
}

export function checkWord(word, userAnswer) {
  const status = classifyAnswer(userAnswer, word);
  const normalized = normalizeAnswer(userAnswer);
  return {
    word,
    wordId: word ? word.id : null,
    id: word ? word.id : null,
    position: word ? word.position : null,
    arabic: word ? word.arabic : null,
    userAnswer: userAnswer == null ? "" : String(userAnswer),
    normalizedAnswer: normalized,
    primary: getPrimaryMeaning(word),
    primaryMeaning: getPrimaryMeaning(word),
    acceptedAnswers: getAcceptedAnswers(word),
    accepted_answers: getAcceptedAnswers(word),
    ...statusAliases(status),
  };
}

export function extractWords(source) {
  if (source == null) return [];
  if (Array.isArray(source)) {
    if (source.length === 0) return [];
    if (source[0] && Array.isArray(source[0].words)) {
      return source.flatMap((v) => (Array.isArray(v.words) ? v.words : []));
    }
    if (source[0] && (source[0].id || source[0].arabic || source[0].meanings)) {
      return source;
    }
    return [];
  }
  if (Array.isArray(source.words)) return source.words;
  if (Array.isArray(source.verses)) {
    return source.verses.flatMap((v) =>
      Array.isArray(v.words) ? v.words : [],
    );
  }
  return [];
}

function getAnswerForWord(answers, word, index) {
  if (Array.isArray(answers)) return answers[index];
  if (answers && typeof answers === "object") {
    if (Object.prototype.hasOwnProperty.call(answers, word.id))
      return answers[word.id];
    if (Object.prototype.hasOwnProperty.call(answers, String(word.position)))
      return answers[String(word.position)];
    if (Object.prototype.hasOwnProperty.call(answers, word.position))
      return answers[word.position];
  }
  return undefined;
}

export function checkAnswers(answers, source) {
  const words = extractWords(source);
  const results = words.map((w, i) =>
    checkWord(w, getAnswerForWord(answers || {}, w, i)),
  );
  const out = results;
  out.results = results;
  out.items = results;
  out.words = results;
  out.details = results;
  return out;
}

export const checkAnswer = checkWord;
export const evaluateAnswer = checkWord;
export const classify = classifyAnswer;
export const normalize = normalizeAnswer;
export const assessAnswers = checkAnswers;
export const evaluateAnswers = checkAnswers;
export const checkAll = checkAnswers;

import { ref, computed } from "vue";
import { loadSurah, getVerse } from "../services/quranService.js";

export function useQuran() {
  const surah = ref(null);
  const currentVerseId = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const verses = computed(() => (surah.value ? surah.value.verses : []));

  const currentVerse = computed(() => {
    if (!surah.value || currentVerseId.value == null) return null;
    return surah.value.verses.find(
      (v) => v.id === currentVerseId.value || v.number === currentVerseId.value,
    );
  });

  const words = computed(() =>
    currentVerse.value ? currentVerse.value.words : [],
  );

  async function load(id) {
    loading.value = true;
    error.value = null;
    try {
      surah.value = await loadSurah(id);
      if (surah.value.verses.length) {
        currentVerseId.value = surah.value.verses[0].id;
      }
    } catch (e) {
      error.value = e;
      surah.value = null;
    } finally {
      loading.value = false;
    }
  }

  function setVerse(id) {
    currentVerseId.value = id;
  }

  return {
    surah,
    verses,
    currentVerse,
    currentVerseId,
    words,
    loading,
    error,
    load,
    setVerse,
  };
}

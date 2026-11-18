<template>
  <div>
    <h1>Surahs</h1>
    <p>Only Surah Al-Fatiha is available initially.</p>
    <ul class="list-group">
      <li
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <div>
          <strong>1. Al-Fatiha (الفاتحة)</strong>
          <div class="text-muted small">The Opening — 7 verses</div>
        </div>
        <router-link to="/surah/1" class="btn btn-sm btn-primary">
          Open
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup></script>

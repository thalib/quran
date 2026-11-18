<template>
  <div class="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container">
        <router-link class="navbar-brand" to="/">Quran Learning</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#nav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="nav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <i class="bi bi-house"></i> Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/surahs">
                <i class="bi bi-book"></i> Surahs
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/history">
                <i class="bi bi-clock-history"></i> History
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/settings">
                <i class="bi bi-gear"></i> Settings
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <main class="container mt-4">
      <router-view />
    </main>
  </div>
</template>

<script setup></script>

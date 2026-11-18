import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SurahListView from "../views/SurahListView.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/surahs", component: SurahListView },
  {
    path: "/surah/:id",
    component: () => import("../views/LearningView.vue"),
  },
  {
    path: "/surah/:id/results",
    component: () => import("../views/ResultsView.vue"),
  },
  {
    path: "/history",
    component: () => import("../views/HistoryView.vue"),
  },
  {
    path: "/settings",
    component: () => import("../views/SettingsView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

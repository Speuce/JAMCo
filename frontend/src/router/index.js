import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import Sandbox from "@/views/Sandbox.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/tracking",
      name: "tracking",
      component: () => import("../views/JobTrackingView.vue"),
    },
    {
      path: "/sandbox",
      name: "sandbox",
      component: Sandbox,
    },
  ],
});

export default router;

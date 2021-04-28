import { createWebHistory, createRouter } from "vue-router";
import Main from "@/views/Main.vue";
import Recommend from "@/views/Recommend.vue";
import Message from "@/views/Message.vue";
import PublishMessage from "@/views/PublishMessage.vue";
import AuthLogin from "@/views/AuthLogin.vue";
import AuthRegist from "@/views/AuthRegist.vue";
import Profile from "@/views/Profile.vue"

const routes = [
  {
    path: "/main",
    name: "Main",
    component: Main,
    children: [
        {
          path: "/",
          name: "Recommend",
          component: Recommend,
        },
        {
          path: "/publish",
          name: "PublishMessage",
          component: PublishMessage,
        },
        {
          path: "/message/:mid",
          name: "Message",
          component: Message,
        },
        {
          path: "/profile",
          name: "Profile",
          component: Profile,
        },
    ]
  },
  {
    path: "/login",
    name: "AuthLogin",
    component: AuthLogin,
  },
  {
    path: "/regist",
    name: "AuthRegist",
    component: AuthRegist,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
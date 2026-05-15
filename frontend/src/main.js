import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
createApp(App).use(router).use(ElementPlus).mount("#app");
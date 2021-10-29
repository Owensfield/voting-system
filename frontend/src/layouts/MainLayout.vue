<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title> Owensfield voting system </q-toolbar-title>

        <div>v0.01</div>
        <q-btn
          v-if="$q.dark.isActive"
          flat
          round
          @click="toggleDarkMode()"
          color="white"
          icon="light_mode"
        ></q-btn>
        <q-btn
          v-else
          flat
          round
          @click="toggleDarkMode()"
          color="white"
          icon="dark_mode"
        ></q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Menu </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
      <q-btn
        unelevated
        color="primary"
        label="Login"
        icon="lock"
        class="q-ma-md"
      ></q-btn>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import EssentialLink from "components/EssentialLink.vue";

const linksList = [
  {
    title: "Main",
    caption: "View all polls",
    icon: "home",
    link: "./",
  },
];

import { defineComponent, ref } from "vue";
import { Dark } from "quasar";
export default defineComponent({
  name: "MainLayout",
  darkMode: false,

  components: {
    EssentialLink,
  },

  setup() {
    const leftDrawerOpen = ref(false);

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      Dark.set(this.darkMode);
      window.localStorage.setItem("darkMode", this.darkMode);
    },
  },
  created() {
    var mode = window.localStorage.getItem("darkMode");
    if (mode == "true") {
      Dark.set(true);
      this.darkMode = true;
    }
  },
});
</script>

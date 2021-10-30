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

        <q-toolbar-title> </q-toolbar-title>

        <div>v0.01</div>

        <q-btn
          unelevated
          color="primary"
          label="Login"
          icon="lock"
          class="q-ma-md"
          @click="loginFormShow = true"
        ></q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Owensfield voting system </q-item-label>

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
        @click="loginFormShow = true"
      ></q-btn>
    </q-drawer>

    <q-dialog v-model="loginFormShow" position="top">
      <q-card style="width: 500px">
        <q-card-section> </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
            <q-input filled type="number" v-model="loginForm.pin" label="Pin" />
            <q-input
              filled
              type="password"
              v-model="loginForm.password"
              label="Password"
            />

            <div>
              <q-btn label="Submit" type="submit" color="primary" />
              <q-btn
                label="Cancel"
                type="reset"
                color="primary"
                flat
                class="q-ml-sm"
                v-close-popup
              />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

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

  components: {
    EssentialLink,
  },

  setup() {
    const leftDrawerOpen = ref(false);

    return {
      loginFormShow: ref(false),
      loginForm: {},

      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
  methods: {
    onSubmit() {
      window.localStorage.setItem("userPin", this.loginForm.pin);
      this.makeRequest("GET", "https://google.com");
      window.localStorage.setItem("userHash", this.loginForm.hash);
    },
    onReset() {
      console.log("yeah");
    },
    makeRequest(type, URL, data = null) {
      this.httpRequest = new XMLHttpRequest();
      if (!this.httpRequest) {
        alert("Giving up :( Cannot create an XMLHTTP instance");
        return false;
      }
      this.httpRequest.onreadystatechange = this.alertContents;
      this.httpRequest.open(type, URL);
      this.httpRequest.send();
    },
    alertContents() {
      if (this.httpRequest.readyState === XMLHttpRequest.DONE) {
        if (this.httpRequest.status === 200) {
          alert(this.httpRequest.responseText);
        } else {
          alert("There was a problem with the request.");
        }
      }
    },
  },
  created() {
    Dark.set(true);
    //  this.loginForm.pin = window.localStorage.getItem("userPin");
    //  this.loginForm.hash = window.localStorage.getItem("userHash");
  },
});
</script>

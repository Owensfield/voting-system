<template>
  <q-page>
    <q-btn
      outline
      color="primary"
      label="Create a poll"
      class="q-ma-md"
    ></q-btn>
    <q-card class="my-card q-ma-md" style="width: 100%">
      <q-card-section>
        <div class="text-h6">Active Polls</div>
      </q-card-section>
      <q-card-section class="q-pt-none"> poo </q-card-section>
    </q-card>

    <q-card class="my-card q-ma-md" style="width: 100%">
      <q-card-section>
        <div class="text-h6">Polls waiting for approval</div>
      </q-card-section>

      <q-card-section class="q-pt-none"> woo </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "PageIndex",
});
</script>

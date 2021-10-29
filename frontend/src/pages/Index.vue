<template>
  <q-page>
    <q-btn
      outline
      color="primary"
      label="Create a poll"
      class="q-ma-md"
      @click="createPoll()"
    ></q-btn>
    <q-card class="my-card q-ma-md" style="width: 100%">
      <q-card-section>
        <div class="text-h6">Active Polls</div>
        <div class="text-subtitle2">Polls active that need votes</div>
      </q-card-section>
      <q-card-section class="q-pt-none"> </q-card-section>
    </q-card>

    <q-card class="my-card q-ma-md" style="width: 100%">
      <q-card-section>
        <div class="text-h6">Polls waiting for approval</div>
        <div class="text-subtitle2">
          Polls need 4/7 steering group members to approve. Unsuccessful polls
          will be deleted after two weeks.
        </div>
      </q-card-section>

      <q-card-section class="q-pt-none"> </q-card-section>
    </q-card>
    <q-dialog v-model="createPollDialogue" position="top">
      <q-card style="width: 500px">
        <q-card-section> </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
            <q-input
              filled
              v-model="name"
              label="Title"
              hint="Question/description, keep concise"
              lazy-rules
              :rules="[(val) => (val && val.length > 0) || 'Must have a title']"
            />
            <q-input filled v-model="opt1" label="Option 1" />
            <q-input filled v-model="opt2" label="Option 2" />
            <q-input filled v-model="opt3" label="Option 3 (optional)" />
            <q-input filled v-model="opt4" label="Option 4 (optional)" />
            <q-input filled v-model="opt5" label="Option 5 (optional)" />

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
  </q-page>
</template>

<script>
import { defineComponent } from "vue";
import { ref } from "vue";
export default defineComponent({
  name: "PageIndex",
  setup() {
    return {
      createPollDialogue: ref(false),
    };
  },
  methods: {
    createPoll() {
      console.log("poo");
      this.createPollDialogue = true;
      console.log(this.createPollDialogue);
    },
  },
});
</script>

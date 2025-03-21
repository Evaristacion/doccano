<template>
  <v-card>
    <v-card-title>Create a Perspective</v-card-title>
    <v-card-text>
      <v-form ref="form" v-model="valid">
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              :value="name"
              :rules="[rules.required, rules.counter]"
              label="Name"
              outlined
              required
              @input="$emit('update:name', $event)"
            />
          </v-col>
          <v-col cols="12" sm="6">
            <v-select
              :value="type"
              :items="dataTypes"
              :rules="[rules.required]"
              label="Type"
              outlined
              required
              @input="$emit('update:type', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="12">
            <slot :valid="valid" />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    name: {
      type: String,
      required: true
    },
    type: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      valid: false,
      dataTypes: ['number', 'string'],
      rules: {
        required: (v: string) => !!v || 'This field is required',
        counter: (v: string) => (v && v.length <= 100) || 'Name must be less than 100 characters'
      }
    }
  }
})
</script>
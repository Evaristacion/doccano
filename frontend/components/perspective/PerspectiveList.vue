<template>
  <v-data-table
    :value="value"
    :headers="headers"
    :items="items"
    :search="search"
    :loading="isLoading"
    :loading-text="$t('generic.loading')"
    :no-data-text="$t('vuetify.noDataAvailable')"
    :footer-props="{
      showFirstLastPage: true,
      'items-per-page-text': $t('vuetify.itemsPerPageText'),
      'page-text': $t('dataset.pageText')
    }"
    item-key="id"
    show-select
    @input="$emit('input', $event)"
  >
    <template #top>
      <v-text-field
        v-model="search"
        :prepend-inner-icon="mdiMagnify"
        :label="$t('generic.search')"
        single-line
        hide-details
        filled
      />
    </template>
    <template #[`item.type`]="props">
      <span>{{ props.item.type }}</span>
    </template>
    <template #[`item.actions`]="{ item }">
      <v-icon small @click="$emit('edit', item)">
        {{ mdiPencil }}
      </v-icon>
    </template>
  </v-data-table>
</template>

<script lang="ts">
import { mdiMagnify, mdiPencil } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { PerspectiveDTO } from '~/services/application/perspective/perspectiveData'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<PerspectiveDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<PerspectiveDTO[]>,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      search: '',
      mdiPencil,
      mdiMagnify
    }
  },

  computed: {
    headers() {
      const headers = [
        { text: 'Name', value: 'name', sortable: true },
        { text: 'Type', value: 'type', sortable: true }
      ]
      return headers
    }
  }
})
</script>
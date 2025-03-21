<template>
  <v-card>
    <v-card-title>
      <v-btn
        class="text-capitalize ms-2"
        color="primary"
        @click="$router.push('perspective/add')"
      >
        {{ $t('generic.create') }}
      </v-btn>
    </v-card-title>
    <perspective-list
      v-model="selected"
      :items="items"
      :is-loading="isLoading"
    />
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import PerspectiveList from '@/components/perspective/PerspectiveList.vue'
import { PerspectiveDTO } from '~/services/application/perspective/perspectiveData'

export default Vue.extend({
  components: {
    PerspectiveList
  },

  layout: 'project',

  data() {
    return {
      items: [] as PerspectiveDTO[],
      selected: [] as PerspectiveDTO[],
      isLoading: false
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    service(): any {
      return this.$services.perspective
    }
  },

  async created() {
    await this.list()
  },

  methods: {
    async list() {
      this.isLoading = true
      this.items = await this.service.list(this.projectId)
      this.isLoading = false
    },
  }
})
</script>
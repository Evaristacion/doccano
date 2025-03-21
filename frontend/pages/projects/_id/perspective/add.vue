<template>
  <form-create
    :name="editedItem.name"
    :type="editedItem.type"
    @update:name="editedItem.name = $event"
    @update:type="editedItem.type = $event"
  >
    <template #default="{ valid }">
      <v-btn :disabled="!valid" color="primary" @click="save">
        Save
      </v-btn>
      <v-btn :disabled="!valid" color="primary" outlined @click="saveAndAnother">
        Save and add another
      </v-btn>
    </template>
  </form-create>
</template>

<script lang="ts">
import Vue from 'vue'
import FormCreate from '~/components/perspective/FormCreate.vue'
import { PerspectiveDTO } from '~/services/application/perspective/perspectiveData'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  data() {
    return {
      editedItem: {
        name: '',
        type: ''
      } as PerspectiveDTO,
      defaultItem: {
        name: '',
        type: ''
      } as PerspectiveDTO
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

  methods: {
    async save() {
      try {
        await this.service.createPerspective(this.projectId, this.editedItem)
        this.$router.push(`/projects/${this.projectId}/perspective`)
      } catch (error) {
        console.error('Error creating perspective:', error)
      }
    },

    async saveAndAnother() {
      try {
        await this.service.createPerspective(this.projectId, this.editedItem)
        this.editedItem = Object.assign({}, this.defaultItem)
      } catch (error) {
        console.error('Error creating perspective:', error)
      }
    }
  }
})
</script>
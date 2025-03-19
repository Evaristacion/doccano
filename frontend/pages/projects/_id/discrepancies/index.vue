<template>
  <v-container>
    <h1>Discrepancies</h1>
    <p>This is the discrepancies page for the project.</p>

    <v-card v-if="!isLoading" class="mt-4">
      <v-card-text>
        <p>Discrepancy percentage: <strong>{{ discrepancyPercentage }}%</strong></p>
      </v-card-text>
    </v-card>

    <p v-if="isLoading">Loading...</p>
    <p v-if="error" class="error-message">{{ error }}</p>
  </v-container>
</template>

<script>
export default {
  layout: "projects",
  middleware: ["check-auth", "auth"],
  data() {
    return {
      discrepancyPercentage: null,
      isLoading: true,
      error: null,
    };
  },
  mounted() {
    this.fetchDiscrepancyData();
  },
  methods: {
    async fetchDiscrepancyData() {
      try {
        const projectId = this.$route.params.id;
        const response = await this.$axios.get(`/v1/projects/${projectId}`);
        this.discrepancyPercentage = response.data.discrepancy_percentage;
      } catch (error) {
        console.error("Error fetching discrepancy data:", error.response?.data);
        this.error = "An error occurred while loading discrepancy data.";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
}
</style>

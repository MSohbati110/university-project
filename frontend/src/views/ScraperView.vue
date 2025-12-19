<template>
  <v-container>
    <v-row justify="center">
      <!-- Scraper Form -->
      <scraper-form @scrape-completed="updateJobs"></scraper-form>

      <ScrapeJobsDashboard :reloadFlag="reloadFlag"></ScrapeJobsDashboard>
    </v-row>
  </v-container>
</template>

<script>
import ScraperForm from '@/components/ScraperForm.vue'
import ScrapeJobsDashboard from '@/components/ScrapeJobsDashboard.vue'

export default {
  components: {
    ScraperForm,
    ScrapeJobsDashboard
  },
  data() {
    return {
      reloadFlag: ''
    }
  },
  methods: {
    updateJobs() {
      this.reloadFlag = Date.now();
    }
  }
}
</script>

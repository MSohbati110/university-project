<template>
  <v-container>
    <v-row justify="center">
      <!-- Scraper Form -->
      <scraper-form @scrape-completed="updateResults"></scraper-form>
  
      <!-- Results Component -->
      <scrape-results :reloadFlag="reloadFlag"></scrape-results>
    </v-row>
  </v-container>
</template>

<script>
import ScraperForm from '@/components/ScraperForm.vue'
import ScrapeResults from '@/components/ScrapeResults.vue'

export default {
  components: {
    ScraperForm,
    ScrapeResults
  },
  data() {
    return {
      reloadFlag: ''
    }
  },
  methods: {
    updateResults() {
      this.reloadFlag = Date.now();
    }
  }
}
</script>

<template>
  <v-container>
    <v-row justify="center">
      <!-- Results Component -->
      <scrape-results :reloadFlag="reloadFlag"></scrape-results>
    </v-row>
  </v-container>
</template>

<script>
import ScrapeResults from '@/components/ScrapeResults.vue'

export default {
  components: {
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

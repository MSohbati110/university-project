<template>
  <v-container>
    <v-card elevation="6" class="pa-6">
      <v-card-title class="text-h6">
        Scraping Jobs
      </v-card-title>

      <v-divider class="mb-4"></v-divider>

      <v-data-table
        :headers="headers"
        :items="jobs"
        item-key="id"
        dense
      >
        <!-- Auto Scrape Toggle -->
        <template v-slot:item.auto_scrape="{ item }">
          <v-switch
            v-model="item.auto_scrape"
            color="primary"
            inset
            @change="toggleAutoScrape(item)"
          />
        </template>

        <!-- Status Chip -->
        <template v-slot:item.status="{ item }">
          <v-chip
            :color="item.auto_scrape ? 'green' : 'grey'"
            dark
            small
          >
            {{ item.auto_scrape ? 'Active' : 'Inactive' }}
          </v-chip>
        </template>

        <!-- Last Scraped -->
        <template v-slot:item.last_scraped_at="{ item }">
          <span v-if="item.last_scraped_at">
            {{ formatDate(item.last_scraped_at) }}
          </span>
          <span v-else class="text-grey">
            Never
          </span>
        </template>
      </v-data-table>

      <!-- Feedback -->
      <v-snackbar v-model="snackbar" timeout="2500" color="success">
        {{ snackbarText }}
      </v-snackbar>
    </v-card>
  </v-container>
</template>

<script>
import api from '@/api'

export default {
  props: ["reloadFlag"],
  name: 'ScrapeJobsDashboard',
  data() {
    return {
      jobs: [],
      snackbar: false,
      snackbarText: '',
      headers: [
        { text: 'URL', value: 'url' },
        { text: 'Auto Scrape', value: 'auto_scrape', sortable: false },
        { text: 'Status', value: 'status', sortable: false },
        { text: 'Interval (sec)', value: 'scrape_interval' },
        { text: 'Last Scraped', value: 'last_scraped_at' },
      ],
    }
  },
  mounted() {
    this.fetchJobs()
  },
  methods: {
    async fetchJobs() {
      const res = await api.scrapeJobs()
      this.jobs = res.data      
    },
    async toggleAutoScrape(job) {
      try {
        await api.toggleAutoScrape({
          url: job.url,
          enabled: job.auto_scrape
        })

        this.snackbarText = job.auto_scrape
          ? 'Automated scraping enabled'
          : 'Automated scraping disabled'

        this.snackbar = true
      } catch (err) {
        job.auto_scrape = !job.auto_scrape // rollback
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleString()
    },
  },
  watch: {
    reloadFlag: {
      handler() {
        this.fetchJobs();
      },
      deep: true
    }
  },
}
</script>

<template>
  <v-container class="py-8" style="width:650px; margin:0">
    <v-card elevation="5" class="pa-6" width="600px">
      <v-card-title class="text-h5">Web Scraper</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitScrape">
          <v-row>
            <!-- URLs Input -->
            <v-col cols="12">
              <v-textarea
                v-model="urlsText"
                label="URLs (one per line)"
                placeholder="https://example.com/product1"
                rows="5"
                outlined
                required
              ></v-textarea>
            </v-col>

            <!-- Selectors Input -->
            <v-col cols="12">
              <v-textarea
                v-model="selectorsText"
                label="Selectors"
                placeholder='h1'
                rows="5"
                outlined
                required
              ></v-textarea>
            </v-col>
          </v-row>

          <!-- Submit Button -->
          <v-row justify="space-between" align="center">
            <v-col>
              <!-- Loading -->
              <v-alert
                v-if="loading"
                type="info"
                class="mt-4"
                border="left"
                colored-border
              >
                Scraping in progress...
              </v-alert>
  
              <!-- Error -->
              <v-alert
                v-if="error"
                type="error"
                class="mt-4"
                border="left"
                colored-border
              >
                {{ error }}
              </v-alert>

              <!-- Success Alert -->
              <v-alert
                v-model="successAlert"
                type="success"
                border="left"
                colored-border
                dense
                class="mb-0 mt-1"
              >
                Scraping completed successfully!
              </v-alert>
            </v-col>

            <v-col cols="auto">
              <v-btn type="submit" color="primary" :loading="loading">
                Scrape
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      urlsText: "",
      selectorsText: "",
      loading: false,
      error: "",
      successAlert: false,
    };
  },
  methods: {
    async submitScrape() {
      this.error = "";
      this.loading = true;
      this.successAlert = false;

      try {
        const urls = this.urlsText
          .split("\n")
          .map((u) => u.trim())
          .filter((u) => u);

        let selectors;
        try {
          selectors = this.selectorsText.split("\n");
        } catch (e) {
          this.error = "Selectors must be valid";
          this.loading = false;
          return;
        }

        if (selectors[0] == '') {
          selectors = ['div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        }        

        const response = await api.scrape({urls, selectors});

        this.$emit('scrape-completed')

        this.successAlert = true;
        setTimeout(() => {
          this.successAlert = false;
        }, 3000)
      } catch (err) {
        this.error = err.response?.data?.error || err.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.v-card {
  max-width: 900px;
  margin: 0 auto;
}
</style>

<template>
  <v-container class="py-8" style="width:650px; margin:0">
    <v-card elevation="5" class="pa-6" width="600px">
      <v-card-title class="text-h5">Scraper Results</v-card-title>
      <!-- URL Filter -->
      <v-select
        v-model="selectedUrl"
        :items="urls"
        label="Select URL"
        dense
        outlined
        class="mb-4"
      ></v-select>

      <!-- Selector Filter -->
      <v-select
        v-model="selectedSelectors"
        :items="selectors"
        label="Select elements to show"
        multiple
        dense
        outlined
        class="mb-4"
      ></v-select>

      <v-row justify="end">
        <v-btn
          color="primary"
          class="mb-4"
          :disabled="!selectedUrl || selectedSelectors.length === 0"
          @click="fetchFilteredResults"
        >
          Load Results
        </v-btn>
      </v-row>

      <!-- Results Table -->
      <v-simple-table v-if="isResults">
        <thead>
          <tr>
            <th  v-for="item in headers" :key="item.id">{{ item.name }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in results" :key="row.id">
            <td v-for="item in headers" :key="item.id">
              {{ row[item.name] }}
            </td>
          </tr>
        </tbody>
      </v-simple-table>

      <div v-else class="text-center mt-4 text-subtitle-1">
        No data loaded yet
      </div>
    </v-card>
  </v-container>
</template>

<script>
import api from "@/api";

export default {
  props: ["reloadFlag"],
  data() {
    return {
      selectedUrl: null,
      selectedSelectors: [],
      jobList: {},
      results: {},
      headers: {},
      isResults: false,
    }
  },
  mounted() {
    this.getJobList();
  },
  methods: {
    async getJobList() {
      try {
        const response = await api.scrapeJobs();
        this.jobList = response.data;
      } catch (err) {
        console.error("Error fetching job list:", err);
      }
    },
    async fetchFilteredResults() {
      try {
        const response = await api.filteredResults({
          url: this.selectedUrl,
          selectors: this.selectedSelectors
        });

        let tmp = {}
        let tmplist = {};
        this.results = [];
        this.headers = [];
        let counter = 0;
        let number = 0;
        for (let data of response.data) {
          tmplist[data.element_name] = data.element_value.split(', ');
          this.headers.push({name: data.element_name, id: number});
          counter = Math.max(counter, tmplist[data.element_name].length);
          number++;
        }

        for (let i=0 ; i<counter ; i++) {
          tmp = {id: i};
          for (let item of Object.keys(tmplist)) {
            tmp[item] = tmplist[item][i];       
          }
          this.results.push(tmp);
        }        
        
        this.isResults = true;
      } catch (err) {
        this.isResults = false;
        console.error("Error fetching filtered results:", err);
      }
    }
  },
  computed: {
    urls() {
      return Object.keys(this.jobList);
    },
    selectors() {
      if (this.selectedUrl)
        return this.jobList[this.selectedUrl]
      
      return []
    },
  },
  watch: {
    reloadFlag: {
      handler() {
        this.getJobList();
      },
      deep: true
    }
  },
}
</script>

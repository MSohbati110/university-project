<template>
  <v-container class="py-8" style="margin:0">
    <v-row justify="center">
      <v-col cols="12" md="4">
        <v-card elevation="5" class="pa-6" width="600px">
          <v-card-title class="text-h5">Scraper Results</v-card-title>
          <!-- Source Type -->
          <v-select
            v-model="sourceType"
            :items="['web', 'api']"
            label="Select Source Type"
            outlined
            dense
            class="mb-4"
          />
    
          <!-- URL Filter -->
          <v-select
            v-model="selectedUrl"
            :items="urls"
            label="Select URL"
            dense
            outlined
            class="mb-4"
            :disabled="!sourceType"
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
            :disabled="(!selectedUrl) || sourceType != 'web'"
            ></v-select>
    
          <v-row justify="end">
            <v-btn
              :disabled="!rawResponse"
              color="primary"
              @click="exportResults"
            >
              Export JSON
            </v-btn>

            <v-btn
              color="primary"
              class="ml-4"
              :disabled="!selectedUrl || (selectedSelectors.length === 0 && sourceType == 'web')"
              @click="fetchFilteredResults"
            >
              Load Results
            </v-btn>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <v-card elevation="5" class="pa-6 mt-2">
      <v-tabs v-model="activeTab" background-color="primary" dark>
        <v-tab value="raw">Raw Data</v-tab>
        <v-tab value="clean">Cleaned Text</v-tab>
        <v-tab value="token">Cleaned Text Tokens</v-tab>
        <v-tab value="pattern">MetaData</v-tab>
      </v-tabs>

      <!-- Results Table -->
      <v-simple-table v-if="isResults">
        <thead>
          <tr>
            <th v-for="item in headers" :key="item.id">{{ item.name }}</th>
          </tr>
        </thead>
        <tbody v-if="activeTab == 0">
          <tr v-for="row in results" :key="row.id">
            <td v-for="item in headers" :key="item.id">
              {{ row[item.name] }}
            </td>
          </tr>
        </tbody>
        <tbody v-if="activeTab == 1">
          <tr v-for="row in cleanedResults" :key="row.id">
            <td v-for="item in headers" :key="item.id">
              {{ row[item.name] }}
            </td>
          </tr>
        </tbody>
        <tbody v-if="activeTab == 2">
          <tr v-for="row in cleanedResultsTokens" :key="row.id">
            <td v-for="item in headers" :key="item.id">
              {{ row[item.name] }}
            </td>
          </tr>
        </tbody>
        <tbody v-if="activeTab == 3">
          <tr v-for="row in metadataResults" :key="row.id">
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
  data() {
    return {
      sourceType: null,
      selectedUrl: null,
      selectedSelectors: [],
      jobList: {},
      results: {},
      headers: {},
      isResults: false,
      activeTab: 0,
      rawResponse: null,
    }
  },
  mounted() {
    this.getJobList();
  },
  methods: {
    async getJobList() {
      try {
        const response = await api.scrapeSelectors();
        this.jobList = response.data;
      } catch (err) {
        console.error("Error fetching job list:", err);
      }
    },
    async fetchFilteredResults() {
      try {
        const response = await api.filteredResults({
          url: this.selectedUrl,
          selectors: this.selectedSelectors,
          source_type: this.sourceType
        });
        this.rawResponse = response.data;

        let tmp = {};
        let tmplist = {};
        this.results = [];
        this.cleanedResults = [{id: 0}];
        this.cleanedResultsTokens = [];
        this.metadataResults= [{id: 0}];
        this.headers = [];
        let counter = 0;
        let tokenCounter = 0;
        let number = 0;

        if (this.sourceType == 'web') {
          for (let data of response.data) {
            tmplist[data.element_name] = data.element_value.split(', ');
            this.headers.push({name: data.element_name, id: number});

            this.cleanedResults[0][data.element_name] = data.cleaned_value;
            this.metadataResults[0][data.element_name] = data.metadata;

            counter = Math.max(counter, tmplist[data.element_name].length);
            tokenCounter = Math.max(tokenCounter, data.cleaned_value_tokens.length);
            number++;
          }
  
          for (let i=0 ; i<counter ; i++) {
            tmp = {id: i};
            for (let item of Object.keys(tmplist)) {
              tmp[item] = tmplist[item][i];       
            }
            this.results.push(tmp);
          }

          for (let i=0 ; i<tokenCounter ; i++) {
            tmp = {id: i};
            for (let data of response.data) {
              tmp[data.element_name] = data.cleaned_value_tokens[i];       
            }
            this.cleanedResultsTokens.push(tmp);
          }
        }
        if (this.sourceType == 'api') {
          let tmpHeaders = [];
          for (let data of response.data) {
            Object.keys(data).forEach((key) => {
              if (!tmpHeaders.includes(key)) {
                this.headers.push({
                  id: counter,
                  name: key
                });
                tmpHeaders.push(key);
              }
              counter++;
            })
          }

          this.results = response.data.map((item, index) => ({
            ...item,
            id: index
          }));
        }

        this.isResults = true;
      } catch (err) {
        this.isResults = false;
        console.error("Error fetching filtered results:", err);
      }
    },
    exportResults() {
      const dataStr = JSON.stringify(this.rawResponse, null, 2); // pretty format
      const blob = new Blob([dataStr], { type: "application/json" });

      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = url;
      link.download = "results.json";
      link.click();

      window.URL.revokeObjectURL(url);
    }
  },
  computed: {
    urls() {
      if (this.sourceType)
        return Object.keys(this.jobList[this.sourceType]);
    },
    selectors() {
      if (this.selectedUrl)
        return this.jobList['web'][this.selectedUrl]
      
      return []
    },
  },
  watch: {
    sourceType(val) {
      this.selectedUrl = null;
      this.selectedSelectors = [];
    }
  }
}
</script>

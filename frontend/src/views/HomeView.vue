<template>
  <v-container class="py-16 text-center">
    <h1 class="text-h3 font-weight-bold mb-4">
      Welcome to Data Harbor
    </h1>

    <p class="text-subtitle-1 mb-8">
      Intelligent web scraping and data exploration platform
    </p>

    <v-row justify="center" dense>
      <v-btn color="primary" large class="mx-2" to="/scraper">
        Go to Scraper
      </v-btn>

      <v-btn outlined large class="mx-2" to="/dashboard">
        View Dashboard
      </v-btn>
    </v-row>
  </v-container>
</template>

<template>
  <v-app-bar app color="primary" dark elevation="4">
    <!-- Logo / Brand -->
    <v-btn text class="d-flex align-center" @click="$router.push('/')">
      <span class="text-h6 font-weight-bold">Data Harbor</span>
    </v-btn>

    <v-spacer />

    <!-- Navigation -->
    <v-btn text to="/scraper">Scraper</v-btn>
    <v-btn text to="/dashboard">Dashboard</v-btn>
  </v-app-bar>
</template>

<template>
  <v-app>
  <!-- <v-app style="background-color: var(--bg-color);"> -->
    <!-- v-if="!$route.meta.hideNavbar" -->
    <Navbar></Navbar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
  },
  data() {
    return {

    }
  }
};
</script>

<!-- <style>
@font-face {
  font-family: 'Inter';
  src: url("assets/fonts/Inter-Regular.ttf") format("truetype"),
       url("assets/fonts/Inter-Regular.woff2") format("woff2");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: 'IRANSans';
  src: url("assets/fonts/IRANSans-web.ttf") format("truetype"),
    url("assets/fonts/IRANSans-web.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}
* {
  font-family: "Inter";
  font-size: 16px;
  --bg-color: linear-gradient(180deg, #071827 20%, #19578D 100%);
  --box-shadow-color: #005CC3;
  --white: #f0f0f0;
  --white2: #c4c9d0;
  --color1: #283140;
  --color2: #002C5D;
  --color3: #23303F;
  --navbar: #052E5C;
  --card: #0B253C;
  --disable-card: rgba(26, 47, 64);
  --accent: #0069D9;
  --input-box: rgba(112, 112, 112, 0.15);
  --font-size-small: 13.33px;
  --font-size-extra-small: 11.11px;
}
h1 {
  font-size: 47.78px;
  font-weight: 400;
}
h2 {
  font-size: 39.81px;
  font-weight: 400;
}
h3 {
  font-size: 33.18px;
  font-weight: 400;
}
h4 {
  font-size: 27.65px;
  font-weight: 400;
}
h5 {
  font-size: 23.04px;
  font-weight: 400;
}
h6 {
  font-size: 19.2px;
  font-weight: 400;
}
body {
  height: 100%;
  color: #5D6D7E;
  user-select: none;
  background: var(--bg-color);
}
.v-text-field__slot {
  text-align: right !important;
}
div.tooltip {
  display: none;
}
.no-margin {
  margin: 0 !important;
}
.no-padding {
  padding: 0 !important;
}
.be-center {
  justify-content: center !important;
  align-items: center !important;
}
.be-white {
  color: var(--white) !important;
}
.be-bold {
  font-weight: bold !important;
}
.v-input__slot {
  margin: 0 !important;
}



[dir="rtl"] *{
  font-family: "IRANSans";
  font-size: 14px;
  --font-size-small: 11.67px;
  --font-size-extra-small: 9.72px;
}
[dir="rtl"] h1 {
  font-size: 41.8px;
  font-weight: 400;
}
[dir="rtl"] h2 {
  font-size: 34.84px;
  font-weight: 400;
}
[dir="rtl"] h3 {
  font-size: 29.03px;
  font-weight: 400;
}
[dir="rtl"] h4 {
  font-size: 24.19px;
  font-weight: 400;
}
[dir="rtl"] h5 {
  font-size: 20.16px;
  font-weight: 400;
}
[dir="rtl"] h6 {
  font-size: 16.8px;
  font-weight: 400;
}


@media (max-width: 1600px) {
  * {
    font-size: 14px;
    --font-size-small: 11.67px;
    --font-size-extra-small: 9.72px;
  }
  h1 {
    font-size: 41.8px;
    font-weight: 400;
  }
  h2 {
    font-size: 34.84px;
    font-weight: 400;
  }
  h3 {
    font-size: 29.03px;
    font-weight: 400;
  }
  h4 {
    font-size: 24.19px;
    font-weight: 400;
  }
  h5 {
    font-size: 20.16px;
    font-weight: 400;
  }
  h6 {
    font-size: 16.8px;
    font-weight: 400;
  }

  [dir="rtl"] *{
    font-family: "IRANSans";
    font-size: 13px;
    --font-size-small: 10.83px;
    --font-size-extra-small: 9.03px;
  }
  [dir="rtl"] h1 {
    font-size: 38.82px;
    font-weight: 400;
  }
  [dir="rtl"] h2 {
    font-size: 32.35px;
    font-weight: 400;
  }
  [dir="rtl"] h3 {
    font-size: 26.96px;
    font-weight: 400;
  }
  [dir="rtl"] h4 {
    font-size: 22.46px;
    font-weight: 400;
  }
  [dir="rtl"] h5 {
    font-size: 18.72px;
    font-weight: 400;
  }
  [dir="rtl"] h6 {
    font-size: 15.6px;
    font-weight: 400;
  }
}
</style> -->
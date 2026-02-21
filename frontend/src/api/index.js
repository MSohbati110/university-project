const ISDEVELOPMODE = process.env.NODE_ENV !== 'production'

const django_api_url = 'http://localhost:8002'

export const base_url = ISDEVELOPMODE ? django_api_url : ''

export const axios = require('axios')
axios.defaults.headers.common = {
  Authorization: `Bearer ` + window.authtoken,
  'Content-Type': 'application/json'
}

export default {
  scrape(config) {
    return axios({
      method: 'post',
      url: `${base_url}/api/scrape/`,
      data: config
    })
  },
  scrapeSelectors() {
    return axios({
      method: 'get',
      url: `${base_url}/api/scrape/selectors/`,
    })
  },
  filteredResults(config) {
    return axios({
      method: 'post',
      url: `${base_url}/api/scrape/results/`,
      data: config
    })
  },
  scrapeJobs() {
    return axios({
      method: 'get',
      url: `${base_url}/api/scrape/jobs/`,
    })
  },
  toggleAutoScrape(config) {
    return axios({
      method: 'post',
      url: `${base_url}/api/scrape/jobs/toggle/`,
      data: config
    })
  },
}

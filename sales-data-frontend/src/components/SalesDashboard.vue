<template>
    <div class="container mx-auto p-4 bg-blue-950">
      <h1 class="text-3xl font-satoshi mb-6 text-center text-white">
        Sales Dashboard
      </h1>
      <div class="flex justify-between">
      <UserProfile />
      <button
        @click="logout"
        class="mt-4 w-20 h-10 bg-red-500 text-white p-1 rounded-sm hover:bg-red-600 text-sm font-satoshi"
      >
        Logout
      </button>
    </div>
      <div class="grid grid-cols-2 md:grid-cols-2 gap-6">
        <div class="space-y-6">
          <SalesForm @sale-added="fetchSales" :sales="sales" />
          <SaleSummary :sales="sales" />
          <SalesTips />
        </div>      
        <div class="space-y-6">   
          <SalesList :sales="sales" @sale-updated="loadSales" @sale-deleted="loadSales" />
          <PredictionChart :sales="sales" />  
        </div>
      </div>
      
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import SalesForm from './SalesForm.vue'
  import SalesList from './SalesList.vue'
  import PredictionChart from './PredictionChart.vue'
  import SaleSummary from './SaleSummary.vue'
  import UserProfile from './UserProfile.vue'
  import SalesTips from './SalesTips.vue'

  export default {
    components: { SalesForm, SalesList, PredictionChart, SaleSummary, UserProfile, SalesTips },
    data() {
      return {
        sales: []
      }
    },
    mounted() {
      this.loadSales()
    },
    methods: {
      async loadSales() {
        try {
          const response = await axios.get('http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com/sales', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
          this.sales = response.data
        } catch (err) {
          console.error('Error loading sales:', err)
        }
      },
      logout() {
        localStorage.removeItem('token')
        this.$router.push('/')
      }
    }
  }
  </script>
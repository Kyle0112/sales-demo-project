<template>
    <div class="bg-white p-3 rounded-md shadow-md h-100 mt-6 font-satoshi">
      <!-- Quick Stats -->
      <div class="mb-4">
        <h3 class="text-sm font-medium mb-2">Sales Stats</h3>
        <p class="text-xs">Total Sales: ${{ totalSales.toFixed(2) }}</p>
        <p class="text-xs">Avg Sale: ${{ averageSale.toFixed(2) }}</p>
      </div>
  
      <!-- Progress Bar -->
      <div class="mb-4">
        <h3 class="text-sm font-medium mb-2">Yearly Goal: $100,000</h3>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
          <div
            class="bg-green-500 h-2.5 rounded-full"
            :style="{ width: progressPercentage + '%' }"
          ></div>
        </div>
        <p class="text-xs mt-1">{{ progressPercentage.toFixed(1) }}% of goal</p>
      </div>
  
      <!-- Recent Sales -->
      <div v-if="recentSales.length" class="mb-4">
        <h3 class="text-sm font-medium mb-2">Recent Sales</h3>
        <table class="w-full border-collapse text-xs">
          <thead>
            <tr class="bg-gray-100">
              <th class="p-1 border">ID</th>
              <th class="p-1 border">Date</th>
              <th class="p-1 border">Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sale in recentSales" :key="sale.id">
              <td class="p-1 border">{{ sale.id }}</td>
              <td class="p-1 border">{{ sale.date }}</td>
              <td class="p-1 border">${{ sale.amount.toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  
  export default {
    props: ['sales'],
    computed: {
      totalSales() {
        return this.sales ? this.sales.reduce((sum, s) => sum + s.amount, 0) : 0
      },
      averageSale() {
        return this.sales && this.sales.length ? this.totalSales / this.sales.length : 0
      },
      progressPercentage() {
        const goal = 100000 // $100,000 goal
        return Math.min((this.totalSales / goal) * 100, 100) // Cap at 100%
      },
      recentSales() {
        return this.sales
          ? this.sales.slice().sort((a, b) => b.id - a.id).slice(0, 3)
          : []
      }
    }
  }
  </script>
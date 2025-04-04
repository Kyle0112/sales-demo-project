<template>
    <div class="bg-white p-4 rounded-lg shadow-lg mt-6">
      <h2 class="text-xl font-satoshi mb-4 text-grey">Sales Prediction</h2>
      <p v-if="prediction" class="mb-4 text-grey">Next Sale Prediction: <span class="font-satoshi text-grey">${{ prediction.toFixed(2) }}</span></p>
      <p v-else class="mb-4 text-gray-500 font-satoshi text-grey">{{ message }}</p>
      <LineChart v-if="chartData" :data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script>
  import config from '@/config.json';
  import axios from 'axios'
  import { Line } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)
  
  export default {
    components: { LineChart: Line },
    props: ['sales'],
    data() {
      return {
        prediction: null,
        plotUrl: '',
        message: 'Add at least 2 sales to see prediction',
        chartData: null,
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          
          plugins: { legend: { position: 'top' } },
          scales: {
            x: { 
              title: { 
                display: true, 
                text: 'Week',
                font: {} 
                } 
              },
            y: { title: { display: true, text: 'Sales ($)' } }
          }
        }
      }
    },
    watch: {
      sales: {
        immediate: true,
        handler() {
          this.loadPrediction()
        }
      }
    },
    methods: {
      async loadPrediction() {
        if (this.sales.length < 2) {
          this.chartData = null
          this.prediction = null
          this.message = 'Add at least 2 sales to see prediction'
          return
        }
        try {
          const response = await axios.get('http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com/predict', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
          if (response.data.predicted_next_sale) {
            this.prediction = response.data.predicted_next_sale
            const weeks = this.sales.map((_, i) => i)
            const amounts = this.sales.map(s => s.amount)
            this.chartData = {
              labels: [...weeks, weeks.length],
              datasets: [
                {
                  label: 'Past Sales',
                  data: [...amounts, null],
                  borderColor: 'blue',
                  fill: false,
                  tension: 0.1
                },
                {
                  label: 'Predicted',
                  data: [...amounts.map(() => null), this.prediction],
                  borderColor: 'red',
                  borderDash: [5, 5],
                  fill: false
                }
              ]
            }
          } else {
            this.message = response.data.message
            this.chartData = null
          }
        } catch (err) {
          console.error('Error loading prediction:', err)
          this.message = 'Error loading prediction'
        }
      }
    }
  }
  </script>
  
  <style scoped>
  canvas {
    max-height: 300px;
  }
  </style>
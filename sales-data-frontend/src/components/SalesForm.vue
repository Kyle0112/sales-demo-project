<template>
  <div class="bg-white p-3 rounded-md shadow-md h-56 mt-6 font-satoshi">
    <h2 class="text-lg font-medium mb-2 font-satoshi">Add New Sale</h2>
    <input
      v-model="date"
      type="date"
      class="w-full p-1 mb-1 border rounded-sm text-sm font-satoshi"
    >
    <input
      v-model="amount"
      type="number"
      placeholder="Amount"
      step="0.01"
      class="w-full p-1 mb-1 border rounded-sm text-sm font-satoshi"
    >
    <button
      @click="addSale"
      class="w-full bg-green-500 text-white p-1 rounded-sm hover:bg-green-600 text-sm font-satoshi"
    >
      Add Sale
    </button>
    <button @click="clearForm" class="w-full bg-gray-500 text-white p-1 rounded-sm hover:bg-gray-600 text-sm mt-3 font-satoshi">Clear</button>
    <p v-if="message" :class="messageClass" class="mt-1 text-xs">{{ message }}</p>

  </div>
</template>

<script>
import config from '@/config.json';
import axios from 'axios'

export default {
  props: ['sales'], // Add sales prop to access recent data
  data() {
    return {
      date: '',
      amount: '',
      message: '',
      isError: false
    }
  },
  computed: {
    messageClass() {
      return this.isError ? 'text-red-500' : 'text-green-500'
    },

  },
  methods: {
    async addSale() {
      if (!this.date || !this.amount) {
        this.showMessage('Please enter both date and amount', true)
        return
      }
      try {
        const response = await axios.post(`http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com/sales`, {
          date: this.date,
          amount: parseFloat(this.amount)
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        this.showMessage(response.data.message)
        this.date = ''
        this.amount = ''
        this.$emit('sale-added')
      } catch (err) {
        this.showMessage(err.response?.data?.message || 'Error adding sale', true)
      }
    },
    clearForm() { this.date = ''; this.amount = ''; this.message = '' },
    showMessage(text, isError = false) {
      this.message = text
      this.isError = isError
      setTimeout(() => (this.message = ''), 3000)
    }
  }
}
</script>
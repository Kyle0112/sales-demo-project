<template>
  <div class="bg-white p-4 rounded-lg shadow-lg mt-6">
    <h2 class="text-xl font-semibold mb-4">Sales History</h2>
    <div class="overflow-y-auto max-h-64">
      <table class="w-full border-collapse">
        <thead class="sticky top-0 bg-gray-100 z-10">
          <tr>
            <th class="p-2 border">ID</th>
            <th class="p-2 border cursor-pointer" @click="sortBy('date')">
              Date
              <span v-if="sortKey === 'date'" class="ml-1">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th class="p-2 border cursor-pointer" @click="sortBy('amount')">
              Amount ($)
              <span v-if="sortKey === 'amount'" class="ml-1">
                {{ sortDirection === 'asc' ? '↑' : '↓' }}
              </span>
            </th>
            <th class="p-2 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sale in sortedSales" :key="sale.id" class="hover:bg-gray-50">
            <td class="p-2 border">{{ sale.id }}</td>
            <td class="p-2 border">
              <span v-if="!editing[sale.id]">{{ sale.date }}</span>
              <input v-else v-model="editSale[sale.id].date" type="date" class="w-full p-1 border rounded">
            </td>
            <td class="p-2 border">
              <span v-if="!editing[sale.id]">${{ sale.amount.toFixed(2) }}</span>
              <input v-else v-model="editSale[sale.id].amount" type="number" step="0.01" class="w-full p-1 border rounded">
            </td>
            <td class="p-2 border">
              <button v-if="!editing[sale.id]" @click="startEdit(sale)" class="bg-yellow-500 text-white p-1 rounded hover:bg-yellow-600">Edit</button>
              <button v-else @click="updateSale(sale.id)" class="bg-blue-500 text-white p-1 rounded hover:bg-blue-600" :disabled="!isValidEdit(sale.id)">Save</button>
              <button @click="deleteSale(sale.id)" class="bg-red-500 text-white p-1 rounded hover:bg-red-600 ml-2">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['sales'],
  data() {
    return {
      editing: {},
      editSale: {},
      sortKey: '',        // Current sort column ('date' or 'amount')
      sortDirection: 'asc' // 'asc' or 'desc'
    }
  },
  computed: {
    sortedSales() {
      if (!this.sortKey) return this.sales // Default: unsorted

      const sorted = [...this.sales] // Clone array to avoid mutating prop
      sorted.sort((a, b) => {
        if (this.sortKey === 'date') {
          const dateA = new Date(a.date)
          const dateB = new Date(b.date)
          return this.sortDirection === 'asc' ? dateA - dateB : dateB - dateA
        } else if (this.sortKey === 'amount') {
          return this.sortDirection === 'asc' ? a.amount - b.amount : b.amount - a.amount
        }
        return 0
      })
      return sorted
    }
  },
  methods: {
    sortBy(key) {
      if (this.sortKey === key) {
        // Toggle direction if same key
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        // New key, start with ascending (Date: oldest first, Amount: smallest first)
        this.sortKey = key
        this.sortDirection = 'asc'
      }
    },
    startEdit(sale) {
      const today = new Date().toISOString().split('T')[0] // Current date in YYYY-MM-DD
      this.editing[sale.id] = true
      this.editSale[sale.id] = { 
        date: sale.date || today, // Use existing date or today
        amount: sale.amount 
      }
    },
    isValidEdit(id) {
      const edit = this.editSale[id]
      return edit && edit.date && edit.amount !== '' && edit.amount !== null // Non-empty check
    },
    async updateSale(id) {
      if (!this.isValidEdit(id)) {
        alert('Date and Amount must be filled before saving.')
        return
      }
      try {
        const response = await axios.put(`http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com/sales/${id}`, this.editSale[id], {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
        this.editing[id] = false
        this.$emit('sale-updated')
      } catch (err) {
        console.error('Error updating sale:', err)
      }
    },
    async deleteSale(id) {
      if (confirm('Are you sure you want to delete this sale?')) {
        try {
          await axios.delete(`http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com/sales/${id}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          })
          this.$emit('sale-deleted')
        } catch (err) {
          console.error('Error deleting sale:', err)
        }
      }
    }
  }
}
</script>
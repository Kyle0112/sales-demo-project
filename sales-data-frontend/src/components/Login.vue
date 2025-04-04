<template>
  <div class="flex items-center justify-center min-h-screen">
    <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
      <h1 class="text-2xl font-bold mb-4 text-center">Login</h1>
      
      <input v-model="username" type="text" placeholder="Username" class="w-full p-2 mb-4 border rounded">
      <input v-model="password" type="password" placeholder="Password" class="w-full p-2 mb-4 border rounded">
      <button @click="login" class="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600">Login</button>
      <p v-if="error" class="text-red-500 mt-2 text-center">{{ error }}</p>
    </div>
  </div>
</template>
<script>
import config from '@/config.json';
import axios from 'axios'

export default {
  data() {
    return {
      username: 'user',
      password: 'pass',
      error: ''
    }
  },
  methods: {
    async login() {
      const url = `http://sales-demo-env.eba-3eudkpej.ap-southeast-2.elasticbeanstalk.com/login`
      console.log('Requesting:', url) // Debug
      try {
        const response = await axios.post(url, {
          username: this.username,
          password: this.password
        }, {
          headers: { 'Content-Type': 'application/json' }
        })
        localStorage.setItem('token', response.data.token)
        this.$router.push('/dashboard')
      } catch (err) {
        this.error = err.response?.data?.message || 'Login failed'
        console.error('Login error:', err.message, err.response)
      }
    }
  }
}
</script>
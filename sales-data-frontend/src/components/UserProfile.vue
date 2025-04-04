<template>
    <div class="bg-blue-950 p-3 rounded-md w-64">
      <div class="flex items-center space-x-4">
        <!-- Circular Profile Picture -->
        <div class="w-12 h-12 rounded-full overflow-hidden bg-gray-200 flex-shrink-0">
          <div class="w-full h-full flex items-center justify-center text-gray-500 text-xl">
            {{ username.charAt(0).toUpperCase() }}
          </div>
        </div>
        <!-- Placeholder User Info -->
        <div>
          <p class="text-s text-white font-satoshi">Logged in as: {{ username }}</p>
        </div>
        <div>
            
        </div>
      </div>  
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: 'Guest' // Static placeholder username
      }
    },
    methods: {
      
    }
  }
  </script>
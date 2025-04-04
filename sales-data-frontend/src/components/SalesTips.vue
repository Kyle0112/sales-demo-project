<template>
    <div class="bg-white p-3 rounded-md shadow-md w-full h-42">
      <h3 class="text-sm font-medium mb-2 text-gray-800">Sales Tips</h3>
      <div class="mb-4">
        <p class="text-xs text-gray-700 font-semibold">{{ currentTip.title }}</p>
        <p class="text-xs text-gray-600 mt-1">{{ currentTip.description }}</p>
      </div>
      <div class="mb-4">
        <p class="text-xs text-gray-700">Tip of the Day:</p>
        <ul class="text-xs text-gray-600 list-disc pl-4">
          <li>Follow up with leads within 24 hours.</li>
          <li>Highlight benefits, not just features.</li>
          <li>Track your progress daily!</li>
        </ul>
      </div>
     
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        tips: [
          { title: 'Know Your Customer', description: 'Tailor your pitch to their needs.' },
          { title: 'Stay Persistent', description: 'Follow-ups can turn a no into a yes.' },
          { title: 'Use Data', description: 'Leverage sales trends to close deals.' },
          { title: 'Smile!', description: 'A positive attitude goes a long way.' }
        ],
        currentTipIndex: 0
      }
    },
    computed: {
      currentTip() {
        return this.tips[this.currentTipIndex]
      }
    },
    mounted() {
      // Rotate tips every 10 seconds
      setInterval(() => {
        this.currentTipIndex = (this.currentTipIndex + 1) % this.tips.length
      }, 10000)
    },
    methods: {
      
    }
  }
  </script>
<template>
  <div>
    <input v-model="query" @keyup.enter="searchSong" placeholder="Search for a song">
    <button @click="searchSong">Search</button>
    <div v-if="songs.length">
      <ul>
        <li v-for="song in songs" :key="song.id">{{ song.title }} by {{ song.artist }}</li>
      </ul>
    </div>
    <div v-else>
      <p>No songs found.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      songs: []
    }
  },
  methods: {
    async searchSong() {
      if (this.query.trim() === '') {
        this.songs = []
        return
      }
      const response = await fetch(`/search/?q=${this.query}`)
      this.songs = await response.json()
    }
  }
}
</script>

<style>

</style>
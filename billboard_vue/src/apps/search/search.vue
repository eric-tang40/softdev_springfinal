<template>
  <div>
    <h1>Search for a Song</h1>
    <input v-model="query" @keyup.enter="searchSong" placeholder="Search for a song" />
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
        this.songs = [];
        return;
      }
      try {
        const response = await fetch(`/rankings/search/?q=${this.query.trim()}`);
        
        if (response.ok) {
          // Parse the JSON response (Error here)
          const jsonResponse = await response.json();

          // Log the response to ensure it's correct
          console.log("JSON Response:", jsonResponse);
          this.songs = jsonResponse;
          console.log("Songs Array:", this.songs);
        } else {
          console.error('Failed to fetch songs');
          
          this.songs = [];
        }
      } catch (error) {
        console.error('An error occurred:', error);
        // this.songs = [];
      }
    }
  }
}
</script>

<style scoped>
h1 {
  font-size: 24px;
  margin-bottom: 20px;
}
input {
  padding: 10px;
  font-size: 16px;
  margin-right: 10px;
}
button {
  padding: 10px;
  font-size: 16px;
}
ul {
  margin-top: 20px;
  list-style: none;
  padding: 0;
}
li {
  padding: 5px 0;
}
p {
  margin-top: 20px;
  font-size: 16px;
  color: gray;
}
</style>

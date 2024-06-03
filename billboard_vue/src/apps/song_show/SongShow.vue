<template>
  <div>
    <h1>{{ song.title }} by {{ song.artist }}</h1>
    <button @click="toggleFavorite">
      {{ isFavorited ? 'Remove from Favorites' : 'Add to Favorites' }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'SongShow',
  props: [
    songId: Number,
    isFavorited: Boolean
  ],
  data() {
    return {
      song: {},
      csrf_token: ext_csrf_token,
    };
  },
  methods: {
    fetchSongDetails() {
      fetch(`/songs/${this.songId}/`)
        .then(response => response.json())
        .then(data => {
          this.song = data;
        })
        .catch(error => console.error('Error:', error));
    },
    toggleFavorite() {
      fetch(`/songs/${this.songId}/toggle_favorites/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.csrf_token,
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        this.isFavorited = !this.isFavorited;
        alert(`Song has been ${data.status}.`);
      })
      .catch(error => console.error('Error:', error));
    }
  },
  mounted() {
    this.fetchSongDetails();
  }
}
</script>

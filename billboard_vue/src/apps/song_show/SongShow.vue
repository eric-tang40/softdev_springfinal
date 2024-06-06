<template>
  <div>
    <h1>{{ songData.title }}</h1>
    <div>
      Artist: {{ songData.artist }} <br>
      Album: {{ songData.album_name }} <br>
      Label: {{ songData.label }}
    </div>
    <button @click="toggleFavorite">
      {{ isFavorited ? 'Remove from Favorites' : 'Add to Favorites' }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'SongShow',
  data() {
    return {
      csrf_token: ext_csrf_token,
      songData: ext_songData,
      isFavorited: ext_songData.favorite,
    }
  },
  methods: {
    toggleFavorite() {
      fetch(`/rankings/songs/${this.songData.id}/toggle_favorites/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.csrf_token,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(response.status)
          }
          return response.json()
        })
        .then((data) => {
          this.isFavorited = data.status == 'added' ? 1 : 0
          alert(`Song has been ${data.status}.`)
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>

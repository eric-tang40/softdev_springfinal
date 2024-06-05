<template>
  <div>
    <h1>{{ songData.title }} by {{ songData.artist }}</h1>
    <button @click="toggleFavorite">
      {{ isFavorited ? 'Remove from Favorites' : 'Add to Favorites' }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'SongShow',
  // props: {
  //   songId: Number,
  //   isFavorited: Boolean
  // },
  data() {
    return {
      csrf_token: ext_csrf_token,
      //songId: ext_songId,
      songData: ext_songData,
      isFavorited: 0,
      isFavorited: false,
    };
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
      .then(response => {
        if (!response.ok) {
          throw new Error(response.status);
        }
        return response.json();
      })
      .then(data => {
        this.isFavorited = data.status == 'added' ? 1 : 0;
        alert(`Song has been ${data.status}.`);
      })
      .catch(error => {
        console.error(error);
      });
    }
  },
}
</script>

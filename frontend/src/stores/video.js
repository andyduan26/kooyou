import { defineStore } from 'pinia'

export const useVideoStore = defineStore('video', {
  state: () => ({
    history: JSON.parse(localStorage.getItem('kooyou-history') || '[]'),
    favorites: JSON.parse(localStorage.getItem('kooyou-favorites') || '[]')
  }),
  actions: {
    remember(video) {
      this.history = [video, ...this.history.filter((item) => item.id !== video.id)].slice(0, 30)
      localStorage.setItem('kooyou-history', JSON.stringify(this.history))
    },
    saveFavorite(video) {
      this.favorites = [video, ...this.favorites.filter((item) => item.id !== video.id)]
      localStorage.setItem('kooyou-favorites', JSON.stringify(this.favorites))
    },
    removeFavorite(id) {
      this.favorites = this.favorites.filter((item) => item.id !== id)
      localStorage.setItem('kooyou-favorites', JSON.stringify(this.favorites))
    }
  }
})

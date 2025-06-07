import { create } from 'zustand';

export const useAppStore = create((set) => ({
  currentPhoto: null,
  location: null,
  searchResults: null,
  isLoading: false,
  error: null,
  
  setCurrentPhoto: (photo) => set({ currentPhoto: photo }),
  setLocation: (location) => set({ location: location }),
  setSearchResults: (results) => set({ searchResults: results }),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error: error }),
  clearError: () => set({ error: null }),
})); 
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // IMPORTANT: Replace 'repo-name' with your actual GitHub repository name
  // Example: if your repo is github.com/josh/lumber-dash, this should be '/lumber-dash/'
  base: '/YOUR_REPO_NAME_HERE/', 
})

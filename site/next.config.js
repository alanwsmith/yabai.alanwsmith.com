// next.config.js
const withPlugins = require('next-compose-plugins')
const optimizedImages = require('next-optimized-images')

module.exports = withPlugins([
  [
    optimizedImages,
    {
      handleImages: ['jpeg', 'png', 'svg', 'webp', 'gif'],
      /* config for next-optimized-images */
    },
  ],

  { reactStrictMode: true },
])

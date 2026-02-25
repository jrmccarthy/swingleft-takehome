/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/api/:path*',
        destination:
          process.env.NODE_ENV === 'development'
            ? 'http://172.233.223.212:5328/api/:path*'
            : '/api/',
      },
    ]
  },
}

module.exports = nextConfig

import type { Core } from '@strapi/strapi';

const config = ({ env }: Core.Config.Shared.ConfigParams): Core.Config.Server => ({
  host: env('HOST', '0.0.0.0'),
  port: env.int('PORT', 1337),
  url: env('STRAPI_URL', 'https://icerik-yonetimi.onrender.com'), // İnternet adresini buraya çaktık şefim!
  proxy: true, // Render arkasında çalıştığı için bu şart
  app: {
    keys: env.array('APP_KEYS'),
  },
});

export default config;
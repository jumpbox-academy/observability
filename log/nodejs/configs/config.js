const dotenv = require('dotenv');

dotenv.config();

module.exports = {
  API_SECRET: process.env.API_SECRET,
  LOG_LEVEL:  process.env.LOG_LEVEL,
  // add any other environment variables here...
};

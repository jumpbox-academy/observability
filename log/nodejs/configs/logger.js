const winston = require('winston');
const moment = require('moment');
const config = require('./config');

const logLevel = config.LOG_LEVEL;

const logFormat = winston.format.printf(({ level, message, label, meta, ...data }) => {
  return JSON.stringify({
    timestamp: moment().format(),
    level: level,
    message: message,
    service: label,
    meta_data: meta,
    data: data
  });
});

const logger = winston.createLogger({
  level: logLevel,
  format: winston.format.combine(
    logFormat,
    winston.format.prettyPrint()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console());
}

module.exports = logger;

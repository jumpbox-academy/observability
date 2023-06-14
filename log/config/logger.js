const winston = require('winston');



const myFormat = winston.format.printf(
  ({ timestamp, level, service, traceId, message, data }) => {
  return JSON.stringify({ 
    timestamp, 
    level, 
    message, 
    service, 
    traceId, 
    data 
  });
});

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    myFormat
),
  transports: [
    new winston.transports.Console()
  ]
});




if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple(),
  }));
}

module.exports = logger;
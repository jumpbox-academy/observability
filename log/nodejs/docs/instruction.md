# Instruction
1. create the project 
```zsh
npx create-next-app@latest nodejs
```
2. fill the iteractive terminal
```zsh
✔ Would you like to use TypeScript with this project? … No / Yes
✔ Would you like to use ESLint with this project? … No / Yes
✔ Would you like to use Tailwind CSS with this project? … No / Yes
✔ Would you like to use `src/` directory with this project? … No / Yes
✔ Use App Router (recommended)? … No / Yes
✔ Would you like to customize the default import alias? … No / Yes
```
3. install library for json log format and dotenv
```zsh
npm install winston && npm install moment && npm install dotenv
```
4. create environment config and logger
```
mkdir -p configs && touch configs/config.js && touch configs/logger.js
```
5. place this to config.js
```js
const dotenv = require('dotenv');

dotenv.config();

module.exports = {
  API_SECRET: process.env.API_SECRET,
  // add any other environment variables here...
};
```

6. place this to logger.js
```js
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
```

7. create route and api
```
mkdir -p pages/api && touch pages/api/hello.js
```

8. place this to hello.js
```js
const logger = require('../../configs/logger');
const config = require('../../configs/config');

export default function handler(req, res) {
    const secret = config.API_SECRET;

    const response = {
        timestamp: new Date().toISOString(),
        message: `Secret is: ${secret}`,
        level: "INFO",
        meta_data: {
            // add any metadata here
            service: "web-api",
            error_code: "ECUS001", 
            error_msg: "Invalid API Token", 
            user_name: "JoJo", 
            user_id: "C168"
        },
        data: {
            // add any additional data here
            key_1: "value", 
            key_2: "value-2", 
            key_3: "value-3"
        }
    };
    logger.info(response);
    logger.debug("message debug");
    logger.error("message error");
    res.status(200).json(response);
}
```
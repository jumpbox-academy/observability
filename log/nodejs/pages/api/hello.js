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
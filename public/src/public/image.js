const http = require('http');
const https = require('https');


/**
 * 
 * @param {string} url 
 */
async function url_tob64(url) {
    const _h_protocol = url.startsWith('https') ? https : http;

    return new Promise((resolve, reject) => {
        _h_protocol.get(url, (res) => {
            let data = [];
            let len_ = parseInt(res.headers['content-length']);
    
            res.on('data', (chunk) => {
                data.push(chunk);
            })
    
    
            res.on('end', () => {
                resolve(
                    Buffer.concat(data, len_).toString('base64')
                )
            });
        })
    })
}

module.exports = url_tob64;
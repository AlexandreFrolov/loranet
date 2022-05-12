const http = require("http");
const hostname = "192.168.0.19";
const port = 8000;
const fs = require('fs'); 

const server = http.createServer((req, res) => {
   res.writeHead(200, {'Content-Type': 'Application/json; charset=utf-8'});
   let rawdata = fs.readFileSync('/home/pi/py/hosts_data.json'); 
   let host_data = JSON.parse(rawdata); 
   console.log(host_data);    
   res.end(JSON.stringify(host_data));
});

server.listen(port, hostname, () => {
   console.log(`Server running at http://${hostname}:${port}/`);
})


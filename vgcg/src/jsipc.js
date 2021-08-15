//interfacing with frontend 
const express = require("express");
const http = require("http");
const FIFO = require("fifo-js");
const fs = require("fs");

const app = express();
const bodyParser = require("body-parser")
const {spawn, fork } = require("child_process");

const IPC_PATH_A = "pipe_a";
const IPC_PATH_B = "pipe_b";








//initiate express direction at current path
app.use( express.static(__dirname));
//when get request is performed, return the index.html document for client render
app.get("/", (req, res) => { res.sendFile(__dirname + "/index.html");});


     


//spawn process of make first in first out pipe, according to IPC_PATH_B
function verify_payload(index, object) {
  if (object[index]) return true;
  else return false;
}
const fifo_b = spawn("mkfifo", [IPC_PATH_B]);
//on exit, gather status and clean, which launches the ipc (seems counter intuitive, but these are attached to the pipe, basically)
fifo_b.on("exit", function (status) {
  const fd   = fs.openSync(IPC_PATH_B, 'r+');
      let fifoRs = fs.createReadStream(null, { fd });
      let fifoWs = fs.createWriteStream(IPC_PATH_A);

  app.post("/api/update", bodyParser.json(), (req, res) => { //when req hits api endpoint update, log data packet and write to pipe
    
    console.log("NODE [UPDATE]: ----Send data packet Update----");
    if (JSON.stringify(req.body.data).length != 2){
        console.log(`NODE [UPDATE]: SENDING REQUEST ${JSON.stringify(req.body)}`);
        fifoWs.write(`${JSON.stringify(req.body)}`);
        setTimeout(() => { console.log("waited")}, 200);

       fifoRs.once('data', data => { // only read this once upon post
        res.status(201).json({msg: data.toString()});
        console.log("NODE [UPDATE]: ending transaction")
        }           
      )
      setTimeout(() => {console.log("NODE: stalling")}, 200);


    console.log("NODE [UPDATE]: end send data packet");
  
    }
  });






  app.post("/api/logging", bodyParser.json(), (req, res) => {
    console.log("NODE   [LOGGING]: ", req.body.data);
    res.status(201).json({msg: "OKAY"}); // just to ensure it doesnt wait forever

  console.log("NODE   [LOGGING]:  should have sent now ");
  });

  //when req hits api endpoint update, log data packet and write to pipe
  app.post("/api/model", bodyParser.json(), (req, res) => { //when req hits api endpoint update, log data packet and write to pipe
    console.log("NODE [MODEL]: ---- Send data packet Model ----");
    
    console.log(JSON.stringify(req.body.data));


    if (JSON.stringify(req.body).length != 2) {
      console.log(`NODE [MODEL]: inside sending of packet, ${req.body}`);
      var X = JSON.stringify(req.body);
    
      fifoWs.write(`${X}`);
        setTimeout(() => { console.log("NODE [MODEL]: waited")}, 200);
       fifoRs.once('data', data => { // only read this once upon post
        console.log('NODE [MODEL]: ----- Received packet -----');
        console.log(data.toString());
        res.status(201).json({msg: data.toString()});
        console.log("NODE [MODEL]: ending transaction")
        }           
      )
      setTimeout(() => {console.log("NODE [MODEL]: stalled")}, 2000);
      console.log("NODE [MODEL]: outer layer of async calls, returning ouput")
    console.log(req.body);
    console.log("NODE [MODEL]: end send data packet"); }
  });

 app.listen(3001); // this could be passed by arg, is the localhost location as lient for this server.
console.log("NODE [GLOBAL]: listening");
});
console.log("end"); // exit


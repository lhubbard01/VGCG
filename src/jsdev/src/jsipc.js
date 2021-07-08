//interfacing with frontend 
//Adapted from https://levelup.gitconnected.com/inter-process-communication-between-node-js-and-python-2e9c4fda928d
const express = require("express");
const http = require("http");
const FIFO = require("fifo-js");

const app = express();
const bodyParser = require("body-parser")
//app.use(bodyParser.json());
//app.get("/", (req, res) => { res.sendFile(__dirname + "/d.html");});
//File system imports for IPC 
const fs = require("fs");
const {spawn, fork } = require("child_process");

const IPC_PATH_A = "pipe_a";
const IPC_PATH_B = "pipe_b";








//initiate express direction at current path
app.use( express.static(__dirname));
//when get request is performed, return the index.html document for client render
app.get("/", (req, res) => { res.sendFile(__dirname + "/index.html");});


     


//spawn process of make first in first out pipe, according to IPC_PATH_B
const fifo_b = spawn("mkfifo", [IPC_PATH_B]);
//on exit, gather status and clean, which launches the ipc (seems counter intuitive, but these are attached to the pipe, basically)
fifo_b.on("exit", function (status) {
  const fd   = fs.openSync(IPC_PATH_B, 'r+');
      let fifoRs = fs.createReadStream(null, { fd });
      let fifoWs = fs.createWriteStream(IPC_PATH_A);
     /*
        setInterval(() => {
        console.log('-----   Send packet   -----');
        fifoWs.write(`${new Date().toISOString()}`);
    }, 1000);  // Write data at 1 second interval*/
  

  app.post("/api/update", bodyParser.json(), (req, res) => { //when req hits api endpoint update, log data packet and write to pipe
    console.log("---- Send data packet ----");
        //fifoWs.write(`${new Date().toISOString()}`);
        fifoWs.write(`${req.body.data}`);
        setTimeout(() => { console.log("waited")}, 200);
            /*console.log('----- Received packet -----');
            console.log(data.toString());
            console.log(data);
            console.log("running");
            return data;
          })*/
       fifoRs.once('data', data => { // only read this once upon post
        //sent_time = new Date(data.toString());
        console.log('----- Received packet -----');
        console.log(data.toString());
        /*console.log('    Date   : ' + data.toString());
        console.log('    Latency: ' + latency.toString() + ' ms');*/
        console.log("running");
        res.status(201).json({msg: data.toString()});
        console.log("ending transaction")
        }           
      )
      setTimeout(() => {console.log("stalling")}, 200);
      console.log("outer layer of async calls, returning ouput")
        /*console.log('    Date   : ' + data.toString());
        console.log('    Latency: ' + latency.toString() + ' ms');*/
    //fifoWr.write( () => {`${new Date().toISOString()}`});
    //console.log("---- Send data packet ----");
    //fifoWr.write(`${new Date().toISOString()}`);
    console.log(req.body);
    //res.status(200).json({msg: "logged"});
    console.log("end send data packet");
  });
 app.listen(3001); // this could be passed by arg, is the localhost location as lient for this server.
console.log("listening");
});
  /*let fifoWr = fs.createWriteStream(IPC_PATH_A);
  let fifoRd = new FIFO(IPC_PATH_B);
  fifoRd.read(data => {
    now_time = new Date();
    sent_time = new Date(data.toString());
      let latency = now_time - sent_time;
      console.log("---- Recieved data packet ----");
      console.log("Latency: " + latency.toString() + "ms");
  }
);

*/
//let fifoRs = fs.createReadStream(fd);
  /*setInterval( () => { */
  /*}, 1000);*/
console.log("end"); // exit


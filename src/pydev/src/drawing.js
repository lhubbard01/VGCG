//GEOMETRIC PRIMITIVES


var globalN = 1;
var curr = 0;
var drawablecb = genRect;

class Line{
  constructor(x1,y1,x2,y2){
    this.pointA = new Point(x1,y1);
    this.pointB = new Point(x2,y2);
  }
}
class Rect{
  constructor(x,y,size,color){
    this.x = x;
    this.y = y;
    this.size = size;
    this.color = color;
  
    this.render = this.render.bind(this);
  }
  render(){

    let divrect = document.createElement("div");
    
    //divrect.jsname = this;
    divrect.id = globalN;
    divrect.innerHTML="hello";
    divrect.style.border= "1px solid black";
    globalN++;
    divrect.style.position = "absolute";
    divrect.style.left = this.x+"px";
    divrect.style.top = this.y+"px";
    divrect.style.width = this.size+"px";
    divrect.style.height = this.size+"px";
    divrect.style.zIndex = "-1";
    divrect.style.background = this.color;
    document.body.appendChild(divrect);
  }
}

function genRect(ev){
  var r = new Rect(ev.clientX, ev.clientY, 200, "red");
  r.render();
  LOG(r);
}



var x = genRect;
LOG(x);



class Point{
  constructor(x,y){
    this.x = x;
    this.y = y;
  }
};


var PointA = new Point(0,0);
var PointB = new Point(100,100);
var globalSearch = {};



//CALLBACKS FOR CLICK HANDLING
function declarecb(){
}
/*function connectcb (){
  //It is assummed 
  //Point A and Point B will be initialized at loadtime, and will be viable for search
  let nameA = search(PointA)
  let nameB = search(PointB);
  if (!nameA || !nameB){
    LOG("modules not c=found for conneciton");
  }
  else{
    //let connect = {In:{Name: nameA.Name, count: count}, Out:{Name:nameB.Name, count: count}};
    send(connect);
    LOG("sent " + JSON.stringify(connect))
  }
}
*/

//STATE MANAGEMENT
function search(PointX){
  globalSearch.get();
}
var p1 = 0;
var p2 = 0;

function connect(e,th){
  if (!p1){
    p1 = new Point(e.clientX, e.clientY);
  }
  else if (!p2){
    p2 = new Point(e.clientX, e.clientY);
    let out= new Line(p1.x, p1.y, p2.x, p2.y);
    


    LOG(out);
    p1 = null;
    p2 = null;
  
  return out;
  }
}
function input(ev,th){
  let data = {isParametric: "off", isNative: "off", mType: null, Name: "MainInput"};
  return data;
}


function linear(ev,th){
  let data = {isParametric: "on",
  isNative: "on",
  mType:"Linear",
  Name: "A"};
  return data;
}

function relu(ev,th){
  let data = {isParametric: "off",
  isNative:"on",
  mType:"ReLU",
  name: "relu1"
  };
  return data;
}
   
//DOM STATE MANAGEMENT
function addField(object, text){
  object.addTextNode(text);
}

function createDiv(fields){
    var  divlocal = document.createElement("DIV");
    //TODO add check for divlocal i.e. only add new popup if divlocal null
    for (let i = 0; i < fields.length; ++i){
      addField(divlocal,fields[i]);
  }
    LOG(divlocal);
}

function popUpDesc(){
  var newPopup = new Rect(atClick.x, atClick.y, DEFAULT_SIZE, WHITE);
  let maybeModule = search(atClick); //search global table of objects for a module at this location
  if (maybeModule){
    let fields = maybeModule.fields; // grab the associated fields
    let out = createDiv(fields); //for consturction within createDiv, as a popup
    body.appendChild(out);
  }
  else{
    LOG("no module found at this location"); // could be more descriptive
  }
}
var drawablecbN = "rect";
var idToCB = {

  "relu": relu,
  "connect": connect,
  "rect": genRect,
  "bilinear": linear,
  "linear": linear,
  "input": input,
};//setTimeout(300, ()=>{document.getElementsByTagName("NAV").item(0).addEventListener("click", (e));});//(t) => { varidToCB[drawablecbN](t);});});
function drawClick(ev){
  LOG(new String(ev), drawablecbN);
  idToCB[drawablecbN](ev);
}
setTimeout(300, ()=>{document.body.addEventListener("click", idToCB[drawableN]);});


function selection(t){
  LOG("selection", t.id);
  
  console.log(typeof(t.id));
  drawablecbN = new String(t.id);
  console.log(drawablecbN);



  console.log(new String(idToCB));
  console.log(new String(idToCB[t.id]));
  console.log("drawable callback name", new String(drawablecbN), "drawable id selected", new String(t.id));
  LOG(t, idToCB[t.id]);

  //LOG(drawablecbN, idToCB[drawablecbN]);
}
 
async function LOG(){
  var data_in = "";
  for (let i = 0; i < arguments.length; i++)
    data_in += " " + new String(arguments[i]);

  console.log("logging", data_in);
  const data = JSON.stringify({data: data_in});
   const options = {
     method: "POST",
     headers : {"Content-Type":"application/json"},
     body: data
    };

  
  console.log("options logging", JSON.stringify(options));
  const res = await fetch("/api/logging", options)
      .then(res => res.json())
      .catch(err => console.error(err));
  console.log("completed logging request");
 };
  /*fLOG(drawablecb);
    drawable.removeEventListener("click", drawablecb);*/


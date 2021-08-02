//GEOMETRIC PRIMITIVES
var verbose = 3;
var globalN = 1;
var curr = 0;
var drawablecb = genRect;

//DIRECT DOM RENDER VIA SVG
class Line{
  constructor(x1,y1,x2,y2){
    LOG("making line!");
    this.pointA = new Point(x1,y1);
    this.pointB = new Point(x2,y2);
    this.render = this.render.bind(this);

  }
  render(){
    var svg_render = document.createElement("svg");
    if (verbose > 0)
      LOG("render line!");
    svg_render.innerHTML = "<line x1=" + this.pointA.x.toString() + "\" y=\"" + this.pointA.y.toString()
      + "\" x2 = \"" + this.pointB.x.toString() + "\" y2 = \"" + this.pointB.y.toString() 
      + "\" stroke=\"black\" />"; 

    svg_render.className="SVG_Conn";
    svg_render.position = "absolute";
    document.body.appendChild(svg_render);
  }


};


//CONTAINER CLASS FOR DIRECT DOM RENDER // holds state for the modules locally
class Rect{
  constructor(x,y,size,color, title, Name){
    this.x = x;
    this.y = y;
    this.size = size;
    this.color = color;
    this.title = title;
    this.Name  = Name;
  
    this.render = this.render.bind(this);

  }
  

  render(){
    let divrect = document.createElement("div");
    divrect.className = "moduleDiv";
    
    //divrect.jsname = this;
    
    divrect.id = this.Name;


    divrect.innerHTML=this.title;
    divrect.style.border= "1px solid black";
    
    divrect.style.position = "absolute";

    divrect.style.left   = this.x+"px";
    divrect.style.top    = this.y+"px";

    divrect.style.width  = this.size+"px";
    divrect.style.height = this.size+"px";

    divrect.style.zIndex = "-1";
    divrect.style.background = this.color;

    document.body.appendChild(divrect);
  }
}




function genRect(ev, title, Name)
{
  var r = new Rect(ev.clientX, ev.clientY, 200, "red", title, Name);
  r.render();
  LOG(r);
  return r;
}


function checkLoc(ev, obj)
{
  // used to gater the bounding box of the div, there might be a better way to do htis
  if ((
  ((ev.clientX > obj.offsetLeft) && (ev.clientX <= (obj.offsetLeft + obj.offsetWidth)))
      && ((ev.clientY > obj.offsetTop ) && (ev.clientY <= (obj.offsetTop + obj.offsetHeight)))
  ) )
    return true;
  else return false;
}


function checkIfRect(ev)
{
  //checks for if an element is being clicked on
  module_rects= document.getElementsByClassName("moduleDiv");
  for (let i = 0; i < module_rects.length; ++i){

    let localrect = module_rects.item(i);

    if (checkLoc(ev, localrect)){
      return {found: true, rect: localrect};
    }

  }
  return {found: false, rect: null};
}

function remove(ev){
  // if element is clicked, remove it from dom and server
  var maybeEl = checkIfRect(ev);
  if ( maybeEl.found )
  {
    
    
    if (verbose>0)
      LOG("removing");
    send(maybeEl.rect.id, "remove");
    maybeEl.rect.remove();
    return true;
  }
  return false;

}





var p1 = null;var p2 = null;
function connect(ev)
{
  //check if a rectangle is beneath the click. if so, and if clicked previously and rect stored, announce connection to server
  var maybeEl = checkIfRect(ev);

  LOG(maybeEl);
  if (maybeEl.found)
  {
      if (!p1){

        if (verbose > 1)
          LOG("part 1 conn");
        p1 = new Point(ev.clientX, ev.clientY);
        connEl = maybeEl.rect;
      }
      else if (!p2){ 
        if ( verbose > 1) 
          LOG("part 2 conn");
        p2 = new Point(ev.clientX, ev.clientY);
        let out = new Line(p1.x, p1.y, p2.x, p2.y);
        LOG(out);
        LOG(connEl);
        LOG(maybeEl);
        let data = {
          from:{
            Name: connEl.id, 
            count: 50
          }, 
          to:{
            Name: maybeEl.rect.id,
            count: 50
          }
        };


        LOG(JSON.stringify(data));
        LOG("sending!");
        out.render();
        send(data, "conn");
        connEl = null; p1 = null; p2 = null; maybeEl = null;
      }

  }

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


function input(ev,th){
  let data = {isParametric: false, isNative: false, mType: null, Name: "MainInput"};
  return data;
}

function linear(ev){
  var name = "A" + globalN;
  globalN++;
  
  let rect=genRect(ev, "Linear", name);

  LOG(rect);
  let data = {isParametric: true,
    isNative: true,
    mType:"Linear",
    
    Name: rect.Name,
    hyperp: JSON.stringify({in_features: 100, out_features: 50})
  };
  send(data, "add");



  console.log("FROM LINEAR", ev);
  return data;
}


function Output(ev, th){
  let data = {isParametric: false, isNative: false, Name: "output"};
  console.log("FROM OUTPUT", th);
  genRect(ev, "Output");
  send(data, "add");
  return data;
 } 








async function send(data_in, signal_type)
{

  const data = JSON.stringify({
    data: data_in,
    route: "model",
    signal_type: signal_type
  });
  
  if (verbose > 0)
    LOG(data);

   const options = {
     method: "POST",
     headers : {"Content-Type":"application/json"},
     body: data
    };

  if (verbose > 1)  
    console.log("options logging", JSON.stringify(options));
  const res = await fetch("/api/model", options)
      .then(res => res.json())
      .catch(err => console.error(err));

  if (verbose>1)
    console.log("completed logging request");
}

function relu(ev,th){
  let data = {
    isParametric: false,
    isNative: true,
    mType:"ReLU",
    name: "relu1"
  };
  if (verbose>0)
    LOG("sending relu", JSON.stringify(data));
  send(data, "add");
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

  else
    LOG("no module found at this location"); // could be more descriptive
}


function verboseSig(ev){
  LOG("VERBOSE");
  let dataIn = {
    signal: "verbose"
  };
  LOG("CALLING FROM SIGNAL: ", dataIn);
  send(dataIn, "signal");
}

function buildSig (ev){
  LOG("BUILD");
  let dataIn = {
    signal: "build"
  };
  LOG("CALLING FROM SIGNAL: ", dataIn);
  send(dataIn, "signal");
}

function registerSig (ev){
  LOG("REGISTER");
  let dataIn = {
    signal: "register"
  };
  LOG("CALLING FROM SIGNAL: ", dataIn);
  send(dataIn, "signal");
}

var dragging = null;
function select(ev){
  var maybeRect = checkIfRect(ev);
  console.log(ev);
  if (verbose > 1)
    LOG(JSON.stringify(ev), JSON.stringify(maybeRect));

  if (maybeRect.found) 
    dragging = maybeRect.rect;
  console.log(dragging);
}

var drawablecbN = "rect";
var idToCB = {

  "relu"    : relu,
  "output"  : Output,
  "connect" : connect,
  "rect"    : genRect,
  "bilinear": linear,
  "linear"  : linear,
  "input"   : input,
  "select"  : select,
  "verbose" : verboseSig,
  "build"   : buildSig,
  "register": registerSig,
  "null"    : () => {console.log("null");LOG("null");},
};



//setTimeout(300, ()=>{document.getElementsByTagName("NAV").item(0).addEventListener("click", (e));});//(t) => { varidToCB[drawablecbN](t);});});


function drawClick(ev)
{
  LOG("calling " + drawablecbN);
  LOG(new String(ev), drawablecbN);



  idToCB[drawablecbN](ev);
}

setTimeout(300, ()=>{document.body.addEventListener("mouseUp", idToCB[drawableN]);});
setTimeout(300, ()=>{document.body.addEventListener("mouseDown", () => { drawablecbN = "null";})});


function selection(t)
{
  if (verbose > 1)
    LOG("selection", t.id);
  
  drawablecbN = new String(t.id);


  if (verbose > 2)
  {
    console.log("drawable callback name", new String(drawablecbN), "drawable id selected", new String(t.id));

    LOG(t, idToCB[t.id]);
  }

  //LOG(drawablecbN, idToCB[drawablecbN]);
}

async function LOG()
{
  var data_in = "LOGGING: ";
  for (let i = 0; i < arguments.length; i++)
    data_in += " " + new String(arguments[i]);

  if (verbose>0)
    console.log("LOGGING: logging", data_in);

  const data = JSON.stringify({data: data_in});
  
  const options = {
     method: "POST",
     headers : {"Content-Type":"application/json"},
     body: data
    };
  
  const res = await fetch("/api/logging", options)
      .then(res => res.json())
      .catch(err => console.error(err));
 };
  /*fLOG(drawablecb);
    drawable.removeEventListener("click", drawablecb);*/




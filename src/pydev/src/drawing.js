//GEOMETRIC PRIMITIVES
var verbose = 3;
var globalN = 1;
var curr = 0;
var drawablecb = genRect;
var svgCanvas; var SVG;
//DIRECT DOM RENDER VIA SVG







var lineCount = 0;
class Line{
  constructor(x1,y1,x2,y2,name){
    LOG("making line!");
    this.pointA = new Point(x1,y1,name+"A");
    this.pointB = new Point(x2,y2,name+"B");
    this.render = this.render.bind(this);


    this.Name = name;

  }

  
 render(){
    svgCanvas = document.getElementById("drawable_svg");
    let currentState = svgCanvas.innerHTML
    if (verbose > 0)
      LOG("render line!");
    svgCanvas.innerHTML = currentState + "<line x1=\"" + this.pointA.x.toString() + "\" y1=\"" + this.pointA.y.toString()
      + "\" x2 = \"" + this.pointB.x.toString() + "\" y2 = \"" + this.pointB.y.toString() 
      + "\" stroke=\"black\" class=\"svgline\" id=\"" + this.Name + "\"/>"; 
  lineCount++;
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
    SVG = document.getElementById("drawable_svg");
    let divrect = "<rect x=\"" + this.x.toString() + "\" y=\"" + this.y.toString() 
    + "\" height=\"" + this.size.toString() + "\" width=\"100\""
    + "id=\"" + this.Name + "\" class=\"moduleDiv\" />";
    SVG.innerHTML = SVG.innerHTML + divrect; 
  }
}




function genRect(ev, title, Name)
{
  //var r = new Rect(ev.clientX, ev.clientY, 100, "red", title, Name);
  var r = new Rect(ev.offsetX, ev.offsetY, 100, "red", title, Name);
  r.render();
  LOG(r);
  return r;
}


function checkLocDOM(ev, obj){
if  ((
  ((ev.offsetX > obj.x.baseVal.value) && (ev.offsetX <= (obj.x.baseVal.value + obj.width)))
      && ((ev.offsetY > obj.y.baseVal.value ) && (ev.offsetY <= (obj.y.baseVal.value + obj.height)))
      )){
      return true;
      }
    return false;
}
function checkLocHTML(ev, obj)
{
  LOG("CHECK LOG: ", ev, obj);
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
      console.log(ev.offsetX, localrect.x,ev.offsetY, localrect.y, localrect);
    if (checkLocDOM(ev, localrect)){ console.log("found a match");
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
  
  //connect module 1 to module click 2. describes a path of information flow and is used to parameterized weight matrices for model backend
  //check if a rectangle is beneath the click. if so, and if clicked previously and rect stored, announce connection to server
  var maybeEl = checkIfRect(ev);

  LOG(maybeEl);
  if (maybeEl.found)
  {
      if (!p1){
        console.log("p1");
        console.log(ev,maybeEl);
        if (verbose > 1)
          LOG("part 1 conn");
        p1 = new Point(ev.offsetX, ev.offsetY, maybeEl.rect.id); //new Point(ev.clientX, ev.clientY);
        connEl = maybeEl.rect;
      }
      else if (!p2){ 
        console.log(ev, maybeEl);
        if ( verbose > 1) 
          LOG("part 2 conn");
        p2 = new Point(ev.offsetX, ev.offsetY, maybeEl.rect.id);
        let out = new Line(p1.x, p1.y, p2.x, p2.y, connEl.id + maybeEl.rect.id);
        LOG(out);
        LOG("CONNECT: FIRST: ", connEl);
        LOG("CONNECT: SECOND" , maybeEl);
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
  // A maintainer of click states for render later
  constructor(x,y,Name){
    this.x = x;
    this.y = y;
    this.Name = Name;
  }
};


var PointA = new Point(0,0,"PA");
var PointB = new Point(100,100,"PB");
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

function linear(ev)
{
  // Linear Transformation of input, defined through dimenion of feature space between other modules
  var name = "A" + globalN.toString();
  globalN++;
  let rect=genRect(ev, "Linear", name);

LOG(name, globalN);
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


function Output(ev, th)
{
  //To handle guarantee on dim of output space, nonlinearity, etc.
  let data = {isParametric: false, isNative: false, Name: "output"};
  console.log("FROM OUTPUT", th);
  genRect(ev, "Output");
  send(data, "add");
  return data;
 } 








async function send(data_in, signal_type)
{
  //handles comm with express and effectively interfaces frontend to backend
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

function relu(ev){
  // ReLU Module, sends info to model backend
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
  //To house selectors corresponding to rectangle attributes
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
  // display cache and connections in the model backend
  LOG("VERBOSE");
  let dataIn = {
    signal: "verbose"
  };
  LOG("CALLING FROM SIGNAL: ", dataIn);
  send(dataIn, "signal");
}

function buildSig (ev){
  //builds forward pass, model definition, and writes to file "local.py"
  LOG("BUILD");
  let dataIn = {
    signal: "build"
  };
  LOG("CALLING FROM SIGNAL: ", dataIn);
  send(dataIn, "signal");
}


function registerSig (ev){
  //used by the ython model state to update cache registration
  LOG("REGISTER");
  let dataIn = {
    signal: "register"
  };
  LOG("CALLING FROM SIGNAL: ", dataIn);
  send(dataIn, "signal");
}





var dragging = null; //helper for moving around selected elements
function select(ev){
  var maybeRect = checkIfRect(ev);
  console.log(ev);
  if (verbose > 1)
    LOG(JSON.stringify(ev), JSON.stringify(maybeRect));

  if (maybeRect.found) 
    dragging = maybeRect.rect;
  console.log(dragging);
}

var drawablecbN = "rect"; // initial callback





// CALLBACK DICTIONARY
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
  //Implements the drawing to the document from callback, among other things
  LOG("calling " + drawablecbN);
  LOG(new String(ev), drawablecbN);



  idToCB[drawablecbN](ev);
}

setTimeout(300, ()=>{document.body.addEventListener("mouseUp", idToCB[drawableN]);});
//setTimeout(300, ()=>{SVG = document.getElementById("drawablesvg");});
setTimeout(300, ()=>{document.body.addEventListener("mouseDown", () => { drawablecbN = "null";})});


function selection(t)
{
  //Handles changing of callback through a json mapping from str to function object
  if (verbose > 1)
    LOG("selection", t.id);
  selectColorify(t); 
  drawablecbN = new String(t.id);


  if (verbose > 2)
  {
    console.log("drawable callback name", new String(drawablecbN), "drawable id selected", new String(t.id));

    LOG(t, idToCB[t.id]);
  }

  //LOG(drawablecbN, idToCB[drawablecbN]);
}

var buttonid = null;var selected = null;
async function LOG()
{
  var data_in = "LOGGING: ";
  for (let i = 0; i < arguments.length; i++)
    data_in += " " + new String(arguments[i]);


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



setTimeout(2000, ()=>{new Line(new Point(0,0,"00"), new Point(window.width, window.height, "01")).render();});
function selectColorify(t)
{
  if (buttonid != t.id)
  {
    if (verbose >2) 
      LOG(t.id);LOG(`setting button id ${buttonid} to ${t.id}`);
    if (selected){
      selected.style.background = '#EEE';
    }
    selected = t;
    buttonid = t.id ;
    selected.style.background = 'red';
    LOG(`Updated button to red.`);
  }
}

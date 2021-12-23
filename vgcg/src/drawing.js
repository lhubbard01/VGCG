//GEOMETRIC PRIMITIVES

const WIDTH  = 50;
const HEIGHT = 50;

class CanvasObj
{
  constructor (color, width, height, x, y, type, geom_type, id)
  {
    this.color  = color;
    this.width  = width;
    this.height = height;

    this.left   = x;
    this.top    = y;

    this.geom_type = geom_type;
    this.type      = type;
    this.id        = id; //usage : is for describing class
  }
}


var cnt = 0;
class Canvas
{
  constructor(canvas)
  {
    this.C = canvas;
    this.CLeft = this.C.offsetLeft;
    this.CTop = this.C.offsetTop;
    this.ctx = this.C.getContext("2d");
    this.elements = [];

    this.renderAll = this.renderAll.bind(this);
    this.addElement = this.addElement.bind(this);
    this.clickElement = this.clickElement.bind(this);

    this.C.addEventListener("auxclick", this.clickElement, event);
    this.checkIfRect = this.checkIfRect.bind(this);    

  } 

  checkIfRect(ev)
  {
    //checks for if an element is being clicked on
    let module_rects = this.elements;
    for (let i = 0; i < module_rects.length; ++i)
    {
      let localrect = module_rects[i];
      console.log(localrect);
      console.log(ev.offsetX, localrect.x,ev.offsetY, localrect.y, localrect);
      if (checkLoc(ev, localrect) && localrect.geom_type == "RECT")
      {
        console.log("found a match");
        return {found: true, rect: localrect};
      }

    }
    return {found: false, rect: null};
  }
  

  addElement(event) 
  {

    var x = event.clientX, 
        y = event.clientY ;
    var OBJ = drawClick(event) ;
    if (OBJ){
      this.elements.push( OBJ);
      cnt++;
      this.renderAll();
    }
  } 

  clickElement(event)
  {
    var x = event.clientX, // this.CLeft,
        y = event.clientY; //- this.CTop;

    console.log(x, y);
    let outcome = this.checkIfRect(event), element;
    if(outcome.found){ 
      element = outcome.rect;
      //element.auxclick();
      alert('clicked an element: ', element);
    }
  }
  





  /* NOTE code adapted from stack overflow adding callbacks to canvas objects
  Add element.
  elements.push({
    colour: '#05EFFF',
    width: 150,
    height: 100,
    top: 20,
    left: 15
  });*/

  renderAll()
  {
    this.ctx.clearRect(0,0,this.C.width, this.C.height);

    for (let i = 0; i < this.elements.length; ++i)
    {
      let element = this.elements[i];
      console.log(element);
      if (element.geom_type == "RECT"){
        this.ctx.fillStyle = element.color;
        this.ctx.fillRect(element.left,
          element.top,
          element.width,
          element.height);

        this.ctx.fillText(element.id + " : " + element.type, element.left, element.top);
        }
      
      else if (element.geom_type == "LINE")
      {
        this.ctx.moveTo(element.pointA.x, element.pointA.y);
        this.ctx.lineTo(element.pointB.x, element.pointB.y, 10,10);
        this.ctx.stroke();
      }

    }
  }
}


var C;
function drawableC(event){
  C.addElement(event);
}
function promptGen(count, list_of_name_to_default)
{
  var gathered_values = [];
  for (let i = 0; i < count; ++i)
  {
      gathered_values.push(prompt(list_of_name_to_default[i]));// el[1]));
  }
  return gathered_values;
}

function htmlel(type)
{
  let loc = document.createElement(type);
  for (let i = 1; i < arguments.length; i++){
    switch(i){
      case 1: loc.className = arguments[i]; break;
      case 2: loc.id = arguments[i]; break;
      case 3: { 
        for ( let el in arguments[3]){
          loc.setAttribute(el, arguments[3][el]); // sets the left side to the right side eg type=text
        } 
      } break;

      default: break;
    }
  } return loc;
}



function prompter(dims, strings)
{

/*
  let prompter = htmlel("div", "prompter", "dims");


  for (let i = 0; i < dims; i++){
    prompter.appendChild(htmlel("input", "promptrow", "dim" + i.toString(), {"type" : "text"}));
  }
  document.body.appendChild(prompter);*/
  let out = promptGen(dims, strings);
  return out;
}

  // Linear Transformation of input, defined through dimenion of feature space between other modules
var ID_LOOKUP = {};

var verbose = 3;
var globalN = 1;
var curr = 0;
var drawablecb = linear;
var svgCanvas; var SVG;
//DIRECT DOM RENDER VIA SVG
function Xr(event, owner){console.log("before menu make"); let x = new Menu(event, owner); console.log(owner); }



var lineCount = 0;




/*
class SVG_HTML{
  constructor(Name, cb_list){

    this.Name = Name
    this.cb_list = cb_list
    this.appendEvent = this.appendEvent.bind(this);
  }

  appendEvent(ev, cb){
    this.cb_list += ev; // of form str(ev), str(cb) // added raw to html
  }
}

function setEvHdlr(eventHook, callback){
  return eventHook + "=\"" + callback + "(event)\"";
}
function setId(id_in){
  return " id=\"" + id_in + "\"";
}
function setClass(classIn){
  return " class=\"" + classIn + "\"";
}
function appendHTMLState(obj, newstr){
  obj.innerHTML = obj.innerHTML + newstr;
}
function setColor(objId, color){
  let obj = document.getElementById(objId);
  console.log(obj);
  obj.style.fill = color;
}
*/
function getInput(promptstr){
  let new_in = prompt(promptstr);
  return new_in;
}
  
function updateAttr(id, obj){
	ID_LOOKUP[id] = obj;
}


class Line extends CanvasObj
{
  constructor(x1,y1,x2,y2,n1,n2,name)
  {
    console.log(x1,y1,x2,y2,n1,n2,name);
    super("black", 5,5, 0,0, "line", "LINE", name,);
    LOG("making line!");
    this.pointA = new Point(x1,y1,name+"A");
    this.pointB = new Point(x2,y2,name+"B");
    this.originalA = n1;
    this.originalB = n2;
    this.attrs = {
      pointA_setcolor: () => {
        setColor(this.originalA.id, "green");}, 
      pointB_setcolor: () => {
        setColor(this.originalB.id, "green");},
      setA_in: () => { 
        let newIns = Number(getInput("new input count for " + this.originalA.id + " : "));
        this.originalA.outs = newIns;
				updateAttr(this.originalA.id, this.originalA);
        console.log(this);
        this.update("A", newIns);}
    }
    this.init = this.init.bind(this);
    this.update = this.update.bind(this);
    this.remove= this.remove.bind(this);
  }


   init()
   {
     console.log(this);
        let data = {
          from:{
            Name: this.originalA.id,
            count: this.originalA.outs
          }, 
          to:{
            Name: this.originalB.id,
            count: this.originalB.ins
          }
        };


      send(data, "conn");
      lineCount++;
     console.log(this);
  }

  

  remove()
  {
    let data = { 
      from: { 
        Name: this.originalA.id,
        count: this.originalA.outs
      },
      to: {
        Name: this.originalB.id,
        count: this.originalB.ins
      }
    };
    console.log("removing, ", data);
    send(data, "conn-remove");
     console.log(this);
  }
  
  
  
  update(AorB, update)
  {
    this.remove(); 
    this.init();
  }


}
//CONTAINER CLASS FOR DIRECT DOM RENDER // holds state for the modules locally
class Rect extends CanvasObj{
  constructor(color, width, height, x,y, type, id)
  {
    super(color, width, height, x, y, type, "RECT",  id);
    this.register = this.register.bind(this);
  }




  
  register(ptr)
  {
    ID_LOOKUP[this.id] = ptr;
  }
}


function genRect(ev, type, id, color)
{
  let size = 100;
  var r = new Rect(color, size, size, ev.offsetX, ev.offsetY, type, id);
  //r.render();
  LOG(r);
  return r;
}



function checkLoc(ev, obj)
{
  if(
      ((ev.offsetX > obj.left)
        && (ev.offsetX <= (obj.left + obj.width))
        )
      && (
        (ev.offsetY > obj.top) 
        && (ev.offsetY <= (obj.top +  obj.height))
      )
    )
    
    {
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
  console.log("INSIDE CONNECT IS");
  var maybeEl = C.checkIfRect(ev);
  console.log("MAYBE ELEMENT IS ", maybeEl);
  LOG(maybeEl);
  if (maybeEl.found)
  {
    console.log("in first")
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
        let out = new Line(p1.x, p1.y, 
            p2.x, p2.y,
            ID_LOOKUP[connEl.id], ID_LOOKUP[maybeEl.rect.id], 
            connEl.id + maybeEl.rect.id);


        out.init();
        connEl = null; p1 = null; p2 = null; maybeEl = null;
        return out;
      }
  }
    console.log("exit connect");

}
var x = genRect;
LOG(x);


class Point{
  // A maintainer of click states for render later
  constructor(x,y,Name)
  {
    this.x = x;
    this.y = y;
    this.Name = Name;
  }
};






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





class Module extends Rect
{
  constructor(ev,  mType, isParametric, isNative, NamePre)
  {
    let id = NamePre + globalN.toString();
    globalN++;
    let width = 100;
    let height = 100;
    let color = isParametric ? "red" : "blue";
    super(color, width, height, ev.offsetX, ev.offsetY, mType, id);   
    this.isParametric = isParametric;
    this.isNative     = isNative;
    this.hyperp       = {};
    this.register(this);


    if (isParametric)
    {
      let ins_outs = prompter(2, ["in_features","out_features"]);
      this.ins = ins_outs[0];
      this.outs = ins_outs[1];
    } 
    else 
    { 
      this.ins = 500;
      this.outs = 500;
    };
    
    this.sender = this.sender.bind(this);
    this.sender("ADD");
  };

  sender(signal_type){
    let data = {
      isParametric: this.isParametric,
      isNative: this.isNative,
      mType: this.type,
      Name: this.id,

    hyperp: JSON.stringify(
    {
      in_features: this.ins, 
      out_features: this.outs
      })
    };

    console.log(data);
    if (signal_type == "ADD")
    {
			send(data, "add");
		} else if (signal_type == "UPDATE") 
    { 
			send(data, "update"); 
		}
  }
}

class Linear extends Rect{
  constructor(ev){ 
    let id = "A" + globalN.toString();
    super(ev.offsetX, ev.offsetY, 100, "red", "Linear", Name);   
    this.Name = Name;
    globalN++;
    this.render(this);
    this.isParametric = true;
    this.isNative = true;
    this.mType = "Linear";
    this.ins = 100;
    this.outs = 50;
    this.sender = this.sender.bind(this);
    this.sender("ADD");
  }
  
  sender(signal_type){
    let data = {isParametric: this.isParametric,
    isNative: this.isNative,
    mType: this.mType,
    Name: this.Name,
    hyperp: JSON.stringify({in_features: this.ins, out_features: this.outs})
    };

    console.log(data);
    if (signal_type == "ADD"){
			send(data, "add");
			} else if (signal_type == "UPDATE") { 
				send(data, "update"); 
		}
  }
}



// Linear Transformation of input, defined through dimenion of feature space between other modules
function linear(ev){     return new Module(ev, "Linear", true, true, "A");  }
function bilinear(ev){   return new Module(ev, "Bilinear", true, true, "Bilinear");}
function relu(ev){       return new Module(ev, "ReLU", false, true, "ReLU");}
function sigmoid(ev){    return new Module(ev, "Sigmoid", false, true, "Sigmoid"); }
function softmax(ev){    return new Module(ev, "Softmax", false, true, "Softmax");}
function leakyrelu(ev) { return new Module(ev, "LeakyReLU", false, true, "LeakyReLU"); }
function tanh(ev) {      return new Module(ev, "Tanh", false, true, "TanH"); }
   
function update(ev)
{
	let maybeRect = checkIfRect(ev); 
	if (maybeRect.found ) {
		ID_LOOKUP[maybeRect.rect.id].sender("UPDATE");
	}
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







/// IMPORTANT
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

class ReLU extends Module{
  constructor(ev){
    let id = "R" + globalN.toString();
    super(ev.offsetX, ev.offsetY, 100, "blue", "ReLU", Name);   
    this.Name = Name;
    globalN++;
    this.render(this);
    this.isParametric = false;
    this.isNative = true;
    this.mType = "ReU";
    this.ins = 100;
    this.outs = 50;
    this.sender = this.sender.bind(this);
    this.sender("ADD");
  }
  
  sender(signal_type){
    let data = {isParametric: this.isParametric,
    isNative: this.isNative,
    mType: this.mType,
    Name: this.Name,
    hyperp: JSON.stringify({in_features: this.ins, out_features: this.outs})
    };
    console.log(data);
    if (signal_type == "ADD"){
			send(data, "add");
			} else if (signal_type == "UPDATE") { 
				send(data, "update"); 
		}
  }
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
var ID_TO_CB = { 
  "output"  : Output,
  "connect" : connect,
  "update"  : update,

  "rect"    : genRect,
  "bilinear": bilinear,
  "linear"  : linear,
  
  "relu"    : relu,
  "lrelu"   : leakyrelu,
  "softmax" : softmax,
  "sigmoid" : sigmoid,
  "tanh"    : tanh,
  
  "input"   : input,
  "select"  : select,

  "verbose" : verboseSig,
  "build"   : buildSig,
  "register": registerSig,
  "null"    : () => {console.log("null");LOG("null");},
};



function drawClick(ev)
{
  //Implements the drawing to the document from callback, among other things
  LOG("calling " + drawablecbN);
  LOG(new String(ev), drawablecbN);



  return ID_TO_CB[drawablecbN](ev);
}

setTimeout(300, ()=>{document.body.addEventListener("mouseUp", ID_TO_CB[drawableN]);});
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
    LOG(t, ID_TO_CB[t.id]);
  }

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


function rowGen(obj, attrs, className){
  
	for (let el in attrs){
    let locp = document.createElement("p"); 
    if (!(className === null) && !(typeof className === "undefined")) 
      locp.className = className;
	  locp.addEventListener("click", attrs[el]); 
	  locp.innerHTML = el;

    obj.appendChild(locp);
	}
  
	console.log(obj.innerHTML);
  return obj;
}









class Row
{
  constructor(name, callback)
  {
    this.Name = name;
    this.cb = callback;
  }
}

class ObjDesc{
  constructor(rows, obj)
  {
    this.rows = rows;
    this.obj = obj;
  }
}


class Menu
{
  constructor(e, owner)
  { console.log("creating menu object");
    console.log(e, owner);
    this.render = this.render.bind(this);
    this.obj = owner;
    if (popupExists){
      popup.remove();
    }
    this.render(e);
  }

  render(e){
    let localdiv = document.createElement("div");
    
		localdiv.className = "popup";  
    
		rowGen(localdiv, this.obj.attrs, "popup-row");
    
		localdiv.style.position = "absolute";
    localdiv.style.left = e.clientX + "px";
    localdiv.style.top = e.clientY + "px";

    this.html = localdiv;
    document.body.appendChild(localdiv);
  
  popup = localdiv;
  popupExists = true;
  }


}

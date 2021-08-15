//GEOMETRIC PRIMITIVES
var ID_LOOKUP = {};

var verbose = 3;
var globalN = 1;
var curr = 0;
var drawablecb = linear;
var svgCanvas; var SVG;
//DIRECT DOM RENDER VIA SVG
function Xr(event, owner){console.log("before menu make"); let x = new Menu(event, owner); console.log(owner); }



var lineCount = 0;





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

function getInput(promptstr){
  let new_in = prompt(promptstr);
  return new_in;
}
  
function updateAttr(id, obj){
	ID_LOOKUP[id] = obj;
}
class Line extends SVG_HTML{
  constructor(x1,y1,x2,y2,n1,n2,name){
    super(name);
    LOG("making line!");
    this.pointA = new Point(x1,y1,name+"A");
    this.pointB = new Point(x2,y2,name+"B");
    this.render = this.render.bind(this);
    this.Name = name;
    this.originalA = n1;
    this.originalB = n2;
    this.attrs = {
      pointA_setcolor: () => {
        setColor(this.originalA.Name, "green");}, 
      pointB_setcolor: () => {
        setColor(this.originalB.Name, "green");},
      setA_in: () => { 
        let newIns = Number(getInput("new input count for " + this.originalA.Name + " : "));
        this.originalA.outs = newIns;
				updateAttr(this.originalA.Name, this.originalA);
        console.log(this);
        this.update("A", newIns);}
    }
    this.init = this.init.bind(this);
    this.update = this.update.bind(this);
    this.remove= this.remove.bind(this);
  }
  

   init(){
     console.log(this);
        let data = {
          from:{
            Name: this.originalA.Name,
            count: this.originalA.outs
          }, 
          to:{
            Name: this.originalB.Name,
            count: this.originalB.ins
          }
        };


      send(data, "conn");
     console.log(this);
  }
  
  remove(){
    let data = { 
      from: { 
        Name: this.originalA.Name,
        count: this.originalA.outs
      },
      to: {
        Name: this.originalB.Name,
        count: this.originalB.ins
      }
    };
    console.log("removing, ", data);
    send(data, "conn-remove");
     console.log(this);
  }
  
  update(AorB, update){
    this.remove(); 
    this.init();
  }

  render(callback, type){
    svgCanvas = document.getElementById("drawable_svg");
    let currentState = svgCanvas.innerHTML
    if (verbose > 0)
      LOG("render line!");
    let newLine = "<line x1=\"" + this.pointA.x.toString() + "\" y1=\"" + this.pointA.y.toString()
      + "\" x2 = \"" + this.pointB.x.toString() + "\" y2 = \"" + this.pointB.y.toString() 
      + "\" stroke=\"black\" class=\"svgline\" id=\"" + this.Name + "\" >";
      //+ callback + "=\"" + type + "(event,  " + JSON.stringify(this.attrs) + ")\">";

    
    console.log(newLine);
    appendHTMLState(svgCanvas, newLine);
    let localline = document.getElementById(this.Name);
    localline.addEventListener("auxclick", (event) => { Xr( event, this); });
    this.html = localline;
  lineCount++;
  }


};

//CONTAINER CLASS FOR DIRECT DOM RENDER // holds state for the modules locally
class Rect extends SVG_HTML{
  constructor(x,y,size,color, title, Name){
    super(Name);
    this.x = x;
    this.y = y;
    this.size = size;
    this.color = color;
    this.title = title;
    this.Name  = Name;
    this.render = this.render.bind(this);
  }
  render(ptr){
    svgCanvas = document.getElementById("drawable_svg");
    let newRect = "<rect x=\"" + this.x.toString() + "\" y=\"" + this.y.toString() 
    + "\" height=\"" + this.size.toString() + "\" width=\"100\""
    + "id=\"" + this.Name + "\" class=\"moduleDiv\" fill=\"" + this.color + "\"/>";
    
		let textrect = "<text x = \"" + this.x.toString() +"\" y=\""+this.y.toString() + "\">" + this.Name +"\n" + this.title + "</text>";
    
		appendHTMLState(svgCanvas, textrect + "\n" + newRect );

    this.html = newRect;
    ID_LOOKUP[this.Name] = ptr;
  }
}


function genRect(ev, title, Name, color)
{
  var r = new Rect(ev.offsetX, ev.offsetY, 100, color, title, Name);
  r.render();
  LOG(r);
  return r;
}



function checkLocDOM(ev, obj)
{
  if(
      ((ev.offsetX > obj.x.baseVal.value)
        && (ev.offsetX <= (obj.x.baseVal.value + obj.width.baseVal.value))
        )
      && (
        (ev.offsetY > obj.y.baseVal.value ) 
        && (ev.offsetY <= (obj.y.baseVal.value + obj.height.baseVal.value))
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

function checkIfRect(ev)
{
  //checks for if an element is being clicked on
  module_rects= document.getElementsByClassName("moduleDiv");
  for (let i = 0; i < module_rects.length; ++i)
  {
    let localrect = module_rects.item(i);
    console.log(ev.offsetX, localrect.x,ev.offsetY, localrect.y, localrect);
    if (checkLocDOM(ev, localrect))
    {
      console.log("found a match");
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
        let out = new Line(p1.x, p1.y, p2.x, p2.y, ID_LOOKUP[connEl.id], ID_LOOKUP[maybeEl.rect.id], connEl.id + maybeEl.rect.id);
        out.init();
        out.render("onauxclick", "Xr");
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





class Linear extends Rect{
  constructor(ev){ 
    let Name = "A" + globalN.toString();
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

function linear(ev)
{
  // Linear Transformation of input, defined through dimenion of feature space between other modules
  let l = new Linear(ev);
}
function update(ev){ 
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



function relu(ev){
  // ReLU Module, sends info to model backend
  var name = "R" + globalN.toString();
  globalN++;
  let rect = genRect(ev, "ReLU", name, "blue");

  let data = {
    isParametric: false,
    isNative: true,
    mType:"ReLU",
    
    Name: rect.Name,
    hyperp: JSON.stringify({})
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
  "update"  : update,
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



function drawClick(ev)
{
  //Implements the drawing to the document from callback, among other things
  LOG("calling " + drawablecbN);
  LOG(new String(ev), drawablecbN);



  idToCB[drawablecbN](ev);
}

setTimeout(300, ()=>{document.body.addEventListener("mouseUp", idToCB[drawableN]);});
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

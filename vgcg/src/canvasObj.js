class CanvasObj{
  constructor (color, width, height, x, y, id){
    this.color  = color;
    this.width  = width;
    this.height = height;
    this.left   = x;
    this.top    = y;
    this.id     = id; //usage : is for describing class
  }
}

class Canvas{
  constructor(canvas){
    this.C = canvas;
    this.CLeft = this.C.offsetLeft;
    this.CTop = this.C.offsetTop;
    this.ctx = this.C.getContext("2d");
    this.elements = [];

    this.renderAll = this.renderAll.bind(this);
    this.addElement = this.addElement.bind(this);
    this.clickElement = this.clickElement.bind(this);

    this.C.addEventListener("click", this.clickElement, event);
  } 

  addElement(event) { 
    var x = event.pageX - this.CLeft, 
        y = event.pageY - this.CTop;
    
    this.elements.push(new CanvasObj("#05EFFF",  150, 150, x,y));
  
    this.renderAll();
  }
  

  clickElement(event)
  {
    console.log("event listener is running for canvas");
    var x = event.pageX - this.CLeft,
        y = event.pageY - this.CTop;

    console.log(x, y);
    this.elements.forEach(
      function(element) 
      {
        if (y > element.top && y < element.top + element.height
          && x > element.left && x < element.left + element.width)
          {
            alert('clicked an element');
          }
      });
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

  renderAll(){
    this.ctx.clearRect(0,0,this.C.width, this.C.height);
    for (let i = 0; i < this.elements.length; ++i)
    {
      let element = this.elements[i];
        console.log(this.elements[i]);
        console.log(this.ctx);
      this.ctx.fillStyle = element.color;
      this.ctx.fillRect(element.left,
          element.top,
          element.width,
          element.height
      );

    }
  }
}


var C;
function drawableC(event){
  C.addElement(event);
}
/*class CObj{
  constructor(Name, cb_list){
    this.Name = Name
    this.cb_list = cb_list
    this.appendEvent = this.appendEvent.bind(this);
  }

  appendEvent(ev, cb){
    this.cb_list += ev; // of form str(ev), str(cb) // added raw to html
  }
}

class Line extends CObj{
  constructor(x1,y1,x2,y2,n1,n2,name)
  {
    super(name);
    LOG("making line!");
    this.pointA = new Point(x1,y1,name+"A");
    this.pointB = new Point(x2,y2,name+"B");

    this.render = this.render.bind(this);

    this.originalA = n1;
    this.originalB = n2;

    this.attrs = {
      pointA_setcolor: () => {
        setColor(this.originalA.Name,
        "green");
      }, 
      pointB_setcolor: () => {
        setColor(this.originalB.Name,
        "green");
      },
      setA_in: () => { 
        let newIns = Number(
          getInput("new input count for " + this.originalA.Name + " : ")
          );
        this.originalA.outs = newIns;
				updateAttr(
          this.originalA.Name, this.originalA
          );
        console.log(this);
        this.update("A", newIns);
      }
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
    if (verbose > 0)
      LOG("render line!");
    ctx.moveTo(this.pointA.x, this.pointA.y);
    ctx.beginPath();
    ctx.moveTo(this.pointB.x, this.pointB.y);
    ctx.strokeStyle = "black";
    ctx.stroke();
    ctx.closePath();
    
    localline.addEventListener("auxclick", (event) => { Xr( event, this); });
    this.html = localline;
  lineCount++;
  }


};
*/

**Visual Graphics for Computational Graph Definitions**

This is a graphical user interface for developing computation graphic models on local machines.
It is intended to eventually support model definitions through the GUI, whereby their edges, in a directed, acyclic, feedforward fashion, can be used for generating an intermediate represetnation that is read by a target framework of choice. 
It is intended that the user can create network components in a modular and efficient manner, emphasizing reusability for efficient model definitions.
Instructions: the buttons on the right side, some of them work. the ones that work are connect, linear, verbose, and build.
Relu works ut doesnt connect to other things because it has yet to inherit from Rect, which will allow for a really easy way to communicate data
Buttons:
*verbose  tells the gen.py runtime to print all data it has stored (its internal state for data to build from)
*build writes the graph to a file in the same directory titled "local.py". 
*connect lets user click one and another rectangle to join them on the graph
#* web browser is **required**. The port that is listened at is **3001**, navigated to by <code>localhost:3001</code>

Copyright (C) 2021,  Lyle Hubbard

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

IMAGES
![image1](/assets/
![image2](/assets/
![image3](/assets/
![image4](/assets/
![image5](/assets/
![vid

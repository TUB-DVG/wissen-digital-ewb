
# Css/Html:

https://www.w3schools.com/tags/default.asp


HTML and CSS Tutorial for 2021 - COMPLETE Crash Course!:https://www.youtube.com/watch?v=D-h8L5hgW-w

## Css: override

In Css it is possible to override class proporties: This can allow us to use some predefined css classes ( bootstrap classes for example) but modify them to suit our needs( a unique coloring template etc..)

There multiple ways to override Css classes:

Assuming you have this html selector

< a class="background_color " href="#" >

Let's say that in the class "background_color", the background color is defined as blue:

 .background_color { background: blue 

                        .....

                    }

if we want to override that, we can add a new class called background-none, so our selector would be:

 < a class="background_color background-none" href="#" >

*Any of the following would override it:

**a.background-none { background: none; }**

**body .background-none { background: none; }**

**.background-none { background: none !important; }**


The first 2 methods work through generalizing the selector proporties: Styling the tags the classes are used under.The last method uses !important, a blunt instrument ( wins through selector priority).

One could also organize your style sheets so that simply

.background-none { background: none; }


would work. In this case, the rule wins simply by order, i.e. by being after an otherwise equally “powerful” rule. But this imposes restrictions and requires you to be careful in any reorganization of style sheets.

These are all examples of the CSS Cascade, a crucial but widely misunderstood concept. It defines the exact rules for resolving conflicts between style sheet rules.

CSS Cascade:https://www.w3.org/TR/CSS2/cascade.html#cascade


https://www.geeksforgeeks.org/how-to-override-the-css-properties-of-a-class-using-another-css-class/

https://stackoverflow.com/questions/20954715/how-to-override-the-properties-of-a-css-class-using-another-css-class/20954771




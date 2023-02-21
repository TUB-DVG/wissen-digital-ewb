# Responsive Design with Bootstrap

## Bootstrap CSS classes
Bootstrap is a grid based css framework. It gives us css classes for different screen width.

### Bootstrap grid classes
Bootstrap’s grid system uses a series of containers, rows, and columns to layout and align content. It’s built with [flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) and is fully responsive. 

The following example gives us a container with three equally wide `.col`umns in a `.row`, centered in the page with the `.container` parent across all screen-widths, devices and viewports.
``` html
<div class="container">
  <div class="row">
    <div class="col">
      Column
    </div>
    <div class="col">
      Column
    </div>
    <div class="col">
      Column
    </div>
  </div>
</div>
```

The grid system of the Bootstrap frameworks also supports percentage column widths, based on a 12-columns-grid. You can choose a column-width to be `n`/12 wide through assigning it the class `.col-{n}` where `n` is a natural number between 1 and 12. In the following example you can see some column splits.
``` html
<div class="container"> 
  <div class="row">
    <div class="col-12">
      Column
    </div>
  </div>
  <div class="row">
    <div class="col-2">
      Column
    </div>
    <div class="col-10">
      Column
    </div>
  </div>
  <div class="row">
    <div class="col-1">
      Column
    </div>
    <div class="col-7">
      Column
    </div>
    <div class="col-4">
      Column
    </div>
  </div>
</div>
```

### Bootstrap Spacing (Padding and Margin)
Assign responsive-friendly margin or padding values to an element or a subset of its sides with shorthand classes. Includes support for individual properties, all properties, and vertical and horizontal properties. Classes are built from a default Sass map ranging from .25rem to 3rem.

You assign spacing to an element through `{property}{sides}-{breakpoint}-{size}` or `{property}{sides}-{size}` if you want to assign a spacing for all sizes.


### Bootstrap Breakpoints
The bootstrap grid supports six responsive breakpoints: `xs`, `sm`, `md`, `lg`, `xl`, `xxl`.
The breakpoints are based on `min-width` [media-queries](#media-queries).

You assign breakpoints to the column classes through `col-{breakpoint}-{size}`.

If you want to do main content with a side bar, where each the main content and the side bar go full-width on smaller devices (for example a screen-width smaller or equal of the screen-width of some tablet-portrait viewport) you can do it as in the following example. Assigning `.col-md-n` to a column means that the column will get the proportional width `n` for screen-widths going up from the breakpoint `md` and full-width for smaller devices (i.e. tablet-portait viewport and smartphones-portrait or smartphones-landscape viewport). 

``` html
<div class="container"> 
  <div class="row">
    <div class="col-md-8">
      Main content
    </div>
    <div class="col-md-4">
      Side bar
    </div>
  </div>
</div>
```

## Flexbox

The Flexbox Layout (Flexible Box) module (a W3C Candidate Recommendation as of October 2017) aims at providing a more efficient way to lay out, align and distribute space among items in a container, even when their size is unknown and/or dynamic (thus the word “flex”).

The main idea behind the flex layout is to give the container the ability to alter its items’ width/height (and order) to best fill the available space (mostly to accommodate to all kind of display devices and screen sizes). A flex container expands items to fill available free space or shrinks them to prevent overflow.

Most importantly, the flexbox layout is direction-agnostic as opposed to the regular layouts (block which is vertically-based and inline which is horizontally-based). While those work well for pages, they lack flexibility (no pun intended) to support large or complex applications (especially when it comes to orientation changing, resizing, stretching, shrinking, etc.).

Note: Flexbox layout is most appropriate to the components of an application, and small-scale layouts, while the Grid layout is intended for larger scale layouts.

[https://css-tricks.com/snippets/css/a-guide-to-flexbox/](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

## Media Queries

Media queries are useful for modifying a website depending on a device's screen properties as width or orientation.

There are for example the attributes `min-width`, `max-width`, `orientation`.
One writes for example a media-query that assigns a style if the screen width is smaller then 854px as follows

``` css
@media (max-width: 854px) { ... }
```

One can also combine media queries with logical operators as follows

``` css
@media (min-width: 30em) and (max-width: 50em) { ... }
```

[https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries/Using_media_queries](https://developer.mozilla.org/en-US/docs/Web/CSS/Media_Queries/Using_media_queries)
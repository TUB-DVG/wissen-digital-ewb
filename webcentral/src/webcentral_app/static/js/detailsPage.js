
//function addDotsWhenCollapsed() {
//  blocksOfContent = $(".blockOfContent");
//  var showMoreLink = undefined;
//  var collapsedElement = undefined;
//  for (var i=0; blocksOfContent.length>i; i++) {
//    showMoreLink = $(blocksOfContent[i]).find("a");
//    if (showMoreLink.length > 0) {
//      collapsedElement = $(blocksOfContent[i]).find(".collapse");
//      if 
//    }
//  }
//
//}

$( document ).ready(function(){
 
    $( "div.showMore a" ).on( "click", function() {
      var divBlockOfContent = $(this).parents("div.blockOfContent");
      var difFirstPart = $(divBlockOfContent).find(".firstPart");
      var collapseDiv = $(divBlockOfContent).find(".collapse");
      var dotsDiv = $(divBlockOfContent).find("div.dots");
      var textOfFirstPart = $(divBlockOfContent).find(".firstPart")[0].textContent;
      while (textOfFirstPart[textOfFirstPart.length-1] == " ") {
        textOfFirstPart = textOfFirstPart.slice(0, -1);
      }
      difFirstPart[0].textContent = textOfFirstPart.trimEnd();
      if (collapseDiv.hasClass("show")) {
         $(dotsDiv).css("display", "inline");
       
      }
      else {
        $(dotsDiv).css("display", "none");
      }
    });
 
});

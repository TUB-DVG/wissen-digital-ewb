



// the criteria catalog is modified, so that the layer deeper than the 2. layer is shown in one element
modifyCatalogToBeShownInOneElement();
depthFirstWalkForParagraphs();
if (idOfTopicToBeOpened != "") {
  var elementsToBeSearched = document.getElementById("hi").querySelectorAll("button, p");;
  for (var i = 0; i < elementsToBeSearched.length; i++) {
    if (elementsToBeSearched[i].getAttribute("topicId").includes(idOfTopicToBeOpened)) {
      var rootElement = findRootElement(elementsToBeSearched[i]);
      depthFirstWalk(rootElement, elementsToBeSearched[i]);  
    }
  }
  openHeadingsForLayers();
}

const el = document.querySelector(".sticky-third-lvl")
const observer = new IntersectionObserver( 
([e]) => e.target.classList.toggle("is-pinned", e.intersectionRatio < 1),
{ threshold: [1] }
);

observer.observe(el);

function isAboveStickyElement(stickyElement) {
  if (stickyElement.getBoundingClientRect().top > 170) {
    return true;
  }
  return false;
}
var lastScrollTop = 0;

window.onscroll = function() {

  var currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
  var currentStickyThirdLvlElement = document.querySelector('div.sticky-third-lvl');
  var allStickyThirdLvlElements = document.querySelectorAll('div.sticky-third-lvl');
  if (isSticky(currentStickyThirdLvlElement)) {
    currentStickyThirdLvlElement.classList.add('border-bottom');
  }
  else {
    if (currentStickyThirdLvlElement.id != "2")
    currentStickyThirdLvlElement.classList.remove('border-bottom');

  }
  var stickyElements = findVisibleButtonElementsInViewport();
  var liParent = undefined;
  if (lastScrollTop < currentScrollTop) {
    var expandedChildOfStickyElement = findFirstElementWhichIsExpanded(currentStickyThirdLvlElement, stickyElements);
    if (expandedChildOfStickyElement != undefined && getDistanceBetweenElements(currentStickyThirdLvlElement, expandedChildOfStickyElement) < 20) {
        currentStickyThirdLvlElement.classList.remove('sticky-third-lvl');
        expandedChildOfStickyElement.parentElement.classList.add('sticky-third-lvl');
    }
  }
  else {
    // on scroll up
    // set the most upward element as sticky element:
    
    // stickyElements[0].parentElement.classList.add('sticky-third-lvl');
    if (isAboveStickyElement(currentStickyThirdLvlElement)) {
      
      // The window is scrolled above the sticky element.
      // currentStickyThirdLvlElement
      // find the ul-parent of most upward button:
      currentStickyThirdLvlElement.classList.remove('sticky-third-lvl');
      if (stickyElements[0].id == "0") {
        stickyElements[0].parentElement.classList.add('sticky-third-lvl');
      }
      else {
        liParent = getFirstParentElementWithTagName(stickyElements[0], "UL").parentElement;
        liParent.children[0].classList.add('sticky-third-lvl');
      }
    }   
  }
  lastScrollTop = currentScrollTop;
};

function isSticky(stickyElement) {
  var rect = stickyElement.getBoundingClientRect();
  if (rect.top == 155) {
    return true;
  }
  return false;
}

function addOrRemoveBottomBorderClass(divElementList) {
  for (var i = 0; i < divElementList.length; i++) {
    if (isSticky(divElementList[i])) {
      divElementList[i].classList.add('border-bottom');
    }
    else {
      if (divElementList[i].id != "2") {
        divElementList[i].classList.remove('border-bottom');
      }
    }
  }
}

function getDistanceBetweenElements(element1, element2) {
    var rect1 = element1.getBoundingClientRect();
    var rect2 = element2.getBoundingClientRect();

    return Math.abs(rect1.bottom - rect2.top);
}

function isInViewport(element) {
    var rect = element.getBoundingClientRect();
    var html = document.documentElement;
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || html.clientHeight) &&
        rect.right <= (window.innerWidth || html.clientWidth)
    );
}

function findVisibleButtonElementsInViewport() {
  var listElements = Array.from(document.querySelectorAll('.sticky-element-button')).filter(function(element) {
    return window.getComputedStyle(element).display !== 'none' && element.parentElement.parentElement.style.display != "none";
  });
    var visibleElements = [];
    for (var i = 0; i < listElements.length; i++) {
        if (isInViewport(listElements[i])) {
            visibleElements.push(listElements[i]);
        }
    }
    return visibleElements;
}

function findFirstElementWhichIsExpanded(stickyElement, listOfVisibleElements) {
  var stickyElementLayerNumber = Number(stickyElement.id);
  var directChildOfStickyElement = undefined;
  
  for (var i = 1; i < listOfVisibleElements.length; i++) {
    if (isExpanded(listOfVisibleElements[i])) {
      return listOfVisibleElements[i];
    }
  }
  return undefined;
}

function isExpanded(element) {
  if (element.tagName == "BUTTON") {
    return element.parentElement.nextElementSibling.style.display != "none" && element.parentElement.nextElementSibling.children[0].style.display != "none";
  }
}


function removeLastDivFromUlOfLevelOne () {
  var ulElements = document.querySelectorAll("#hi ul.\\1");
  for (var i = 0; i < ulElements.length; i++) {
    if (ulElements[i].nextElementSibling == undefined) {
      ulElements[i].children[0].children[1].style.display = "none";
    }
  }
}

function findRootElement(element) {
  var parentElement = element;
  while ((parentElement.id != "0" || parentElement.tagName != "UL")) {
        parentElement = parentElement.parentElement;
      }
  return parentElement;
}

function getHeadingAndDescription(element, stringToConcatanate) {
  for (var i = 0; i < element.children.length; i++) {
    if (element.children[i].tagName == "BUTTON") {
      stringToConcatanate += "<h6>" + element.children[i].textContent + "</h6>" + "<br />";
    }
    if (element.children[i].tagName == "P") {
      stringToConcatanate += "<p>" + element.children[i].textContent + "</p>" + "<br />";
    }
  }
  return stringToConcatanate;
}

function createDivElement(id){
  var newDivElement = document.createElement("div");
  newDivElement.className = "hr";
  newDivElement.style.display = "none";
  newDivElement.id = id;

  return newDivElement;
}

function depthFirstSearch(element, func) {
  var stack = [element];

  while (stack.length > 0) {
     var currentElement = stack.pop();
      func(currentElement);

      var children = currentElement.children;
      for (var i = children.length - 1; i >= 0; i--) {
          stack.push(children[i]);
      }
  }
}

function hideLeftBorder(element) {
  if (element.tagName == "UL" && element.id == "0") {
    element.querySelector("li").classList.remove("border-left");
  }
}


function hideElementExceptForFirstLayer(element) {
  if (element.tagName === "IMG" && element.id !== '0') {
    showDirectionOfArrow(element, "down");
  }

  if (element.classList.contains("wrapper")) {
    return;
  }
  if (Number(element.id) > 0) {
    element.style.display = "none";
  }
  hideLeftBorder(element);
}

function depthFirstWalkForParagraphs() {
  var divContainerOfCriteriaCatalog = document.getElementById("hi");
  var childElements = divContainerOfCriteriaCatalog.children;
  var queue = Array.from(childElements);
  var elementFromQueue = undefined;
  var firstUlAsChildOfLi = undefined;
  while (queue.length > 0) {
    elementFromQueue = queue.shift();
    // bring child-elements into queue:
    queue = addElementsToArray(queue, elementFromQueue.children);
    if (elementFromQueue.tagName == "P" && Number(elementFromQueue.id) < 3) {
      childUlFromParagraph = returnFirstAppearanceOfElementWithTagName(elementFromQueue, "UL");
      if (childUlFromParagraph != "") {
        newLiElement = document.createElement("li");
        newLiElement.prepend(elementFromQueue);
        childUlFromParagraph.prepend(newLiElement);
        // remove the paragraph from its current position:
        parentOfParagraph = elementFromQueue.parentElement;
        parentOfParagraph.removeChild(elementFromQueue);
      }
      else {
        parentOfParagraph = elementFromQueue.parentElement;
        parentOfParagraph.removeChild(elementFromQueue);
        
        elementFromQueue.id = Number(elementFromQueue.id) + 1;

        newUlElement = document.createElement("ul");
        newUlElement.id = Number(elementFromQueue.id);
        newUlElement.style.display = "none";
        if (newUlElement.id == 1) {
          newUlElement.className = "absolute-horizontal-position-lvl-one";
        }
        else if (newUlElement.id == 2) {
          newUlElement.className = "absolute-horizontal-position-lvl-two";
        }
        newLiElement = document.createElement("li");
        newLiElement.id = Number(elementFromQueue.id);

        prevNewDiv = createDivElement(Number(elementFromQueue.id));
        nextNewDiv = createDivElement(Number(elementFromQueue.id));

        newLiElement.prepend(prevNewDiv);
        newLiElement.appendChild(elementFromQueue);
        newLiElement.appendChild(nextNewDiv);
        newUlElement.prepend(newLiElement);
        firstUlAsChildOfLi = returnFirstAppearanceOfElementWithTagName(parentOfParagraph, "UL");
        if (firstUlAsChildOfLi != "") {
          parentOfParagraph.insertBefore(newUlElement, firstUlAsChildOfLi);
        }
        else {
        parentOfParagraph.prepend(newUlElement);
      }
    }
  }
}
}

function modifyCatalogToBeShownInOneElement() {
  var elementsToBeSearched = document.getElementById("hi").getElementsByTagName("*");
  for (var i = 0; i < elementsToBeSearched.length; i++) {
    
    if (elementsToBeSearched[i].tagName == "UL" && Number(elementsToBeSearched[i].id) >= 2) {
      var textForCombinedElement = "";
      var textCombinedConcatenated = "";
      var aggregatedTags = "";
      var aggregatedTopicIds = "";
      var liDescendants = elementsToBeSearched[i].querySelectorAll('li');                
      // first add the content of the element itself:
       
       if (liDescendants[0] != undefined) {
        var firstParagraph = liDescendants[0].getElementsByTagName("p");
        if (firstParagraph != null) {
          textCombinedConcatenated += firstParagraph[0].innerHTML;
        }
       }

      var ulChildElements = elementsToBeSearched[i].querySelectorAll('ul');
      window.textForCombinedElement = "";
      for (var j = 0; j < ulChildElements.length; j++) {
        if (Number(ulChildElements[j].id) == 3) {
          textForCombinedElement = ulChildElements[j].innerHTML
          depthFirstSearch(ulChildElements[j], aggregateAndStyleText);
          firstLiChildren = returnFirstAppearanceOfElementWithTagName(ulChildElements[j], "LI");
          if (firstLiChildren != "") {
            aggregatedTags += ", " + firstLiChildren.getAttribute("tags");
            aggregatedTopicIds += "," + firstLiChildren.getAttribute("topicId");
          }
          
          textForCombinedElement = textForCombinedElement.replace(/(\s*\n)+/g, '\n');
          textCombinedConcatenated += textForCombinedElement;
        }
        if (Number(ulChildElements[j].id) > 3) {
          ulChildElements[j].remove();
        }
      }
      //debugger;
      for (var j = 0; j < liDescendants.length; j++) {
        // }
        if (Number(liDescendants[j].id) >= 3) {
          if (liDescendants[j].getAttribute("aggregatedText") != "true") {
            liDescendants[j].remove();
          }
          
        }
        if (Number(liDescendants[j].id) == 2) {
        
          paragraphToBeDeleted = liDescendants[j].querySelector("p")
          if (paragraphToBeDeleted.getAttribute("aggregatedText") != "true") {
            
            if (paragraphToBeDeleted.parentElement.parentElement.getElementsByTagName("ul").length > 0) {
              paragraphToBeDeleted.remove();
            }
            else {
              var newUlElement = document.createElement("ul");
              newUlElement.id = "3";
              newUlElement.style.display = "none";
              var newLiElement = document.createElement("li");
              newLiElement.id = "3";
              newLiElement.style.display = "none";
              newLiElement.setAttribute("aggregatedText", true);
              var newParagraphElement = document.createElement("p");
              newParagraphElement.classList.add("paragraph-deeper-level")
              newParagraphElement.setAttribute("topicId", paragraphToBeDeleted.getAttribute("topicId"))
              newParagraphElement.setAttribute("tags", paragraphToBeDeleted.getAttribute("tags"))
              newLiElement.setAttribute("aggregatedText", true);
              newParagraphElement.style.display = "none";
              newParagraphElement.style.fontSize = "18px";
              newParagraphElement.id = "3";
              newParagraphElement.innerHTML = paragraphToBeDeleted.innerHTML;
              paragraphToBeDeleted.parentElement.append(newUlElement);
              paragraphToBeDeleted.parentElement.children[paragraphToBeDeleted.parentElement.children.length-1].append(newLiElement);
              paragraphToBeDeleted.parentElement.children[paragraphToBeDeleted.parentElement.children.length-1].children[0].append(newParagraphElement)

              paragraphToBeDeleted.remove();
            }
          }
        }
        
      }

      var newLiElement = document.createElement("li");
      var newParagraphElement = document.createElement("p");
      newLiElement.style.display = "none";
      newParagraphElement.style.whiteSpace = "pre-line";
      newParagraphElement.setAttribute("aggregatedText", "true")
      newParagraphElement.innerHTML = window.textForCombinedElement;
      newParagraphElement.style.fontSize = "18px";
      newParagraphElement.setAttribute("topicId", aggregatedTopicIds);
      newParagraphElement.setAttribute("tags", aggregatedTags);
      newLiElement.id = "3";
      newLiElement.setAttribute("aggregatedText", "true")
      newParagraphElement.id = "3";
      newLiElement.appendChild(newParagraphElement);
      var firstULElement = elementsToBeSearched[i].querySelector('ul')
      if (firstULElement != null) {
        firstULElement.id = "3";
        firstULElement.appendChild(newLiElement);
        
      }
      
    }
  }
}

function aggregateAndStyleText(element) {
  var textContent = "";
  if (element.tagName == "BUTTON") {
      textContent = "<span style='font-size: 22px;'>" + element.textContent + "</span>";
  }
  if (element.tagName == "P") {
      textContent = "<div style='margin-left: 40px;'>" + element.innerHTML + "</div>";
  }
  window.textForCombinedElement += textContent;
}

function showAllElementsUntilRoot(element) {
  var parentElement = element;
  while (parentElement.id != "0" || parentElement.tagName != "UL") {
    showElement(parentElement);
    parentElement = parentElement.parentElement;
  }
}

function searchFullText(searchString) {    
  var elementsToBeSearched = document.querySelectorAll("#hi *");
  var foundElements = [];
  foundULelements = [];
  for (var i = 0; i < elementsToBeSearched.length; i++) {
    if (elementsToBeSearched[i].textContent.includes(searchString)) {
      // The search string is contained in the text content of the element
      if (elementsToBeSearched[i].tagName == "BUTTON" || elementsToBeSearched[i].tagName == "P") {
        foundElements.push(elementsToBeSearched[i]);
      }
    }
  }
  if (foundElements.length > 0) {
    // call a function, which will reset the criteriaCatalog to the original state
    resetCriteriaCatalog();
    // show all found elements
    for (var i = 0; i < foundElements.length; i++) {
      foundElements[i].innerHTML = foundElements[i].innerHTML.replace(new RegExp(searchString, 'g'), '<mark>$&</mark>');
      var rootElement = findRootElement(foundElements[i]);
      depthFirstWalk(rootElement, foundElements[i]);  
    }
  }
  openHeadingsForLayers();
}

function handleOptionSelected() {
  // Code to be executed when an option is selected
  var selectedOption = document.getElementById("tags").value;
  // search all HTML, which are childs of div-element with id "container-criteria-catalog-details"
  // var elementsToBeSearched = document.getElementById("hi").getElementsByTagName("*");
  var elementsToBeSearched = document.querySelectorAll("#hi *");
  var foundElements = [];
  foundULelements = [];
  for (var i = 0; i < elementsToBeSearched.length; i++) {
    // if the element has the attribute "tags" and the value of the attribute is equal to the selected option
    if (elementsToBeSearched[i].hasAttribute("tags") && elementsToBeSearched[i].getAttribute("tags").includes(selectedOption)) {
      // show the element
      // add the element to the found elements:
      parentElement = elementsToBeSearched[i];
      while ((parentElement.id != "0" || parentElement.tagName != "UL")) {
        parentElement = parentElement.parentElement;
      }
      resetCriteriaCatalog();
      depthFirstWalk(parentElement, elementsToBeSearched[i]);
    }
  }
  var numberOfLayersShown = checkHowManyLayersAreShown();
  if (numberOfLayersShown >= 1) {
    document.getElementById("criterias").style.display = "block";
  }
  if (numberOfLayersShown >= 2) {
    document.getElementById("requirementsAndRuleExamples").style.display = "block";
  }
}

function openHeadingsForLayers() {
var numberOfLayersShown = checkHowManyLayersAreShown();
  if (numberOfLayersShown >= 1) {
    document.getElementById("criterias").style.display = "block";
  }
  else {
    document.getElementById("criterias").style.display = "none";
  }
  if (numberOfLayersShown >= 2) {
    document.getElementById("requirementsAndRuleExamples").style.display = "block";
  }
  else {
    document.getElementById("requirementsAndRuleExamples").style.display = "none";
  }
}

function getLiAndUlElements(element) {
var array = Array.prototype.slice.call(element.children);
var ulAndLiElements = array.filter(function(element) {
  return element.tagName === 'UL' || element.tagName === 'LI';
});
return ulAndLiElements;
}

function addElementsToArray(arrayToBeAddedTo, arrayToAdd) {
for (var i = 0; i < arrayToAdd.length; i++) {
  arrayToBeAddedTo.push(arrayToAdd[i]);
}
return arrayToBeAddedTo;
}

function returnFirstAppearanceOfElementWithTagName(element, tagName) {
var childElements = element.children;
for (var i = 0; i < childElements.length; i++) {
  if (childElements[i].tagName == tagName) {
    return childElements[i];
  }
}
return "";
}

function depthFirstWalkForModification(element) {

var aggregatedString = ""; 
var liElement = ""
var newUlLiElements = [];
var array = Array.prototype.slice.call(element.children);
var ulAndLiElements = array.filter(function(element) {
  return element.tagName === 'UL' || element.tagName === 'LI';
});
liUlElements = []
liUlElements = addElementsToArray(liUlElements, ulAndLiElements)
while (liUlElements.length > 0) {
  
  liUlElement = liUlElements.pop();
  if (liUlElement.tagName == "LI" && Number(liUlElement.id) > 2) {
    liElement = liUlElement;
    aggregatedString += returnFirstAppearanceOfElementWithTagName(liElement, "BUTTON").textContent + "<br />"
    aggregatedString += returnFirstAppearanceOfElementWithTagName(liElement, "P").textContent + "<br />"
  }
  newUlLiElements = getLiAndUlElements(liUlElement);
  liUlElements = addElementsToArray(liUlElements, newUlLiElements);
}
return aggregatedString;
}

function depthFirstWalk(rootElement, target) {
var childElements = rootElement.children;
var buttonForLI = undefined;
for (var i = 0; i < childElements.length; i++) {
  var childElement = childElements[i];
  // Perform your desired operation on the child element here
  // console.log(childElement);
  // check if the childElement is a ancestor of target
  
  if (checkIfAncestor(childElement, target)) {
    if (childElement.tagName == "LI") {
      buttonForLI = childElement.querySelector("button");
      openChildLayer(buttonForLI);
    }
      if (Number(childElement.id) <= Number(target.id)) {
        openChildLayer(childElement);
      depthFirstWalk(childElement, target);
    }
  }
  else {
    openChildLayer(childElement);
  }
}
}

function checkIfAncestor(element, target) {
var childElements = [];
childElements.push(element);
while (childElements.length > 0) {
  var childElement = childElements.pop();
  if (childElement == target) {
    return true;
  }
  else {
    var grandChildElements = childElement.children;
    for (var i = 0; i < grandChildElements.length; i++) {
      childElements.push(grandChildElements[i]);
    }
  }
}
return false;
}

function showHeading(element){
if (element.tagName == "UL") {
  element.style.display = "block";
  for (var i = 0; i < element.children.length; i++) {
    if (element.children[i].tagName == "LI") {
      element.children[i].style.display = "block";
      element.children[i].getElementsByTagName("div")[0].style.display = "block";
      element.children[i].getElementsByTagName("div")[0].style.marginLeft = "0px";
    }
  }
}
if (element.tagName == "LI") {
  element.style.display = "block"; 
  element.children.getElementsByTagName("hr")[0].style.display = "block";
}
else if (element.tagName == "HR") {
  element.style.display = "block";
}
if (element.tagName == "P" && element.id == "0") {
  element.style.display = "block";
}
}

function showHeadingAndDescription(element) {
if (element.tagName == "UL") {
  element.style.display = "block";
  for (var i = 0; i < element.children.length; i++) {
    if (element.children[i].tagName == "LI") {
      element.children[i].style.display = "block";
      element.children[i].getElementsByTagName("p")[0].style.display = "block";
      element.children[i].getElementsByTagName("div")[0].style.display = "block";
    }
  }
}
if (element.tagName == "LI" || element.tagName == "DIV") {
  element.style.display = "flex";
  element.getElementsByTagName("p")[0].style.display = "block";
}
}


function showFullTextOfHeading(element) {
var fullHeading = element.getAttribute("text");
element.textContent = fullHeading;
}
function showPreviewTextOfHeading(element) {
if (element.textContent.length > 80) {
  element.textContent = element.getAttribute("text").substring(0, 80) + "...";
}
}

function showElement(element) {
if (element.tagName == "UL" || element.tagName == "LI" || element.tagName == "DIV" || element.tagName == "P") {
  element.style.display = "block";
}
else {
  if (element.tagName != "MARK") {
    element.style.display = "inline";
  }
}
}

function checkHowManyLayersAreShown() {
// find the li-element with the highest id
var elementsToBeSearched = document.getElementById("hi").getElementsByTagName("*");
// check the visible UL-elements to check, how many layers are shown:
var liElements = Array.from(elementsToBeSearched).filter((element) => {return element.tagName == "LI"})
var layersExpanded = 0;
for (var i = 0; i < liElements.length; i++) {
  if ((liElements[i].style.display == "block" || liElements[i].style.display == "") && Number(liElements[i].id) > layersExpanded) {
    var parentElement = liElements[i];
    var parentIsNone = false;
    
    while (Number(parentElement.parentElement.id) >= 0) {

      if (parentElement.parentElement.style.display == "none") {
        parentIsNone = true;
      }
      parentElement = parentElement.parentElement;
    }
    if (!parentIsNone) {
    layersExpanded += 1;
    }
  }
}
return layersExpanded;
}

function getFirstParentElementWithTagName(element, tagName) {
var parentElement = element;
while (parentElement.tagName != tagName) {
  parentElement = parentElement.parentElement;
}
return parentElement;
} 

function getAllChildElementsWithTagName(element, tagName) {
var childElements = element.children;
var elements = [];
for (var i = 0; i < childElements.length; i++) {
  if (childElements[i].tagName == tagName) {
    elements.push(childElements[i]);
  }
}
return elements;
}

function removeMarkTagsFromText(element) {
if (element.tagName == "BUTTON" || element.tagName == "P") {
  var textContentOfNode = element.innerHTML;
  textContentOfNode = textContentOfNode.replace(/<mark>/g, "");
  textContentOfNode = textContentOfNode.replace(/<\/mark>/g, "");
  element.innerHTML = textContentOfNode;
}
}

function showDirectionOfArrow(imgElement, direction) {
if (direction == "up") {
  imgElement.src = pathToArrowUpImg;
}
else {
  imgElement.src = pathToArrowDownImg;
}
}

function openChildLayer(element) {
if (element == null) {
  return;
}
if (element.tagName == "BUTTON" && element.id != "0") {
  showFullTextOfHeading(element);
  addOrRemoveBottomBorder(element);
}
showElement(element);
var parentOfClickedElement = getFirstParentElementWithTagName(element, "UL")
var childUlElements = [];
if (element.id == "2") {
  if (element.display == "none") {
    element.style.display = "block";
  }
  childUlElements = element.parentElement.parentElement.querySelectorAll("ul ul");
  if (childUlElements.length == 0) {
    childUlElements = element.parentElement.parentElement.parentElement.querySelectorAll("ul ul");
  }
  if (childUlElements.length > 0) {
    childUlElements[0].style.display = "block";
    showElement(childUlElements[0].querySelectorAll("li li")[0]);
    showElement(childUlElements[0].querySelectorAll("li li")[0].children[0]);
    showElement(childUlElements[0].querySelectorAll("li li p")[0]);
    var layerNumberOfClickedElement = Number(element.id);
    var childElementsOfButton = element.children;
    if (childElementsOfButton.length > 0) {
      if (Number(element.id) > 0) {
      childElementsOfButton[0].src = pathToArrowUpImg;
      }
    }
  }
}
else {
  if (parentOfClickedElement.id == "0" && parentOfClickedElement.tagName == "UL") {
    parentOfClickedElement.children[0].classList.add("border-left");
  }
  
  var layerNumberOfClickedElement = Number(element.id);
  imageInButtonElement = element.previousElementSibling;
  if (imageInButtonElement != null) {
    showElement(imageInButtonElement);
  }
  
  var nextLayerElementsUL = Array.from(element.parentElement.parentElement.children).filter((element) => {return element.tagName == "UL"});
  var childOfLi = undefined;
  var buttonElementInLi = undefined;
  var paragraphElementInLi = undefined;
  var divElements; 
  var imageInButtonElement;
  for (var i = 0; i < nextLayerElementsUL.length; i++) {
    nextLayerElementsUL[i].style.display = "block";

    // get the li-elements, which are childs of the ul:
    var childsOfUL = nextLayerElementsUL[i].children;
    var nextLayerElementsLI = Array.from(childsOfUL).filter((element, layerNumberOfClickedElement) => {
      if (Number(element.id) > layerNumberOfClickedElement && element.tagName == "LI") {
        return element;
      } 
    })
    
    for (var j = 0; j < nextLayerElementsLI.length; j++) {
      showElement(nextLayerElementsLI[j]);
      childOfLi = nextLayerElementsLI[j].children;
      
      buttonElementInLi = Array.from(childOfLi[0].children).filter((element) => {return element.tagName == "BUTTON"})
      if (buttonElementInLi.length > 0) {
        showElement(buttonElementInLi[0]);
        imageInButtonElement = buttonElementInLi[0].previousElementSibling;
        showElement(imageInButtonElement);
      }
      paragraphElementInLi = Array.from(childOfLi).filter((element) => {return element.tagName == "P"})
      if (paragraphElementInLi.length > 0) {
        paragraphElementInLi[0].style.display = "block";
        try {
        paragraphElementInLi[0].nextElementSibling.style.display = "block";
        paragraphElementInLi[0].previousElementSibling.style.display = "block";
        }
        catch {
          console.log("Error");
        
        }
      }
      if (i < nextLayerElementsUL.length - 1) {
        if (nextLayerElementsLI[j].getElementsByTagName("div").length > 0) {
          if (nextLayerElementsLI[j].parentElement.nextElementSibling != null && nextLayerElementsLI[j].id != "0") {
            divElements = getAllChildElementsWithTagName(nextLayerElementsLI[j], "DIV")
            for (var k = 0; k < divElements.length; k++) {
              divElements[k].style.display = "block";
            }
          }
        }
      }
    }
  }

}
}

function setArrowUpOrDown(element, directionStr) {
if (directionStr == "up") {
  element.src = pathToArrowUpImg;
}
else {
  element.src = pathToArrowDownImg;
}
}

function addOrRemoveBottomBorder(buttonElement) {
// check if the child-elements of button are hidden
// then it will be opened and the border-bottom will be added
var liParentElement = getFirstParentElementWithTagName(buttonElement, "LI");
var divParent = getFirstParentElementWithTagName(buttonElement, "DIV");
var imgElement = divParent.querySelector("img");
var firstChildUlElement = liParentElement.querySelector("ul");
var firstChildLiElement = firstChildUlElement.querySelector("li");
var firstButtonOrParagraphElement = firstChildLiElement.querySelector("button, p");
if (firstChildUlElement.style.display == "none" || firstChildLiElement.style.display == "none") {
  if (divParent.id == "2") {
    divParent.classList.add("border-bottom");
  }
  setArrowUpOrDown(imgElement, "up");
  showElement(buttonElement)
}
else {
  if (divParent.id == "2") {
    divParent.classList.remove("border-bottom");
  }
  setArrowUpOrDown(imgElement, "down");
}

}


function closeChildLayer(element) {
if (element.tagName == "BUTTON" && element.id != "0") {
  showPreviewTextOfHeading(element);
  addOrRemoveBottomBorder(element);
}
var parentOfClickedElement = element.parentElement.parentElement.parentElement;

hideLeftBorder(parentOfClickedElement);

var layerNumberOfClickedElement = Number(element.id);
var childElements = element.parentElement.parentElement.children;
if (layerNumberOfClickedElement > 0) {
  element.previousElementSibling.src = pathToArrowDownImg;
}

var nextLayerElementsUL = Array.from(childElements).filter((element) => {return element.tagName == "UL"});
for (var i = 0; i < nextLayerElementsUL.length; i++) {
  nextLayerElementsUL[i].style.display = "none";

  // get the li-elements, which are childs of the ul:
  var childsOfUL = nextLayerElementsUL[i].children;
  var nextLayerElementsLI = Array.from(childsOfUL).filter((element, layerNumberOfClickedElement) => {
    if (Number(element.id) > layerNumberOfClickedElement && element.tagName == "LI") {
      return element;
    } 
  })

  for (var j = 0; j < nextLayerElementsLI.length; j++) {
    nextLayerElementsLI[j].style.display = "none";
    if (nextLayerElementsLI[j].getElementsByTagName("div").length > 0) {
      nextLayerElementsLI[j].getElementsByTagName("div")[0].style.display = "block";
    }
  }
}
}


function resetCriteriaCatalog() {
// search all HTML, which are childs of div-element with id "container-criteria-catalog-details"
depthFirstSearch(document.getElementById("hi"), removeMarkTagsFromText);
depthFirstSearch(document.getElementById("hi"), hideElementExceptForFirstLayer);
document.getElementById("criterias").style.display = "none";
document.getElementById("requirementsAndRuleExamples").style.display = "none";
// remove all current sticky-elements:
var stickyElements = document.querySelectorAll('.sticky-third-lvl');
for (var i = 0; i < stickyElements.length; i++) {
  stickyElements[i].classList.remove('sticky-third-lvl');
}
var firstLevelDivs = document.getElementById("hi").querySelectorAll('div[id="0"]');
for (var i = 0; i < firstLevelDivs.length; i++) {
  firstLevelDivs[i].classList.add("sticky-third-lvl");
}
}

var numberOfOpenElementsPerLayer = {};
function showOrHide(event, element) {
// check if element if child-elements should be expoanded or collapsed
var childElements = element.parentElement.parentElement.children; 
var filteredChildElements = Array.from(childElements).filter((element) => {return element.tagName == "UL"}); 
if (filteredChildElements.length == 0) {
  return;
}
if (filteredChildElements[0].style.display == "none") {
  openChildLayer(element);
}
else {
  closeChildLayer(element);
}

var foundULs = 0;
var foundChilds = [];
var firstElementSkipped = false;
// if the parent of the parent of the clicked element is a div, then the clicked element is
// a root element and its text should be displayed in grey.
var displayPInGray = false;
if (element.parentElement.parentElement.tagName == "DIV") {
  displayPInGray = true;
  pElements = element.getElementsByTagName("p");
}
  openHeadingsForLayers();
  if (event.stopPropagation) {
    event.stopPropagation();   // W3C model
  } else {
    event.cancelBubble = true; // IE model
  }
}

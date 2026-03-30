/*
  AUTHOR: 
    -> Omar Hossam
  
  LICENSE: 
    -> MIT
  
  GitHub repo:
    -> https://github.com/omar-hossam/QalamJS
  
  This mini framework is created by me and it's open source on GitHub :) 
*/


// CLASS
function togClass(el, val) {
  if (typeof(el) === "string") {
    [...document.querySelectorAll(el)].forEach(e => e.classList.toggle(val))
    return;
  }
  el.classList.toggle(val)
}

function addClass(el, val) {
  if (typeof(el) === "string") {
    [...document.querySelectorAll(el)].forEach(e => e.classList.add(val))
    return;
  }
  el.classList.add(val)
}

function remClass(el, val) {
  if (typeof(el) === "string") {
    [...document.querySelectorAll(el)].forEach(e => e.classList.remove(val))
    return;
  }
  el.classList.remove(val)
}

// ATTRIBUTES
function togAttr(el, attr) {
  if (typeof(el) === "string") {
    [...document.querySelectorAll(el)].forEach(e => e.toggleAttribute(attr))
    return;
  }
  el.toggleAttribute(attr)
}

function setAttr(el, attr, val) {
  if (typeof(el) === "string") {
    [...document.querySelectorAll(el)].forEach(e => e.setAttribute(attr, val))
    return;
  }
  el.toggleAttribute(attr, val)
}

function log(val) { console.log(val) }

// APP OBJECTS MUST START WITH 'my' e.g. 'myApp', 'myProgram', 'mySystem' etc..
const appObjects = Object.keys(window).filter(ob => ob.startsWith("my"));
const forElements = [...document.querySelectorAll("[q-for]")];

const textElements = [...document.querySelectorAll("[q-text]")];

let alreadyTrackedHText = [];

const isNumber = (str) => !isNaN(str) && !isNaN(parseFloat(str));

function setElText(el, forArrayValue="", forArrayVarName="") {
  if (forArrayValue) {
    let qText = el.getAttribute("q-text")
    let result = qText.replace(forArrayVarName, forArrayValue).replaceAll("'", "").replaceAll('"', "")
    
    el.textContent = result;
    return;
  }
  let qText = el.getAttribute("q-text").split("").map(str => str.trim()).filter(char => char !== "");
  let final = "";
  let operators = ["+", "-", "*", "/", "%", "**"] 
  
  let variables = []
  let varName = ""
  
  for (let i = 0; i < qText.length; i++) {
    if (!isNumber(qText[i]) && !operators.includes(qText[i])) { 
      varName += qText[i]
    } else { 
      if (varName) final += getVariableValue(varName); varName = ""; 
      final += qText[i]
    }

  }
  if (varName) final += getVariableValue(varName);
  if (!isNumber(final[0]) && !isNumber(final[final.length-1])) {
    el.textContent = final
    console.log(el.outerHTML)
  } else {
    el.textContent = new Function("return " + final)();
  }
}

function getVariableValue(varName) {
  if (varName.includes(".") 
      && appObjects.includes(varName.split('.')[0])
  ) {
    return window[varName.split('.')[0]][varName.split('.')[1]]
  }
}

forElements.forEach(el => {
  const value = el.getAttribute("q-for").split("in").map(str => str.trim()); // split by in, remove whitespaces from start and end only
  const children = [...el.children];
  el.innerHTML = '';
  
  if (isNumber(value[0])) { 
    
    let numeralFor = []
    
    if (value[1].includes("by")) { // for 1 in 10 by 2
      const arr = [...value[1].split("by")]
      numeralFor = [...value[0], ...arr].map(s => Number(s));
    } else {
      numeralFor = [...value, ..."1"].map(s => Number(s));  
    }
    // for 1 in 10
    // log (numeralFor)
    
    for (let i = numeralFor[0]; i < numeralFor[1]; i += numeralFor[2]) {
      children.forEach(child => {
        el.innerHTML += child.outerHTML
      })
    }
    
    
  } else { // loop through an array
    const elObj = { 
      name: value[1].split('.')[0],
      varName: value[1].split('.')[1] 
    }
    // hobby in hobbies 
    // -- here the value of `hobbies` is the `targetValue`
    const targetValue = window[elObj.name][elObj.varName]
    
    log(targetValue)
    for (let i = 0; i < targetValue.length; i++) {
      children.forEach(child => {
        setElText(child, forArrayValue=targetValue[i], forArrayVarName=value[0])
        alreadyTrackedHText.push(child)
        el.innerHTML += child.outerHTML;
      })
    }
  }
})

textElements.filter(e => !alreadyTrackedHText.includes(e)).forEach(e => setElText(e))


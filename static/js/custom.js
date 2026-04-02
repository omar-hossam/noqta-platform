/*
  AUTHOR: 
    -> Omar Hossam
  
  LICENSE: 
    -> MIT
  
  GitHub repo:
    -> https://github.com/omar-hossam/petit-js
  
  This mini script is part of Petit.js created by me, it's open source on GitHub :) 
*/

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

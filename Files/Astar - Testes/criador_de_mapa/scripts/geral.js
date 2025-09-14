const canvas = document.querySelector("canvas")
const ctx = canvas.getContext("2d")
const $M=(arg)=>document.querySelector(arg)

let mapa = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

var lembrar = []
var atualMouse = [0,0]//x,y

var desenhando = false
var operation = 0

var ferramenta = 1

function getScale(e){
    x = e.pageX-canvas.offsetLeft
    y = e.pageY-canvas.offsetTop
    let newX = x*canvas.width/canvas.offsetWidth
    let newY = y*canvas.height/canvas.offsetHeight
    return {
        x:Math.floor(newX),
        y:Math.floor(newY)
    }
}
function operationState(op, obj){
    var divs = document.querySelectorAll(".items div")
    divs.forEach(div=>{
        div.classList.remove("selected")
    })
    if(obj.parentElement == divs[0].parentElement){
        obj.classList.add("selected")
    }
    operation = op
}

function setFerramenta(number, obj){
    ferramenta = number
    var divs = document.querySelectorAll(".type div")
    divs.forEach(div=>{
        div.classList.remove("selected")
    })
    obj.classList.add("selected")
}

function update(){
    var width = $M("#width").value || 1
    var height = $M("#height").value || 1

    if(height>mapa.length){
        var nova_linha = []
        for(let i = 0; i<mapa[0].length;i++){
            nova_linha[i] = 0
        }
        mapa[mapa.length] = nova_linha
    }
    if(height<mapa.length){
        mapa.splice(mapa.length-1,1)
    }
    
    if(width>mapa[0].length){
        for(var i = 0;i<mapa.length;i++){
            mapa[i].push(0)
        }
    }
    if(width<mapa[0].length){
        for(var i = 0;i<mapa.length;i++){
            mapa.splice(mapa[0].length-1,1)
        }
    }

    canvas.width = width
    canvas.height = height
    linha = 0
    coluna = 0
    mapa.forEach(line=>{
        coluna = 0
        line.forEach(data=>{
           if(data == 1){
                ctx.fillStyle = 'black'
                ctx.fillRect(coluna,linha,1,1)
            }
            coluna++
        })
        linha++
    })
    
    //start
    startX = $M("#iniciox").value
    startY = $M("#inicioy").value
    ctx.fillStyle = 'blue'
    if(operation!=1){
        ctx.fillRect(startX,startY,1,1)
    }
    //finish
    finishX = $M("#fimx").value
    finishY = $M("#fimy").value
    ctx.fillStyle = 'red'
    if(operation!=2){
        ctx.fillRect(finishX,finishY,1,1)
    }
    //onde o mouse foca
    ctx.globalAlpha = 0.5
    ctx.fillStyle=(operation==1)?'blue':(operation==2)?'red':'gray'
    ctx.fillRect(atualMouse[0],atualMouse[1],1,1)
    ctx.globalAlpha =1
    //linhas
    if(lembrar.length==2){
        var x1 = lembrar[0].x
        var y1 = lembrar[0].y
        var x2 = lembrar[1].x
        var y2 = lembrar[1].y
        var w = x2-x1
        var h = y2-y1
        w+=(w<0)?0:1
        h+=(h<0)?0:1
        if( operation == 3){
            ctx.fillStyle = 'gray'
            ctx.fillRect(x1,y1,1,h)
        }
        if( operation == 4){
            ctx.fillStyle = 'gray'
            ctx.fillRect(x1,y1,w,1)
        }
        if(operation == 5){
            ctx.fillStyle = 'gray'
            //linha top
            ctx.fillRect(x1,y1,w,1)
            //linha bottom
            ctx.fillRect(x1,y2,w,1)
            //linha left
            ctx.fillRect(x1,y1,1,h)
            //linha Right
            ctx.fillRect(x2, y1, 1, h)
        }
    }
    
    
    titulo = `X: ${atualMouse[0]}/ Y:${atualMouse[1]}`
    if(lembrar.length==2){
        titulo+=' '
        var w = Math.abs(lembrar[1].x-lembrar[0].x)
        var h = Math.abs(lembrar[1].y-lembrar[0].y)
        if(operation == 4 || operation==5){//horizontal
            titulo+='- width:'+w
        }
        if(operation == 3 || operation==5){//horizontal
            titulo+='- height:'+h
        }
    }
    document.title = titulo
    document.body.style.background = (operation==1)?'#0008ff85':(operation==2)?'#ff080085':'white'
    window.requestAnimationFrame(update)
}
update()
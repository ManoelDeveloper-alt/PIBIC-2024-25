canvas.addEventListener("mousedown",(e)=>{
    pos = getScale(e)
    if(operation==0){
        desenhando = true
        if(mapa[pos.y]!=null){
            if(mapa[pos.y][pos.x]!=null){
                mapa[pos.y][pos.x] = ferramenta
            }
        }
    }
    if(operation==1){//satrtSelection
        $M("#iniciox").value = pos.x
        $M("#inicioy").value = pos.y
        operationState(0, $M(".items .ponto"))
    }
    if(operation==2){//satrtSelection
        $M("#fimx").value = pos.x
        $M("#fimy").value = pos.y
        operationState(0, $M(".items .ponto"))
    }
    if(operation==3 || operation==4 || operation==5){//linha
        lembrar = [pos]
    }
})

canvas.addEventListener("mousemove",(e)=>{
    pos = getScale(e)
    if(desenhando){
        if(mapa[pos.y]!=null){
            if(mapa[pos.y][pos.x]!=null){
                mapa[pos.y][pos.x] = ferramenta
            }
        }
    }
    if((operation==3||operation==4 || operation==5) && lembrar.length>0){
        lembrar[1] = pos
    }
    atualMouse = [pos.x,pos.y]
})

canvas.addEventListener("mouseup",(e)=>{
    desenhando = false
    if(lembrar.length>0){
        lembrar[1] = getScale(e)
    }
    if(operation==3 && lembrar.length>1){
        var x = lembrar[0].x
        var ystart = lembrar[0].y
        var deslocamento = lembrar[1].y-ystart
        var dir = 1
        if(deslocamento<0){
            dir = -1
            deslocamento = deslocamento*-1
        }
        for(var i = 0; i<=deslocamento;i++){
            var y_indice = ystart+(i*dir)
            if(mapa[y_indice]!=null){
                if(mapa[y_indice][x] != null){
                    mapa[y_indice][x] = ferramenta
                }
            }
        }
    }
    if(operation==4 && lembrar.length>1){
        var y = lembrar[0].y
        var xstart = lembrar[0].x
        var deslocamento = lembrar[1].x-xstart
        var dir = 1
        if(deslocamento<0){
            dir = -1
            deslocamento = deslocamento*-1
        }
        for(var i = 0; i<=deslocamento;i++){
            var x_indice = xstart+(i*dir)
            if(mapa[y]!=null){
                if(mapa[y][x_indice] != null){
                    mapa[y][x_indice] = ferramenta
                }
            }
        }
    }
    if(operation==5 && lembrar.length>1){
        var x1 = lembrar[0].x
        var y1 = lembrar[0].y
        var x2 = lembrar[1].x
        var y2 = lembrar[1].y
        var w = x2-x1
        var h = y2-y1
        //linha top
        let dirw = 1
        if(w<0){
            dirw=-1
            w=w*-1
        }
        for(let i = 0; i<=w; i++){
            var x_indice = x1+(i*dirw)
            if(mapa[y1]!=null){
                if(mapa[y1][x_indice] != null){
                    mapa[y1][x_indice] = ferramenta
                }
            }
            if(mapa[y2]!=null){
                if(mapa[y2][x_indice] != null){
                    mapa[y2][x_indice] = ferramenta
                }
            }
        }
        let dirh = 1
        if(h<0){
            dirh=-1
            h=h*-1
        }
        for(let i = 0; i<=h; i++){
            var y_indice = y1+(i*dirh)
            if(mapa[y_indice]!=null){
                if(mapa[y_indice][x1] != null){
                    mapa[y_indice][x1] = ferramenta
                }
                if(mapa[y_indice][x2] != null){
                    mapa[y_indice][x2] = ferramenta
                }
            }
        }
    }
    lembrar = []
})
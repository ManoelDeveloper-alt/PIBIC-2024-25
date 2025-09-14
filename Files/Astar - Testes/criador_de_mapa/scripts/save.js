function save(){
    var varname = $M("#varname").value || "mapa"
    var out = varname+' = [\n'
    startX = $M("#iniciox").value
    startY = $M("#inicioy").value
    finishX = $M("#fimx").value
    finishY = $M("#fimy").value
            
    for(var i = 0; i<mapa.length;i++){
        out += '['
        for( var j = 0; j<mapa[i].length;j++){
            if(i==startY && j==startX){
                out+=2
            }else if(i==finishY && j==finishX){
                out+=3
            }else{
                out+=mapa[i][j]
            }
            if(j<mapa[i].length-1){
                out+=','
            }
        }
        out+=']'
        if(i<mapa.length-1){
            out+=','
        }
        out+='\n'
    }
    out+=']'
    const blob = new Blob([out], {type:'text/py'})
    const link = document.createElement("a")
    link.href = URL.createObjectURL(blob)
    var name = $M("#fileName").value || "mapa"
    link.download = name+'.py'
    document.body.appendChild(link)
    link.click()

    document.body.removeChild(link)
}
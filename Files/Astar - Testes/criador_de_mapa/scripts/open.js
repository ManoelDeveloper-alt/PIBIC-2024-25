function openFile(){
    var input = document.createElement('input')
        input.type = 'file'

        input.onchange = function(e){
            var file = e.target.files[0]
            var name = file.name
            if(name.indexOf('.py')>0){
                $M("#fileName").value = name.substring(0,name.length-3)
                var fileread = new FileReader()
                fileread.onload = function(e){
                    var text =fileread.result
                    var varname = ""
                    var content = "{\"valor\":"
                    var ctrl = 0
                    for(var i = 0; i<text.length; i++){
                        var letter = text.charAt(i)
                        if(ctrl == 0){
                            if(letter != "=" && letter != " "){
                                varname+=letter
                            }
                            if(letter == "="){
                                ctrl=1
                            }
                        }else if(ctrl==1){
                            content+=letter
                        }
                    }
                    content+='}'
                    $M("#varname").value = varname
                    var newmap = JSON.parse(content).valor
                    for(var line =0; line<newmap.length;line++){
                        for(var col = 0; col<newmap[line].length;col++){
                            var data = newmap[line][col]
                            //2 start, 3 finish
                            if(data == 2){
                                $M("#iniciox").value = col
                                $M("#inicioy").value = line
                                newmap[line][col] = 0
                            }else if(data == 3){
                                $M("#fimx").value = col
                                $M("#fimy").value = line
                                newmap[line][col] = 0
                            }
                        }
                    }
                    var larg = newmap[0].length
                    var alt = newmap.length
                    $M("#width").value = larg
                    $M("#height").value = alt
                    mapa = newmap
                }
                fileread.readAsText(file)
            }else{
                var dataInfo = "o Arquivo selecionado deve ser um arquivo .py"
                console.error(dataInfo)
                alert(dataInfo)
            }
        }
        input.click()
}
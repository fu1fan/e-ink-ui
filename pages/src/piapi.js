piapi = {}
piapi.msg = "okk"

piapi.updateImage = function(){
    piapi.msg = "updateImage"
}

piapi.log = function(msg){
    piapi.msg = "log"
    piapi.logmsg = msg
}
function piCallback(data){
    piapi.callback(data)
}

piapi.getInfo = function(callback){
    piapi.msg = "getInfo"
    piapi.callback = callback
}
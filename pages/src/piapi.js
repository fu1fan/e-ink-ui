piapi = {}
piapi.msg = "okk"

piapi.updateImage = function(){
    piapi.msg = "updateImage"
}

piapi.log = function(msg){
    piapi.msg = "log"
    piapi.logmsg = msg
}
piapi.piCallback = function(data){
    piapi.callback(data)
}

piapi.getInfo = function(callback){
    piapi.msg = "getInfo"
    piapi.callback = callback
}

piapi.stop = function(){
    piapi.msg = "stop"
}

piapi.poweroff = function(){
    piapi.msg = "poweroff"
}

piapi.reboot = function(){
    piapi.msg = "reboot"
}

piapi = {}
piapi.msg = "okk"

piapi.updateImage = function(){
    piapi.msg = "updateImage"
}

piapi.refreshScreen = function(){
    piapi.msg = "refreshScreen"
}

piapi.log = function(msg){
    piapi.msg = "log"
    piapi.logmsg = msg
}
piapi.piCallback = function(data){
    if (data.msg == "getInfo"){
        piapi.infoCallback(data)
    } else if (data.msg == "runCmd"){
        piapi.cmdCallback(data)
    }
}

piapi.getInfo = function(callback){
    piapi.msg = "getInfo"
    piapi.infoCallback = callback
}

piapi.runCmd = function(cmd, callback){
    piapi.msg = "runCmd"
    piapi.cmd = cmd
    piapi.cmdCallback = callback
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

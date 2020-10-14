const electron =require('electron')
const path=require('path')
const fs=require('fs')
const ipc=electron.ipcRenderer;
const refreshBtn=document.getElementById("refresh");
refreshBtn.addEventListener('click',function(){
    ipc.send('refresh-widget');
})
const fontList = require('font-list');
ipc.send('requestPath');
let configPath;
ipc.on('sendPath',(event,arg)=>{
    configPath=arg;
})

fontList.getFonts()
  .then(fonts => {
      fonts.forEach(element => {
        var temp=document.getElementById("fontsList");
        var option=document.createElement("option");
        option.text=element;
        temp.add(option);
      });
    
  })
  .catch(err => {
    console.log(err)
  })
console.log(document.getElementById(''))
let conf={
    time:{},
    day:{},
    quote:{}
}
conf=JSON.parse(fs.readFileSync(path.join(configPath,"config.json"),'utf-8'));
document.getElementById('settingsForm').addEventListener('submit',function(e){
    e.preventDefault()
    
    let filePath=null;let fontName=null
    const color=document.getElementById('hex_code').value;
    try{
        filePath=document.getElementById('customFont').files[0].path;
    }
    catch(err){
        filePath=null;
    }
    if(filePath==null)
        fontName=document.getElementById('fontsList').value;
    console.log(fontName);
    if(filePath!=null){
        conf.time.fontName="CustomFont";
        conf.time.customFont=true;
        conf.time.fontPath=filePath;
        conf.time.color=color;
        fs.copyFileSync(filePath,path.join(configPath,"CustomPath."+path.parse(filePath).ext),function(err){
            if (err) { 
              console.error(err); 
            } 
        })
    }
    else{
        conf.time.fontName=fontName;
        conf.time.customFont=false;
        conf.time.fontPath=null;
        conf.time.color="#ffff";
    }
    console.log(conf);
    
    fs.writeFileSync(path.join(configPath,"config.json"),JSON.stringify(conf));
})
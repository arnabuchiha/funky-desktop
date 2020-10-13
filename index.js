const electron =require('electron')
const { promisify } = require('util');
const { pipeline } = require('stream');
const {
  createReadStream,
  createWriteStream
} = require('fs');
const pipe = promisify(pipeline);
const { createGzip } = require('zlib');

const ipc=electron.ipcRenderer;
const refreshBtn=document.getElementById("refresh");
refreshBtn.addEventListener('click',function(){
    ipc.send('refresh-widget');
})
const fontList = require('font-list');

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
// const clocksettings=document.getElementById("clock");
// console.log(clocksettings)
// clocksettings.addEventListener('click',function(){
//     clocksettings.className="select";
// })
async function do_gzip(input, output) {
    const gzip = createGzip();
    const source = createReadStream(input);
    const destination = createWriteStream(output);
    await pipe(source, gzip, destination);
  }
document.getElementById('settingsForm').addEventListener('submit',function(e){
    e.preventDefault()
    let conf={
        time:{},
        day:{},
        quote:{}
    }
    let filePath=null;let fontName=null
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
        do_gzip(filePath, 'input.txt.gz')
        .catch((err) => {
            console.error('An error occurred:', err);
        });
        conf.time.fontName=null;
        conf.time.customFont=true;
        conf.time.fontPath=filePath;
        conf.time.color="#ffff";
    }
    else{
        conf.time.fontName=fontName;
        conf.time.customFont=false;
        conf.time.fontPath=null;
        conf.time.color="#ffff";
    }
    console.log(conf);
})
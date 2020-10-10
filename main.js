const {app,BrowserWindow,remote} =require("electron");
const path=require("path");
const url=require("url");
const cp = require('child_process');
try {
  cp.spawnSync('which xprop').toString();
} catch (error){
  console.error(`GlassIt Error: Please install xprop package to use GlassIt.`);
  return;
}
let win;
function createWindow(){
    win=new BrowserWindow({
        width: 800,
        height: 600,
        frame:false,
        transparent:true,
        title:"funkyD",
        // backgroundColor:"rgba(255, 255, 255, 0)",
        webPreferences: {
          nodeIntegration: true
        }
        // type:'desktop'
      });
    win.loadURL(url.format({
        pathname:path.join(__dirname,'index.html'),
        protocol:"file",
        slashes:true
    }))
    // win.setOpacity(0)
    console.log(process.pid);
    // win.webContents.openDevTools({mode:'undocked'})
}

app.commandLine.appendSwitch('enable-transparent-visuals');
// app.commandLine.appendSwitch('disable-gpu');
app.whenReady().then(createWindow)

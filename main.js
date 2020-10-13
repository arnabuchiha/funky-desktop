const {app,BrowserWindow,remote,Tray,Menu,ipcMain} =require("electron");
var path = require('path')
var iconpath = path.join(__dirname, 'user.png')
const url=require("url");
const {spawn} = require('child_process');
const cp=require('child_process')
const { platform } = require("os");
var AutoLaunch = require('auto-launch');
const ipc=ipcMain;
let child;
let win;
let appIcon;
function createWindow(){
    win=new BrowserWindow({
        width: 800,
        height: 600,
        frame:true,
        // transparent:true,
        title:"funkyD",
        // backgroundColor:"rgba(255, 255, 255, 0)",
        webPreferences: {
          nodeIntegration: true
        }
      });
    win.loadURL(url.format({
        pathname:path.join(__dirname,'index.html'),
        protocol:"file",
        slashes:true
    }))
    appIcon = new Tray(iconpath)
    var contextMenu = Menu.buildFromTemplate([
      {
          label: 'Show App', click: function () {
              win.show()
          }
      },
      {
          label: 'Quit', click: function () {
              app.isQuiting = true
              app.quit()
          }
      }
    ])
    win.removeMenu()
    appIcon.setContextMenu(contextMenu);
    appIcon.setToolTip('funkyD-Desktop Customisation')
    // and load the index.html of the app.
    win.loadFile('index.html')
    win.on('close', function (event) {
      win = null
    })

    win.on('minimize', function (event) {
        event.preventDefault()
        win.hide()
    })
    // win.on('show',function (event) {
    //     appIcon.setHighlightMode('always')
    // })
    appIcon.on('click',()=>{
      win.show()
    })
    win.webContents.openDevTools()
}


//Add App to StartUp
var funkyDLauncher=new AutoLaunch({
  name:'funkyD',
  path:app.getPath("exe")
})
funkyDLauncher.isEnabled().then((isEnabled)=>{
  if(!isEnabled)funkyDLauncher.enable();
})


console.log(app.getPath("appData"))
// if(process.platform=='linux'){
//   cp.exec("python widget.py --path="+app.getPath("exe"));
// }


if(process.platform=='linux'){
  // cp.exec(".\\dist\\widget\\widget.exe");
  console.log(app.getPath("userData"))
  app.whenReady().then(createWindow)
  child=spawn('python',['widget.py']);
    child.on('close', (code, signal) => {
      console.log(
        `child process terminated due to receipt of signal ${code}`);
        // child.kill('SIGTERM');
    });
  // Send SIGTERM to process
  
  // cp.exec("python widget.py --path="+app.getPath("userData"));
  process.on('exit',function(){
    console.log('Closed')
    child.kill('SIGTERM');
  })
}


ipc.on('refresh-widget',function(){
  try{
    child.kill('SIGTERM');
  }
  catch{
    console.log('Not open');
  }
  child=spawn('python',['widget.py']);
})
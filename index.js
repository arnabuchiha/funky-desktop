const electron = require("electron");
const path = require("path");
const fs = require("fs");
const ipc = electron.ipcRenderer;
const fontkit = require("fontkit");
const refreshBtn = document.getElementById("refresh");
const settings = require("electron-settings");
const fontList = require("font-list");
const {dialog} =require('electron').remote
const archiver = require('archiver');
const extract = require('extract-zip');

refreshBtn.addEventListener("click", function () {
  ipc.send("refresh-widget");
});
ipc.send("requestPath");

let conf = {
  time: {},
  day: {},
  quote: {},
};
let configPath;
ipc.on("sendPath", (event, arg) => {
  configPath = arg;
  conf = JSON.parse(
    fs.readFileSync(path.join(configPath, "config.json"), "utf-8")
  );
  loadData("time");
});

//Preview Background settings

var x = settings.getSync("preview-bg-path");
if (x == undefined) x = "./assets/icons/change-bg-icon.svg";
document.getElementById(
  "preview"
).style.background = `url(${x})no-repeat center /cover`;


//Get system fonts and append in select

async function getFonts() {
  var temp = document.getElementById("fontsList");
  fontList
    .getFonts()
    .then((fonts) => {
      // fonts=fonts.slice(240)
      fonts.forEach((element) => {
        element = element.replace(/^"(.*)"$/, "$1");
        let option = document.createElement("option");
        // option.style.fontFamily=element
        option.innerHTML = element;

        temp.add(option);
      });
    })
    .catch((err) => {
      console.log(err);
    });
}
getFonts();

// Id of List item currently active
let settingsId = "time";
let previewText = document.getElementById("preview-text");
loadData(settingsId);

$("#list-tab a").on("click", function (e) {
  e.preventDefault();
  settingsId = e.target.innerHTML.toLowerCase();
  loadData(settingsId);
});
var days = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];
var color = null;
var fontSize = null;
var fontName = null;

//Load Data from configuration file to respective fields

function loadData(id) {
  let fontPath = null;
  if (conf[id].customFont) {
    var font = new FontFace(conf[id].fontName, `url(${conf[id].fontPath})`);
    font.load().then((f) => {
      document.fonts.add(f);
      fontPath = fontPath;
    });
  }
  fontName = conf[id].fontName;
  color = conf[id].color;
  fontSize = conf[id].fontSize;
  previewText.style.color = color;
  previewText.style.fontSize = fontSize;
  previewText.style.fontFamily = conf[id].fontName;
  switch (id) {
    case "time":
      previewText.innerHTML = new Date().toLocaleTimeString("en-US");
      break;
    case "day":
      previewText.innerHTML = days[new Date().getDay()];
      break;
    case "greeting":
      previewText.innerHTML = "Good Morning.";
      break;
    default:
      break;
  }
  document.getElementById("hex_code").value = conf[id].color;
  document.getElementById("font_size").value = conf[id].fontSize;
  console.log(conf[id].color);
}

//Change event listeners

document
  .getElementById("change-preview-bg")
  .addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("background-file").click();
  });

document
  .getElementById("background-file")
  .addEventListener("change", function (e) {
    e.preventDefault();
    settings.set("preview-bg-path", e.target.files[0].path);
    document.getElementById(
      "preview"
    ).style.background = `url(${e.target.files[0].path})no-repeat center /cover`;
  });

document.getElementById("hex_code").addEventListener("change", function (e) {
  e.preventDefault();

  color = e.target.value;
  previewText.style.color = color;
});

document.getElementById("font_size").addEventListener("change", function (e) {
  fontSize = e.target.value;
});

document.getElementById("fontsList").addEventListener("change", function (e) {
  fontName = e.target.value;
  previewText.style.fontFamily = fontName;
  fontPath = null;
});

document.getElementById("customFont").addEventListener("change", function (e) {
  fontPath = e.target.files[0].path;
  fontName = fontkit.openSync(fontPath).fullName;
  var font = new FontFace(fontName, `url(${fontPath})`);
  font.load().then((f) => {
    document.fonts.add(f);
    fontPath = fontPath;
  });
  previewText.style.fontFamily = fontName;
});


//Submit data and apply to widget

document
  .getElementById("settingsForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const colorFinal = color;
    const fontSizeFinal = parseInt(fontSize);

    let filePathFinal = null;
    let fontNameFinal = null;
    try {
      // filePath = document.getElementById("customFont").files[0].path;
      filePathFinal = fontPath;
    } catch (err) {
      filePathFinal = null;
    }
    if (filePathFinal == null) {
      // fontName = document.getElementById("fontsList").value;
      fontNameFinal = fontName;
    }
    if (filePathFinal != null) {
      var font = fontkit.openSync(filePathFinal);
      conf[settingsId].fontName = font.fullName;
      conf[settingsId].customFont = true;
      conf[settingsId].fontPath = path.join(
        configPath,
        "CustomPath" + settingsId + path.parse(filePathFinal).ext
      );
      fs.copyFileSync(
        filePathFinal,
        path.join(
          configPath,
          "CustomPath" + settingsId + path.parse(filePathFinal).ext
        ),
        function (err) {
          if (err) {
            console.error(err);
          }
        }
      );
    } else {
      conf[settingsId].fontName = fontNameFinal;
      conf[settingsId].customFont = false;
      conf[settingsId].fontPath = null;
    }
    conf[settingsId].color = colorFinal;
    conf[settingsId].fontSize = fontSizeFinal;
    console.log(conf);

    fs.writeFileSync(
      path.join(configPath, "config.json"),
      JSON.stringify(conf)
    );

    //Restart the widget

    ipc.send("refresh-widget");
  });

//Load theme
document.getElementById('load_theme').addEventListener('click',function loadTheme(e){
  dialog.showOpenDialog({
    properties:['openFile']
  }).then(fpath=>{
    var src=fpath.filePaths[0]
    if(src==undefined)return
    console.log(src)
    // var src=e.target.files[0].path
    if(path.extname(src)=='.fdskin'){
      $('.toast').toast('hide');
      
      try {
        extract(src, { dir: configPath }).then(x=>{
          conf = JSON.parse(
            fs.readFileSync(path.join(configPath, "config.json"), "utf-8")
          );
        })
        document.getElementById('toast-msg').innerHTML="Load success!!"
        $('.toast').toast('show')
        ipc.send('refresh-widget')
        loadData(settingsId);
      } catch (err) {
        document.getElementById('toast-msg').innerHTML="Something went wrong"
        $('.toast').toast('show')
      }
    }
    else{
      document.getElementById('toast-msg').innerHTML="Select a '.fdskin' file'!!"
      $('.toast').toast('show');
      
      console.log('Wrong File')
    }})
})


//Export theme
document.getElementById('export_theme').addEventListener('click',function(e){
  dialog.showSaveDialog({
    properties:['openDirectory']
  }).then(path=>{
    if(path!=undefined){
      const output=fs.createWriteStream(path.filePath+'.fdskin')
      const src=configPath
      output.on('close', function () {
        console.log(archive.pointer() + ' total bytes');
        console.log('archiver has been finalized and the output file descriptor has closed.');
      });
      const archive=archiver('zip',{
        zlib:{level:9}
      })
      archive.pipe(output)
      archive.directory(src,false)
      archive.finalize()
      // asar.createPackage(src,output)
    }
    
    
  })
})
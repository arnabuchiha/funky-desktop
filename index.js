const electron = require('electron')
const path = require('path')
const fs = require('fs')
const ipc = electron.ipcRenderer
const refreshBtn = document.getElementById('refresh')
refreshBtn.addEventListener('click', function () {
  ipc.send('refresh-widget')
})
const fontList = require('font-list')
ipc.send('requestPath')
let conf = {
  time: {},
  day: {},
  quote: {}
}
let configPath
ipc.on('sendPath', (event, arg) => {
  configPath = arg
  conf = JSON.parse(fs.readFileSync(path.join(configPath, 'config.json'), 'utf-8'))
})

fontList.getFonts()
  .then(fonts => {
    fonts.forEach(element => {
      var temp = document.getElementById('fontsList')
      var option = document.createElement('option')
      option.text = element
      temp.add(option)
    })
  })
  .catch(err => {
    console.log(err)
  })

// Id of List item currently active
let settingsId = 'time'
$('#list-tab a').on('click', function (e) {
  e.preventDefault()
  console.log(e.target.innerHTML)
  settingsId = e.target.innerHTML.toLowerCase()
})

function isHexColor (hex) {
  var RegExp = /^#[0-9A-F]{6}$/i
  return RegExp.test(hex)
}
document.getElementById('settingsForm').addEventListener('submit', function (e) {
  e.preventDefault()
  const color = document.getElementById('hex_code').value
  const fontSize = parseInt(document.getElementById('font_size').value)

  // Validations
  if (!isHexColor(color)) {
    const errorDiv = document.getElementById('error')
    errorDiv.style.display = 'block'
    errorDiv.innerHTML = 'Color Code invalid'
    return
  }

  document.getElementById('error').style.display = 'none'
  let filePath = null; let fontName = null
  try {
    filePath = document.getElementById('customFont').files[0].path
  } catch (err) {
    filePath = null
  }
  if (filePath == null) { fontName = document.getElementById('fontsList').value }
  console.log(fontName)
  if (filePath != null) {
    conf[settingsId].fontName = path.parse(filePath).name
    conf[settingsId].customFont = true
    conf[settingsId].fontPath = path.join(configPath, 'CustomPath' + settingsId + path.parse(filePath).ext)
    fs.copyFileSync(filePath, path.join(configPath, 'CustomPath' + settingsId + path.parse(filePath).ext), function (err) {
      if (err) {
        console.error(err)
      }
    })
  } else {
    conf[settingsId].fontName = fontName
    conf[settingsId].customFont = false
    conf[settingsId].fontPath = null
    
  }
  conf[settingsId].color = color
  conf[settingsId].fontSize=fontSize
  console.log(conf)

  fs.writeFileSync(path.join(configPath, 'config.json'), JSON.stringify(conf))
  ipc.send('refresh-widget')
})

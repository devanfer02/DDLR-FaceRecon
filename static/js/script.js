const CONF = {
  cam_is_playing: false,
  recon_cam_is_playing: false,
  cam: 'cam_is_playing',
  video: 'cam_is_playing',
}

function toggle_nav() {
  const navs = document.getElementById('nav-links')

  if (navs.classList.contains('hidden')) {
    navs.classList.remove('hidden')
  } else {
    navs.classList.add('hidden')
  }
}

function hide_loading(id_tag) {
  document.getElementById(id_tag).classList.add('hidden')

  const video = document.getElementById('video')
  if (video) {
    document.getElementById('video').classList.remove('hidden')
    document.getElementById('video').classList.add('flex')
  }
}

function give_loading(title) {
  document.getElementById('load-recon-title').innerHTML = title
  document.getElementById('img-result').src = ''

  document.getElementById('info-recon').classList.remove('flex')
  document.getElementById('info-recon').classList.add('hidden')

  document.getElementById('loading-recon').classList.remove('hidden')
  document.getElementById('loading-recon').classList.add('flex')
}

function upload_image() {
  give_loading('Loading Result')

  const res_img = document.getElementById('img-result')
  const file_input = document.getElementById('img-input')
  const file = file_input.files[0]

  if (!file) {
    // you havent uploaded any file yet
    console.log("lol debug by yourself")
    return 
  } 

  const form_data = new FormData()
  form_data.append('file', file)

  fetch('/recognize', {
    method: 'POST',
    body: form_data
  })
  .then( res => res.blob())
  .then(blob => {
    const img_url = URL.createObjectURL(blob)
    
    res_img.src = img_url
  })
  .catch(err => console.log(err))
}

async function toggle_camera(key, id) {
  try {
    const div = document.getElementById('div-img-result')
    const img = document.getElementById('img-result')
    const btn = document.getElementById(id)
  
    if (CONF[CONF[key]]) {
      await fetch('/stopcam', {method: 'POST'})
      CONF[CONF[key]] = false
      
      img.src = ''
      btn.innerHTML = btn.innerHTML.replace('Off', 'On')
      btn.style.backgroundColor = '#FFF'
      btn.style.color = '#000'
      div.style.display = 'none'
    } else {
      give_loading('Loading Camera')
    
      btn.innerHTML = btn.innerHTML.replace('On', 'Off')
      btn.style.backgroundColor = '#000'
      btn.style.color = '#FFF'
      img.src = `/${key}`
      CONF[CONF[key]] = true
      div.style.display = 'flex'
    }
  
  } catch (e) {
    console.log(e)
  }
}

async function take_image() {
  give_loading('Loading Result')
  const img = document.getElementById('img-result')
  const btn = document.getElementById('toggle-cam')
      
  img.src = ''
  btn.innerHTML = 'Toggle On Camera'
  btn.style.backgroundColor = '#FFF'
  btn.style.color = '#000'

  const res = await fetch('/takeimg', {method:'POST'})
  const blob = await res.blob()
  const img_url = URL.createObjectURL(blob)
  img.src = img_url

  CONF.cam_is_playing = false
}

function prevent_form_refresh() {
  const forms = document.getElementsByClassName('form-user')

  for(let i = 0; i < forms.length; i++) {
    forms[i].addEventListener('submit', function(event) {
      event.preventDefault()
    })
  }
}

prevent_form_refresh()
const CONF = {
  cam_is_playing: false,
  recon_cam_is_playing: false,
  cam: 'cam_is_playing',
  video: 'cam_is_playing',
}

function other_cam_is_playing(btn) {
  return (btn.classList.contains('bg-white') && 
  (CONF.cam_is_playing || CONF.recon_cam_is_playing)) 
}

function enable_btns() {
  const live = document.getElementById('toggle-live')
  const cam = document.getElementById('toggle-cam')

  cam.style.cursor = 'pointer'
  live.style.cursor = 'pointer'
}

function disable_other_btn(btn) {
  const live = document.getElementById('toggle-live')
  const cam = document.getElementById('toggle-cam')

  if (btn !== live) {
    live.style.cursor = 'not-allowed'
  } else {
    cam.style.cursor = 'not-allowed'
  }
}

function toggle_nav() {
  const navs = document.getElementById('nav-links')

  if (navs.classList.contains('hidden')) {
    navs.classList.remove('hidden')
  } else {
    navs.classList.add('hidden')
  }
}

function toggle_btn(btn) {
  if(btn.classList.contains('bg-white')) {
    btn.classList.remove('bg-white')
    btn.classList.remove('text-black')
    btn.classList.add('bg-black')
    btn.classList.add('text-white')
  } else {
    btn.classList.remove('bg-black')
    btn.classList.remove('text-white')
    btn.classList.add('bg-white')
    btn.classList.add('text-black')
  }
}

function hide_loading(id_tag) {
  document.getElementById(id_tag).classList.add('hidden')
}

function give_loading(title) {
  document.getElementById('load-recon-title').innerHTML = title
  document.getElementById('img-result').src = ''

  document.getElementById('info-recon').classList.remove('flex')
  document.getElementById('info-recon').classList.add('hidden')

  document.getElementById('loading-recon').classList.remove('hidden')
  document.getElementById('loading-recon').classList.add('flex')
}

function give_info() {
  document.getElementById('info-recon').classList.remove('hidden')
  document.getElementById('info-recon').classList.add('flex') 
}

function upload_image() {
  give_loading('Loading Result')

  const div = document.getElementById('div-img-result')
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
    
    div.style.display = 'flex'
    res_img.src = img_url
  })
  .catch(err => console.log(err))
}

async function toggle_camera(key, id) {
  try {
    const div = document.getElementById('div-img-result')
    const img = document.getElementById('img-result')
    const btn = document.getElementById(id)

    if (other_cam_is_playing(btn)) {
      return 
    }

    if (CONF[CONF[key]]) {
      await fetch('/stopcam', {method: 'POST'})
      CONF[CONF[key]] = false
      
      img.src = ''
      btn.innerHTML = btn.innerHTML.replace('Off', 'On')
      toggle_btn(btn)
      
      div.style.display = 'none'
      hide_loading('loading-recon')
      give_info()
      enable_btns()
    } else {
      
      give_loading('Loading Camera')
      disable_other_btn(btn)
      
      btn.innerHTML = btn.innerHTML.replace('On', 'Off')
      toggle_btn(btn)
      
      img.src = `/${key}?t=${new Date().getTime()}`
      CONF[CONF[key]] = true
      div.style.display = 'flex'
    }
    console.log(img.src)
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
  toggle_btn(btn)

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

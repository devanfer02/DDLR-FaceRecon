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
  document.getElementById('video').classList.remove('hidden')
  document.getElementById('video').classList.add('flex')
}

function give_loading() {
  document.getElementById('img-result').src = ''

  document.getElementById('info-recon').classList.remove('flex')
  document.getElementById('info-recon').classList.add('hidden')

  document.getElementById('loading-recon').classList.remove('hidden')
  document.getElementById('loading-recon').classList.add('flex')
}

function upload_image() {
  give_loading()

  const res_img = document.getElementById('img-result')
  const file_input = document.getElementById('img-input')
  const file = file_input.files[0]

  if (!file) {
    // you havent uploaded any file yet
    console.log("NOT OK")
    return 
  } 

  console.log("OK")
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

function prevent_form_refresh() {
  const form1 = document.getElementById('form-user')
  form1.addEventListener('submit', function(event) {
    event.preventDefault()
  })
}

prevent_form_refresh()
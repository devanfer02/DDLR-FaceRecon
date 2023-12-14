function toggle_nav() {
  const navs = document.getElementById('nav-links')

  if (navs.classList.contains('hidden')) {
    navs.classList.remove('hidden')
  } else {
    navs.classList.add('hidden')
  }
}

function hide_loading() {
  document.getElementById('loading').classList.add('hidden')
  document.getElementById('video').classList.remove('hidden')
  document.getElementById('video').classList.add('flex')
}
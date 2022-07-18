window.addEventListener('load', (event) => {
  let form = document.getElementById('previous-date')
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault()
      let dateStr = e.target[0].value
      const dateObj = new Date(dateStr)
      console.log('supp', dateObj.getFullYear())
    })
  }
})

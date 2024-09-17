window.sendLuminance = function () {
  var slider = document.getElementById("myRange");
  var lumins = slider.value
  fetch('/', {
    method: 'POST',
    headers: {
                'Content-Type': 'application/json',
              },
    body: JSON.stringify({ luminance: lumins })
  }) 
  .then(response => response.json())
  .then(body => {

  })
}

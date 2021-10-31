//event handlers trigger functions after listening to particular events on an HTML page
//DOMContentLoaded gets trigger when the webpage content loads up

// () => is an arrow function (will trigger function)
document.addEventListener('DOMContentLoaded', () => {

  document.querySelectorAll('audio').forEach(aud => {
    
          if ("{{media_playback['position']}}" != "None") {  
              aud.currentTime = "{{media_playback['position'].progress}}";
          }

      aud.onpause = () => {
          const request = new XMLHttpRequest();
          const id = "{{media_playback['media_id']}}"
          request.open('POST', "/update_progress/" + id);
          //define what happens with response data
          request.onload = () => {
              console.log("done")
          };
          var data = new FormData();
          data.append('progress', aud.currentTime)
          request.send(aud.currentTime);
      };
  });
});


// get audio player
audio = document.getElementsByClassName('audio');
console.log(document.getElementsByTagName('audio'))

$(audio).on('pause','.audio',function(e)
        { 
            console.log("hello")
            song_id = e.target.id;
            save_progress(e, song_id);
        });

function save_progress(e, song_id) {
        console.log('event recieved');
        e.preventDefault();
        $.ajax({
          type:'POST',
          url:'/update_progress/${song_id}',
          data:{
            progress: audio.currentTime
          },
          success: console.log('plz')
        })
}
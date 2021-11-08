"""
Route management.

This provides all of the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML templates
to be displayed.

You will have to make 
"""

# Importing the required packages
from modules import *
from flask import *
import database
import datetime


user_details = {}                   # User details kept for us
session = {}                        # Session information (logged in state)
page = {}                           # Determines the page information

# Initialise the application
app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""


#####################################################
#   INDEX
#####################################################

@app.route('/')
def index():
    """
    Provides the main home screen if logged in.
        - Shows user playlists
        - Shows user Podcast subscriptions
        - Shows superUser status
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'User Management'

    # Get a list of user playlists
    user_playlists = None
    user_playlists = database.user_playlists(user_details['username'])
    # Get a list of subscribed podcasts
    user_subscribed_podcasts = None
    user_subscribed_podcasts = database.user_podcast_subscriptions(user_details['username'])
    # Get a list of in-progress items
    user_in_progress_items = None
    user_in_progress_items = database.user_in_progress_items(user_details['username'])
    # Data integrity checks
    if user_playlists == None:
        user_playlists = []
    
    if user_subscribed_podcasts == None:
        user_subscribed_podcasts = []

    if user_in_progress_items == None:
        user_in_progress_items = []
    print(user_subscribed_podcasts)
    return render_template('index.html',
                           session=session,
                           page=page,
                           user=user_details,
                           playlists=user_playlists,
                           subpodcasts=user_subscribed_podcasts,
                           usercurrent=user_in_progress_items)

#####################################################
#####################################################
####    User Management
#####################################################
#####################################################

#####################################################
#   LOGIN
#####################################################

@app.route('/update_progress/<media_id>', methods = ['POST'])
def update_progress(media_id):

    current_playback_time = float(request.get_data())
    
    #we need media id and current time from the html page
   # print(request.get_json())
    #stuff = request.get_json()
    #print(stuff['progress'])
    username = None
    if 'username' in user_details and session['logged_in'] == True:
        username = user_details['username']
    else:
        return
    #media_id = None 

    #we need to extract song duraction from here to calc progress
    #meta = database.get_song_metadata(media_id)
    now = datetime.date.today()
    playcount = database.get_media_playback_playcount(username,media_id)
    if playcount != None:
        playcount = playcount[0]
    else:
        playcount = 1

    print("PLAYCOUNT", playcount)
    check = database.update_progress(username, media_id, current_playback_time, now,playcount)
    print("setting progress to {} on {}".format(current_playback_time, media_id))
    return ""
    #call  update progress database method
    



@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Provides /login
        - [GET] If they are just viewing the page then render login page.
        - [POST] If submitting login details, check login.
    """
    # Check if they are submitting details, or they are just logging in
    if(request.method == 'POST'):
        # submitting details
        # The form gives back EmployeeID and Password
        login_return_data = database.check_login(
            request.form['username'],
            request.form['password']
        )

        # If it's null, saying they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect username/password, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        # Store the user details for us to use throughout
        global user_details
        user_details = login_return_data[0]

        return redirect(url_for('index'))

    elif(request.method == 'GET'):
        return(render_template('login.html', session=session, page=page))


#####################################################
#   LOGOUT
#####################################################

@app.route('/logout')
def logout():
    """
    Logs out of the current session
        - Removes any stored user data.
    """
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out')
    return redirect(url_for('index'))

#####################################################
#####################################################
####    List All items
#####################################################
#####################################################


#####################################################
#   List Artists
#####################################################
@app.route('/list/artists')
def list_artists():
    """
    Lists all the artists in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Artists'

    # Get a list of all artists from the database
    allartists = None
    allartists = database.get_allartists()

    # Data integrity checks
    if allartists == None:
        allartists = []


    return render_template('listitems/listartists.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allartists=allartists)


#####################################################
#   List Songs
#####################################################
@app.route('/list/songs')
def list_songs():
    """
    Lists all the songs in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Songs'

    # Get a list of all songs from the database
    allsongs = None
    allsongs = database.get_allsongs()


    # Data integrity checks
    if allsongs == None:
        allsongs = []


    return render_template('listitems/listsongs.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allsongs=allsongs)

#####################################################
#   List Podcasts
#####################################################
@app.route('/list/podcasts')
def list_podcasts():
    """
    Lists all the podcasts in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List podcasts'

    # Get a list of all podcasts from the database
    allpodcasts = None
    allpodcasts = database.get_allpodcasts()

    # Data integrity checks
    if allpodcasts == None:
        allpodcasts = []


    return render_template('listitems/listpodcasts.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allpodcasts=allpodcasts)


#####################################################
#   List Movies
#####################################################
@app.route('/list/movies')
def list_movies():
    """
    Lists all the movies in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'List Movies'



    # Get a list of all movies from the database
    allmovies = None
    allmovies = database.get_allmovies()


    # Data integrity checks
    if allmovies == None:
        allmovies = []


    return render_template('listitems/listmovies.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allmovies=allmovies)


#####################################################
#   List Albums
#####################################################
@app.route('/list/albums')
def list_albums():
    """
    Lists all the albums in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get a list of all Albums from the database
    allalbums = None
    allalbums = database.get_allalbums()


    # Data integrity checks
    if allalbums == None:
        allalbums = []


    return render_template('listitems/listalbums.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allalbums=allalbums)


#####################################################
#   List TVShows
#####################################################
@app.route('/list/tvshows')
def list_tvshows():
    """
    Lists all the tvshows in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshows from the database
    alltvshows = None
    alltvshows = database.get_alltvshows()


    # Data integrity checks
    if alltvshows == None:
        alltvshows = []


    return render_template('listitems/listtvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           alltvshows=alltvshows)




#####################################################
#####################################################
####    List Individual items
#####################################################
#####################################################

#####################################################
#   Individual Artist
#####################################################
@app.route('/artist/<artist_id>')
def single_artist(artist_id):
    """
    Show a single artist by artist_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Artist ID: '+artist_id

    # Get a list of all artist by artist_id from the database
    artist = None
    artist = database.get_artist(artist_id)

    # Data integrity checks
    if artist == None:
        artist = []

    return render_template('singleitems/artist.html',
                           session=session,
                           page=page,
                           user=user_details,
                           artist=artist)


def get_playback_dict(media_id):
    media_playback = {}
    media_position = []
    storage_location = database.get_mediaLink(media_id)
    
    if 'username' in user_details and session['logged_in'] == True:
        media_position = database.get_media_playback_position(user_details['username'],media_id)
    
    if len(storage_location) > 0:
        media_playback['storage_location'] = storage_location[0]
    if len(media_position) > 0:
         media_playback['position'] = media_position[0]
    else:
        media_playback['position'] = "None"

    media_playback['media_id'] = media_id
    return media_playback

#####################################################
#   Individual Song
#####################################################
@app.route('/song/<song_id>')
def single_song(song_id):
    """
    Show a single song by song_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Song'
    if(database.songExists(song_id) == False):
        return render_template('invalid.html')
    # Get a list of all song by song_id from the database
    song = None
    song = database.get_song(song_id)

    songmetadata = None
    songmetadata = database.get_song_metadata(song_id)

    media_playback = get_playback_dict(song_id)

    # Data integrity checks
    if song == None:
        song = []
    
    if songmetadata == None:
        songmetadata = []

    album_artwork = None
    album_artwork = database.get_songs_album_artwork(song_id)
    album_description = None 
    album_description = database.get_songs_album_description(song_id)
    print(album_description)
    if len(album_description) == 0:
        newdict = {'md_id': 0, 'md_type_name': 'description', 'md_value': 'No Description Available!'}
        album_description.append(newdict)
    print(album_description)
    
    i = 0
    j = 0
    for item in songmetadata:
        if item['md_type_name'] != 'artwork':
            i+=1
            #print(i)
        if item['md_type_name'] != 'description':
            j+=1
            print(j)
    #if songmetadata['description'] == None:
    if i == len(songmetadata):
        print("yes")
        if (len(album_artwork) > 0):
            songmetadata.append(album_artwork[0])
        else:
            songmetadata.append(None)
    
    if j+1 == len(songmetadata):
        print("yes")
        songmetadata.append(album_description[0])
    print(songmetadata)
    #if j == len(songmetadata):


    return render_template('singleitems/song.html',
                           session=session,
                           page=page,
                           user=user_details,
                           song=song,
                           songmetadata=songmetadata,
                           media_playback=media_playback)

#####################################################
#   Query (6)
#   Individual Podcast
#####################################################
@app.route('/podcast/<podcast_id>')
def single_podcast(podcast_id):
    """
    Show a single podcast by podcast_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast     #
    #############################################################################

    page['title'] = 'Podcast' # Add the title

        # Get a list of all song by song_id from the database
    podcast = None
    podcast = database.get_podcast(podcast_id)

    podcast_episodes = None
    podcast_episodes = database.get_all_podcasteps_for_podcast(podcast_id)

    # Data integrity checks
    if podcast == None:
        podcast = []

    if podcast_episodes == None:
        podcast_episodes = []
    # Set up some variables to manage the returns from the database fucntions
        
    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/podcast.html',
                           session=session,
                           page=page,
                           podcast=podcast,
                           podcast_episodes=podcast_episodes,
                           user=user_details)

@app.route('/playlist/<collection_id>')
def single_playlist(collection_id):

    name = database.get_playlist_name(collection_id)[0]
    media = database.get_playlist_media(collection_id)

    return render_template('singleitems/playlist.html',name=name,media=media)



#####################################################
#   Query (7)
#   Individual Podcast Episode
#####################################################
@app.route('/podcastep/<media_id>')
def single_podcastep(media_id):
    print("asdasdasdasssssssssssssssssss\n\n\n\n")
    """
    Show a single podcast epsiode by media_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast ep  #
    #############################################################################

    page['title'] = 'Podcast Episode' # Add the title

    # Set up some variables to manage the returns from the database fucntions
    podcastep = None
    podcastep = database.get_podcastep(media_id)
    # Once retrieved, do some data integrity checks on the data
    if podcastep == None:
        podcastep = []

    media_playback = get_playback_dict(media_id)    
    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/podcastep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcastep=podcastep,
                           media_playback=media_playback)


#####################################################
#   Individual Movie
#####################################################
@app.route('/movie/<movie_id>')
def single_movie(movie_id):
    """
    Show a single movie by movie_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies by movie_id from the database
    movie = None
    movie = database.get_movie(movie_id)
    
    media_playback = get_playback_dict(movie_id)

    # Data integrity checks
    if movie == None:
        movie = []


    return render_template('singleitems/movie.html',
                           session=session,
                           page=page,
                           user=user_details,
                           movie=movie,
                           media_playback=media_playback)


#####################################################
#   Individual Album
#####################################################
@app.route('/album/<album_id>')
def single_album(album_id):
    """
    Show a single album by album_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get the album plus associated metadata from the database
    album = None
    album = database.get_album(album_id)

    album_songs = None
    album_songs = database.get_album_songs(album_id)

    album_genres = None
    album_genres = database.get_album_genres(album_id)

    # Data integrity checks
    if album_songs == None:
        album_songs = []

    if album == None:
        album = []

    if album_genres == None:
        album_genres = []

    return render_template('singleitems/album.html',
                           session=session,
                           page=page,
                           user=user_details,
                           album=album,
                           album_songs=album_songs,
                           album_genres=album_genres)


#####################################################
#   Individual TVShow
#####################################################
@app.route('/tvshow/<tvshow_id>')
def single_tvshow(tvshow_id):
    """
    Show a single tvshows and its eps in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'TV Show'

    # Get a list of all tvshows by tvshow_id from the database
    tvshow = None
    tvshow = database.get_tvshow(tvshow_id)

    tvshoweps = None
    tvshoweps = database.get_all_tvshoweps_for_tvshow(tvshow_id)
    # Data integrity checks
    if tvshow == None:
        tvshow = []

    if tvshoweps == None:
        tvshoweps = []

    return render_template('singleitems/tvshow.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshow=tvshow,
                           tvshoweps=tvshoweps)

#####################################################
#   Individual TVShow Episode
#####################################################
@app.route('/tvshowep/<tvshowep_id>')
def single_tvshowep(tvshowep_id):
    """
    Show a single tvshow episode in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshow eps by media_id from the database
    tvshowep = None
    tvshowep = database.get_tvshowep(tvshowep_id)
    media_playback = get_playback_dict(tvshowep_id)

    # Data integrity checks
    if tvshowep == None:
        tvshowep = []


    return render_template('singleitems/tvshowep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshowep=tvshowep,
                           media_playback=media_playback)

#####################################################
#   Query (10)
#   Individual Genre
#####################################################
@app.route('/genre/<genre_type>/<genre_id>')
def single_genre(genre_id, genre_type):
    """
    Show a single genre in your media server
    First, figure out what type of genre this is
    Then list all items that have that genre:
    1. Song Genre
        a. list all songs
    2. Film Genre
        a. list all tv shows and films
    3. Postcast Genre
        a. list all podcasts
    Can do this without a login
    """
  

    genre_name = database.get_genre_name(genre_id)
    media = None
    if genre_type == "film genre":
        media = database.get_genre_movies_and_shows(genre_id)

    
    if genre_type == "song genre":
        media = database.get_genre_songs(genre_id)
    
    if genre_type == "podcast genre":
        media = database.get_genre_podcasts(genre_id)


    #############################################################################
    # Fill in the Function below with to do all data handling for a genre       #
    #############################################################################

    

    # Identify the type of genre - you may need to add a new function to database.py to do this

    # Set up some variables to manage the returns from the database functions
    #   There are some function frameworks provided for you to do this.
    
    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/genre.html',
                           session=session,
                           genre_name=genre_name,
                           genre_type=genre_type,
                           media=media,
                           user=user_details)


#####################################################
#####################################################
####    Search Items
#####################################################
#####################################################

#####################################################
#   Search TVShow
#####################################################
@app.route('/search/tvshow', methods=['POST','GET'])
def search_tvshows():
    """
    Search all the tvshows in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'TV Show Search'

    # Get a list of matching tv shows from the database
    tvshows = None
    if(request.method == 'POST'):

        tvshows = database.find_matchingtvshows(request.form['searchterm'])

    # Data integrity checks
    if tvshows == None or tvshows == []:
        tvshows = []
        page['bar'] = False
        flash("No matching tv shows found, please try again")
    else:
        page['bar'] = True
        flash('Found '+str(len(tvshows))+' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_tvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshows=tvshows)

#####################################################
#   Query (9)
#   Search Movie
#####################################################
@app.route('/search/movie', methods=['POST','GET'])
def search_movies():
    """
    Search all the movies in your media server
    """
    # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for searching for #
    # a movie                                                                   #
    #############################################################################

    page['title'] = '' # Add the title

    if request.method == 'POST':
        # Set up some variables to manage the post returns
        movies = None
        movies = database.find_matchingmovies(request.form['searchterm'])
        
        # Once retrieved, do some data integrity checks on the data
        if movies == None or movies == []:
            movies = []
            page['bar'] = False
            flash("No matching movies found, please try again")
        else:
            page['bar'] = True
            flash('Found '+ str(len(movies))+' results!')
            session['logged_in'] = True
        # Once verified, send the appropriate data to 

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/search_movies.html',
                    session=session,
                    page=page,
                    user=user_details,
                    movies=movies)
    else:
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_movies.html',
                           session=session,
                           page=page,
                           user=user_details)


#####################################################
#   Add Movie
#####################################################
@app.route('/add/movie', methods=['POST','GET'])
def add_movie():
    """
    Add a new movie
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Movie Creation'

    movies = None
    print("request form is:")
    newdict = {}
    print(request.form)

    # Check your incoming parameters
    if(request.method == 'POST'):

        # verify that the values are available:
        if ('movie_title' not in request.form):
            newdict['movie_title'] = 'Empty Film Value'
        else:
            newdict['movie_title'] = request.form['movie_title']
            print("We have a value: ",newdict['movie_title'])

        if ('release_year' not in request.form):
            newdict['release_year'] = '0'
        else:
            newdict['release_year'] = request.form['release_year']
            print("We have a value: ",newdict['release_year'])

        if ('description' not in request.form):
            newdict['description'] = 'Empty description field'
        else:
            newdict['description'] = request.form['description']
            print("We have a value: ",newdict['description'])

        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ",newdict['storage_location'])

        if ('film_genre' not in request.form):
            newdict['film_genre'] = 'drama'
        else:
            newdict['film_genre'] = request.form['film_genre']
            print("We have a value: ",newdict['film_genre'])

        if ('artwork' not in request.form):
            newdict['artwork'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
        else:
            newdict['artwork'] = request.form['artwork']
            print("We have a value: ",newdict['artwork'])
        
        print('newdict is:')
        print(newdict)

        #forward to the database to manage insert
        movies = database.add_movie_to_db(newdict['movie_title'],newdict['release_year'],newdict['description'],newdict['storage_location'],newdict['film_genre'],newdict['artwork'])


        max_movie_id = database.get_last_movie()[0]['movie_id']
        print(movies)
        if movies is not None:
            max_movie_id = movies[0]

        # ideally this would redirect to your newly added movie
        return single_movie(max_movie_id)
    else:
        return render_template('createitems/createmovie.html',
                           session=session,
                           page=page,
                           user=user_details)


#####################################################
#   Query (8)
#   Add song
#####################################################
@app.route('/add/song', methods=['POST','GET'])
def add_song():
    """
    Add a new Song
    """
    # # Check if the user is logged in, if not: back to login.
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    #########
    # TODO  #  
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for adding a song #
    #############################################################################

    page['title'] = 'Adding Song' # Add the title
    newdict = {}

    if request.method == 'POST':
        
        if ('song_title' not in request.form):
            newdict['song_title'] = 'Empty Song Value'
        else:
            newdict['song_title'] = request.form['song_title']
        
        if ('description' not in request.form):
            newdict['description'] = 'Empty Song Description'
        else:
            newdict['description'] = request.form['description']
            print("We have a description value: ",newdict['description'])
        
        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a storage value: ",newdict['storage_location'])
        
        if ('songlength' not in request.form):
            newdict['songlength'] = 'Empty storage location'
        else:
            newdict['songlength'] = request.form['songlength']
            print("We have a songlength value: ",newdict['songlength'])
        
        if ('genre' not in request.form):
            newdict['genre'] = 'No genre'
        else:
            newdict['genre'] = request.form['genre']
            print("We have a genre value: ",newdict['genre'])
        
        if ('artistid' not in request.form):
            newdict['artistid'] = '0'
        else:
            newdict['artistid'] = request.form['artistid']
            print("We have a artist value: ",newdict['artistid'])
        
        print('newdict is:')
        print(newdict)
        if (database.artistExists(newdict['artistid']) == False ):
            return render_template('invalid.html')
        
        song_id = database.add_song_to_db(newdict['storage_location'],newdict['description'],newdict['song_title'],newdict['songlength'],newdict['genre'], newdict['artistid'])

        print("We have a value: ",newdict['song_title'])
        
        

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        # return render_template('singleitems/song.html',
        #                    session=session,
        #                    page=page,
        #                    user=user_details)
        max_song_id = database.get_last_song()[0]['song_id']
        print(max_song_id)
        # if song_id is not None:
        #     max_song_id = song_id[0]
        
        return single_song(max_song_id)
    else:
        return render_template('createitems/createsong.html',
                           session=session,
                           page=page,
                           user=user_details)

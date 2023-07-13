### English | [简体中文]

# Just a music player

For someone who simply wants to listen to music, a music player should have a pure and straightforward functionality - playing songs. It should not include features such as live streaming, social interactions, or DJ capabilities. The user interface should have a single interaction, which is to start playing music by adding music files. Subsequently, the user should only see lyrics, album cover, progress bar, and playback controls, without distractions such as comments, karaoke, or playlists.

The lyrics should be displayed similar to Apple Music, where they are initially blurred and become visible when the mouse is hovered over them. The scrolling of the lyrics should be smooth, with each line seamlessly transitioning to the next, creating a fluid and unobtrusive visual experience.

The album cover should be a simple image or a circular disc-like design. If it is a circular disc, it could have the ability to rotate, adding a visually engaging element to the music player interface.

The progress bar could be incorporated within the disc itself or exist as a separate element. It could be designed in a way that seamlessly integrates with the overall aesthetic of the music player, providing a clear and intuitive representation of the playback progress.

......

Although I have wild ideas in my mind, I can't seem to execute them...

On July 11th, I tinkered with the PyQT Designer, but I couldn't figure it out. Indeed! I couldn't even implement the functionality to load lyrics, let alone UI design. Moreover, at this moment, I'm frustrated because I can't play songs in the background.

On July 12th, I deleted the previously designed UI and decided to start with something simple. "A journey of a thousand miles begins with a single step." I should first focus on implementing background music playback and lyrics extraction/display features. After an hour of debugging, I managed to accomplish the display of lyrics and background music playback. In that fleeting moment of its smooth operation, I felt satisfied, yet it didn't fully meet my desired outcome. However, I'm still puzzled about the next steps... What should I use to achieve it? Tkinter, PyQT, Pygame, or HTML+CSS? Regardless of which path I choose, I have to pay the price for my initial imaginative ideas. To fulfill those aspirations, I might have to implement AAML lyric parsing, Gaussian blur effects, audio background playback, support for various formats like MP3/WAV/OGG, automatic search for artist lyrics information... As for Gaussian blur effects, I believe it would be difficult or even impossible to achieve using Tkinter or PyQT. In terms of difficulty, I am more inclined to choose Pygame, which I have a certain foundation in. Additionally, based on my knowledge, Pygame can fulfill some of the rendering requirements.

On July 13th, the basic roadmap using Pygame for development has been finalized. MusicPlayer v2 is complete, or at least it has a GUI interface.

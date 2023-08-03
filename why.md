# Why make this?

For someone who simply wants to listen to music, a music player should have a pure and straightforward functionality - playing songs. It should not include features such as live streaming, social interactions, or DJ capabilities. The user interface should have a single interaction, which is to start playing music by adding music files. Subsequently, the user should only see lyrics, album cover, progress bar, and playback controls, without distractions such as comments, karaoke, or playlists.

The lyrics should be displayed similar to Apple Music, where they are initially blurred and become visible when the mouse is hovered over them. The scrolling of the lyrics should be smooth, with each line seamlessly transitioning to the next, creating a fluid and unobtrusive visual experience.

The album cover should be a simple image or a circular disc-like design. If it is a circular disc, it could have the ability to rotate, adding a visually engaging element to the music player interface.

The progress bar could be incorporated within the disc itself or exist as a separate element. It could be designed in a way that seamlessly integrates with the overall aesthetic of the music player, providing a clear and intuitive representation of the playback progress.

......

Although I have wild ideas in my mind, I can't seem to execute them...

On July 11th, I tinkered with the PyQT Designer, but I couldn't figure it out. Indeed! I couldn't even implement the functionality to load lyrics, let alone UI design. Moreover, at this moment, I'm frustrated because I can't play songs in the background.

On July 12th, I deleted the previously designed UI and decided to start with something simple. "A journey of a thousand miles begins with a single step." I should first focus on implementing background music playback and lyrics extraction/display features. After an hour of debugging, I managed to accomplish the display of lyrics and background music playback. In that fleeting moment of its smooth operation, I felt satisfied, yet it didn't fully meet my desired outcome. However, I'm still puzzled about the next steps... What should I use to achieve it? Tkinter, PyQT, Pygame, or HTML+CSS? Regardless of which path I choose, I have to pay the price for my initial imaginative ideas. To fulfill those aspirations, I might have to implement AAML lyric parsing, Gaussian blur effects, audio background playback, support for various formats like MP3/WAV/OGG, automatic search for artist lyrics information... As for Gaussian blur effects, I believe it would be difficult or even impossible to achieve using Tkinter or PyQT. In terms of difficulty, I am more inclined to choose Pygame, which I have a certain foundation in. Additionally, based on my knowledge, Pygame can fulfill some of the rendering requirements.

On July 13th, the basic roadmap using Pygame for development has been finalized. MusicPlayer v2 development begins, at least with a GUI interface. Particle effects have been added during music playback.

For more updates, please refer to the commit history.

# 为什么做这个？

对于一个只想听音乐的人来说，一个音乐播放器应该只有纯粹的功能——听歌。而不是直播、社交甚至打碟。它的开屏界面应该只有一个交互，那就是放入音乐文件开始。紧接着，我只应该看到歌词、封面、进度条和播放控制，而不是评论、K歌或歌单。

歌词应该是像Apple Music一样的，你看到下面的歌词是模糊的，将鼠标放上去会显现出来，歌词的移动是平滑的，下面的歌词紧跟其后，灵动而不花哨。

封面应该只是一张图片或者可以是一个圆形唱片。如果是圆形唱片，那它应该可以旋转。

进度条也许会包含在唱片中，也许可以单独作为一个条存在。

……

虽然我脑子里有天马行空的想法，但是我做不到……

7月11日，我折腾了PyQT设计器，可我弄不明白。是啊！我甚至连歌词加载的功能都没有实现，何谈UI设计呢？而且，此时的我正因歌曲无法后台播放而抓耳挠腮。

7月12日，我删除了之前设计的UI，决定从简单的做起。不积跬步，无以至千里，我应该先实现歌曲的后台播放以及歌词提取、展示功能。最后，经过一个小时的Debug调试，我完成了歌词展示和歌曲后台播放。在它正常运行的一刹那，我很满足，但并不对我想要的结果满足。可是，我仍然为下一步感到迷茫……我应该用什么来实现它呢？是Tkinter、PyQT、Pygame或者HTML+CSS？无论我选择哪一条，都要为我最初天马行空的想象买单，如果想实现那种愿望，我可能得做出AAML歌词读取、高斯模糊特效、音频后台播放、MP3/WAV/OGG等格式全支持、自动搜索歌手歌词信息……对于高斯模糊特效，我认为使用Tkinter和PyQT无法/很难做到高斯模糊；对于难度而言，我更愿意选择有一定基础的Pygame。而且，据我所知，在渲染方面的一些需求完全可以由Pygame实现。

7月13日，使用Pygame开发的基本路线已经敲定，MusicPlayer v2开始开发，至少有了GUI界面；加入了播放音乐时的效果

更多更新日志，请看commit
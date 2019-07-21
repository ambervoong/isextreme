# isextreme

<p align="center"> 
  <b> Team Nyarlathotep - Orbital Project </b>
</p> 

<p align="center"> 
Aim
</p> 

<p align="center">
An application that allows users to crawl Twitter for tweets containing any desired search term and detect the presence of pro-ISIS tweets using machine learning.
</p>

How to use (for *nix systems):

Run frontend.py in Code. Open up a terminal and navigate to where you downloaded the files.

For example,
```
cd your_file_path/isextreme_master/Code
```
Then run the GUI.
```
python3 frontend.py
```

Troubleshooting
- You might have to download some libraries for the program to work.
- The progress bar is known to not work on MacOS, but the rest of the program works fine.

```
pip install twint
```
```
pip install aiohttp_socks
```
Depending on your system and what you're using, you might have to use pip3 instead.

Other things you may need: Python3, PyQT, numpy, pandas, matplotlib, wordcloud etc. The errors will tell you if you have any missing dependencies.

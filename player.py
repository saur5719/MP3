from tkinter import *
from tkinter import filedialog
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()

root.title("MP3 Player")
root.geometry("600x400")

pygame.mixer.init()

def  play_time():
	if stopped:
		return

	#Grab Current song time
	current_time=pygame.mixer.music.get_pos()/1000
	converted_current_time=time.strftime('%M:%S',time.gmtime(current_time))
	#find current song length
	song=playlist_box.get(ACTIVE)
	song=f'E:/Projects/mp3/audio/{song}mp3'
	song_mut=MP3(song)
	global song_length
	song_length=song_mut.info.length
	converted_song_length=time.strftime('%M:%S',time.gmtime(song_length))
	
	#check to see if song is over
	if int(song_slider.get())==int(song_length):
		stop()

	elif paused:
		pass
	else:
		next_time=int(song_slider.get())+1
		song_slider.config(to=song_length,value=next_time)

		converted_current_time=time.strftime('%M:%S',time.gmtime(int(song_slider.get())))
		status_bar.config(text=f'Time Elapsed : {converted_current_time} / {converted_song_length}')


	#add current time to status bar
	if current_time>=1:
		status_bar.config(text=f'Time Elapsed : {converted_current_time} / {converted_song_length}')
	status_bar.after(1000,play_time)

def add_song():
	song=filedialog.askopenfilename(initialdir='audio/',title="choose A Song",filetypes=(("mp3 Files","*.mp3"),))
	#Strip out directory structure and .mp3 from 
	song=song.replace("E:/Projects/mp3/audio/","")
	song=song.replace("mp3","")
	playlist_box.insert(END,song)

def add_many_song():
	songs=filedialog.askopenfilenames(initialdir='audio/',title="choose Many Song",filetypes=(("mp3 Files","*.mp3"),))
	for song in songs:
		#Strip out directory structure and .mp3 from 
		song=song.replace("E:/Projects/mp3/audio/","")
		song=song.replace("mp3","")
		playlist_box.insert(END,song)

def delete_song():
	playlist_box.delete(ANCHOR)

def delete_all_songs():
	playlist_box.delete(0,END)

def play():
	global stopped
	stopped=False
	song=playlist_box.get(ACTIVE)
	song=f'E:/Projects/mp3/audio/{song}mp3'
	#Load play song with pygame
	pygame.mixer.music.load(song)
	#play song with pygame
	pygame.mixer.music.play(0)

	#Get Song Time
	play_time()

#stop function global variable
global stopped
stopped=False
def stop():
	pygame.mixer.music.stop()
	playlist_box.selection_clear(ACTIVE)
	status_bar.config(text='')
	song_slider.config(value=0)
	global stopped
	stopped=True

#pause function global variable
global paused
paused=False
def pause(is_paused):
	global paused
	paused=is_paused

	if paused:
		pygame.mixer.music.unpause()
		paused=False
	else:
		pygame.mixer.music.pause()
		paused=True

def next_song():
	#Reset Slider and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	next_one=playlist_box.curselection()
	next_one=next_one[0]+1

	song=playlist_box.get(next_one)
	song=f'E:/Projects/mp3/audio/{song}mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(0)

	playlist_box.selection_clear(0,END)
	playlist_box.activate(next_one)

	playlist_box.selection_set(next_one,last=None)

def previous_song():
	#Reset Slider and status bar
	status_bar.config(text='')
	song_slider.config(value=0)
	next_one=playlist_box.curselection()
	next_one=next_one[0]-1

	song=playlist_box.get(next_one)
	song=f'E:/Projects/mp3/audio/{song}mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(0)

	playlist_box.selection_clear(0,END)
	playlist_box.activate(next_one)

	playlist_box.selection_set(next_one,last=None)

def volume(x):
	pygame.mixer.music.set_volume(volumn_slider.get())

def slide(x):
	song=playlist_box.get(ACTIVE)
	song=f'E:/Projects/mp3/audio/{song}mp3'
	#Load play song with pygame
	pygame.mixer.music.load(song)
	#play song with pygame
	pygame.mixer.music.play(0,start=song_slider.get())


#create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#create volume slider frame
volumn_frame=LabelFrame(main_frame,text="Volumn")
volumn_frame.grid(row=0,column=1,padx=5)
#Create volume slider
volumn_slider=ttk.Scale(volumn_frame,from_=0, to=1,orient=VERTICAL,value=1,length=140,command=volume)
volumn_slider.pack(pady=10)

#Create song slider
song_slider=ttk.Scale(main_frame,from_=0, to=100,orient=HORIZONTAL,value=0,length=450,command=slide)
song_slider.grid(row=2,column=0,pady=10)

# Crete Playlist box
playlist_box=Listbox(main_frame,bg="black",fg="green",width=80,selectbackground="green",selectforeground="black")
playlist_box.grid(row=0,column=0)

#define button image for control
back_btn_img=PhotoImage(file='images/back.png')
forward_btn_img=PhotoImage(file='images/far.png')
play_btn_img=PhotoImage(file='images/play.png')
pause_btn_img=PhotoImage(file='images/pause.png')
stop_btn_img=PhotoImage(file='images/stop.png')

#Create Button Frame
control_frame=Frame(main_frame)
control_frame.grid(row=1,column=0)

#Create Play/Stop etc Button
back_button=Button(control_frame,image=back_btn_img,borderwidth=0,command=previous_song)
forward_button=Button(control_frame,image=forward_btn_img,borderwidth=0,command=next_song)
play_button=Button(control_frame,image=play_btn_img,borderwidth=0,command=play)
pause_button=Button(control_frame,image=pause_btn_img,borderwidth=0,command=lambda:pause(paused))
stop_button=Button(control_frame,image=stop_btn_img,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

#create menu
my_menu=Menu(root)
root.config(menu=my_menu)

#create add song menu dropdown
add_song_menu=Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Songs",menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Plylist",command=add_song)
add_song_menu.add_command(label="Add Many Song To Plylist",command=add_many_song)

#create delete song menu dropdown
remove_song_menu=Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Delete Song",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete One Song To Plylist",command=delete_song)
remove_song_menu.add_command(label="Delete All Song To Plylist",command=delete_all_songs)

#create status Bar
status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2)

#temporary Label
my_label=Label(root,text="")
my_label.pack(pady=20)




root.mainloop()
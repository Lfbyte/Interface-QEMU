'''
# Author: Lfbyte
# Github: https://github.com/Lfbyte
# License: MIT
# Versao: 1.0
'''

import os
import time
from tkinter import *
from tkinter import filedialog


def init():
		#processador
		p = smp.get()
		#memória
		m = memory.get()
		#kvm
		k = chk.get()
		#hdd
		hd = hda.get()
		#iso
		cd = iso.get()
		
		if p == "" or m == "" :
			throwError("PROCESSADOR ou MEMÓRIA não estão preenchidos!")
		
		
		#Instalacao completa em modo live com suporte KVM
		
		elif p != "" and m != "" and k == 1 and hd != "" and cd != "":
			os.system(f"qemu-system-x86_64 --enable-kvm -vga virtio -smp {p} -boot d -cdrom {cd} -m {m}G -hda {hd} &")		  

		
		#instalacao completa em  modo live sem supporte ao KVM
		elif p != "" and m != "" and k == 0 and hd != "" and cd != "":
			os.system(f"qemu-system-x86_64 -vga virtio -smp {p} -boot d -cdrom {cd} -m {m}G -hda {hd} &")		  
			
		
		#boot do sistema alocado no HDA sem suporte ao KVM
		elif p != "" and m != "" and k == 0 and hd != "" and cd == "":
			os.system(f"qemu-system-x86_64 -vga virtio -smp {p} -m {m}G -hda {hd} &")	
			
		
		#boot do sistema  alocado no HDA com suporte ao KVM
		elif p != "" and  m != ""  and k == 1  and hd != "" and cd == "":
			os.system(f"qemu-system-x86_64 --enable-kvm -vga virtio -smp {p} -m {m}G -hda {hd} &")
			
		
		#boot apenas da iso LIVE sem HDA com suporte ao KVM
		elif p != "" and m != "" and k == 1 and hd == "" and cd != "":
			os.system(f"qemu-system-x86_64 --enable-kvm -vga virtio -smp {p} -boot d -cdrom {cd} -m {m}G &")	
			
		
		#boot apenas da iso LIVE sem HDA e SEM suporte ao KVM
		elif p != "" and m != "" and k == 0 and hd == "" and cd != "":
			os.system(f"qemu-system-x86_64 -vga virtio -smp {p} -boot d -cdrom {cd} -m {m}G &")	

		else:
			throwError("Parâmetros inválidos")

def throwError(status):
	error = Tk()
	error.geometry('235x80')
	error.title("ERRO")
	Label(error, text=f'O parâmetro de {status}').place(x=10, y=10)
	Button(error,text="OK", command=error.destroy).place(x=105, y=30)	

def procurar_hda():
	caminho_hda = filedialog.askopenfilenames(filetypes=[("Arquivo HDA",".qcow2")],initialdir=user)
	hda.insert(0,caminho_hda)

def procurar_iso():
	caminho_iso = filedialog.askopenfilenames(filetypes=[("Arquivo ISO",".iso")],initialdir=user)
	iso.insert(0,caminho_iso)


def gui():
	try:
		#variaveis globais
		global tk 
		global smp
		global chk
		global memory 
		global hda
		global iso
		global user
		absolute = os.system("whoami > /dev/null")
		user = f"/home/{absolute}"
		#INICIALIZAR INTERFACE :D	
		tk = Tk()
		tk.geometry('680x420')
		tk.title("Interface-QEMU")
		
		#Definicao de labels dos campos
		Label(tk, text="Quantidade de Processadores: ").place(x=10,y=10)
		Label(tk, text="Quantidade de Memória: ").place(x=10, y=70)
		Label(tk, text='HDA (arquivo.qcow2)').place(x=10, y=115)
		Label(tk, text='ISO (arquivo.iso)').place(x=10, y=170)		
		
		# ------> Posicao dos Entry's <---------- #
		
		#Entry do PROCESSADOR
		smp = Entry(tk)
		smp.place(x=10,y=30,width=50,height=20)
		
		#Entry da MEMORIA
		memory = Entry(tk)
		memory.place(x=10, y=90, width=50,height=20)
		
		#Entry do HDA
		hda = Entry(tk)
		hda.place(x=10, y=140, width=400, height=20)
		
		#Entry da ISO
		iso = Entry(tk)
		iso.place(x=10, y= 195, width=400, height=20)


		#transformando a garela em Int \o/
		chk = IntVar()

		#--- Definindo checkboxes e Buttons ---
		#--- kvm ---
		kvm = Checkbutton(tk, text="Habilitar KVM", variable=chk)
		kvm.place(x=10, y=220)
		
		# ---- buttons de search
		Button(tk, text="...", command=procurar_hda,cursor="hand2").place(x=420, y=140 , height=20)
		Button(tk, text="...", command=procurar_iso,cursor="hand2").place(x=420, y=195 , height=20)
		
		# ---- buttons de action
		Button(tk, text="Executar", command=init,cursor="hand2").place(x=10, y=250)
		Button(tk, text="Sair",cursor="hand2", command=tk.destroy).place(x=95, y=250)
	
	except KeyboardInterrupt:
		throwError("Encerrado pelo usuario...")
	tk.mainloop()
try:
	gui()
except:	
	tk.destroy()
	global message 
	message = Tk()
	message.title("Erro")
	message.geometry("235x80")
	Label(message, text=f'Ocorreu um erro inesperado, encerrando...').place(x=10, y=10)
	Button(message,text="OK", command=message.destroy).place(x=105, y=30)	
	message.mainloop()

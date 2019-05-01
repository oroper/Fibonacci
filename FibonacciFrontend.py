# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import create_connection
import wx
import threading
from pubsub import pub


class Interfaccia(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        print('tread del Frame: ' + str(threading.get_ident()))

        self.panel = wx.Panel(self)
        self.answare = wx.StaticText(self.panel, label="Risultato:")
        self.result = wx.StaticText(self.panel, label="")
        self.result.SetForegroundColour(wx.RED)
        self.button = wx.Button(self.panel, label="Calcola")
        self.request = wx.StaticText(self.panel, label="Numero di cui calcolare la serie:")
        self.input = wx.TextCtrl(self.panel, size=(140, -1))

        # Set sizer for the frame, so we can change frame size to match widgets
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)

        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(5, 5)
        self.sizer.Add(self.request, (0, 0))
        self.sizer.Add(self.input, (0, 1))
        self.sizer.Add(self.button, (1, 0), flag=wx.EXPAND)
        self.sizer.Add(self.answare, (2, 0))
        self.sizer.Add(self.result, (2, 1))

        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)

        self.button.Bind(wx.EVT_BUTTON, self.onButton)
        pub.subscribe(self.printResult, 'result')

    def onButton(self, arg1):
        value = self.input.GetValue()
        pub.sendMessage('rootTopic', arg1=value)
        print("Messaggio inviato a rootTopic.")
        self.result.SetLabel("Calcolo in corso...")

    def printResult(self, arg):
        print('Ricevuto ' + arg)
        # self.result = wx.StaticText(self.panel, label=arg)
        self.result.SetLabel(arg)


def calc2(arg1):
    ws = create_connection(("127.0.0.1", 35491))
    '''"ws://localhost:8765"'''
    print(ws)
    byte2send = str.encode(arg1)
    ws.send(byte2send)
    print('Tread di attesa: ' + str(threading.get_ident()))
    data = ws.recv(1024)
    print(data.decode())
    pub.sendMessage('result', arg=data.decode())


def listRic(arg1):
    t3 = threading.Thread(target=calc2, args=[arg1])
    t3.daemon = True
    t3.start()


def connection():
    print("Task connection avviato.")
    print('Tread di Connection: ' + str(threading.get_ident()))
    pub.subscribe(listRic, 'rootTopic')


if __name__ == "__main__":
    t1 = threading.Thread(target=connection, name='t2')
    print("Thread di partenza: " + str(threading.get_ident()))

    t1.daemon = True
    # starting threads
    t1.start()

    app = wx.App(False)
    frame = Interfaccia(None)
    frame.Show()
    app.MainLoop()

    # wait until all threads finish
    t1.join()

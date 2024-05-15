import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio

QUIT = False

def quit_(window):
    print(window)
    global QUIT
    QUIT = True



class VentanaPrincipal(Gtk.ApplicationWindow):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    
        #------ventana principal-----------
        main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
        self.set_child(main_box)

        #------- caja que almacena un texto y otro ingresado por usuario -----
        text_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 10)
        main_box.append(text_box)

        label = Gtk.Label()
        label.set_text("Escribe algun chiste")
        text_box.append(label)

        self.texto = Gtk.Entry()
        text_box.append(self.texto)

        #---------boton para guardar----------

        boton = Gtk.Button()
        boton.set_label("Guardar")
        main_box.append(boton)
        boton.connect("clicked",self.on_clicked_open_dialog)

        #---------boton para imprimir en consola----------

        boton1 = Gtk.Button()
        boton1.set_label("Imprimir")
        main_box.append(boton1)
        boton1.connect("clicked", self.on_clicked_print_chiste)

        #---------boton para salir----------

        boton2 = Gtk.Button()
        boton2.set_label("Salir")
        main_box.append(boton2)
        boton2.connect("clicked", self.on_clicked_exit)



    def on_clicked_exit(self,boton2):
        sys.exit()


    def on_clicked_open_dialog(self,widget):

        # ------crear mensaje de dialogo ---------
        dialog = Gtk.MessageDialog(title="Ventana de guardado",
                                   transient_for=self,
                                   modal=True,
                                   default_width=300,
                                   default_height=50)

        # ----- añade texto debajo de titulo
        dialog.set_property("secondary-text",
                            "¿Estas seguro que quieres guardar ese chiste tan malo?")

        #-----
        dialog.add_buttons("Guardar", Gtk.ResponseType.OK,
                           "No Guardar", Gtk.ResponseType.CLOSE)
        
        dialog.set_deletable(True)

        dialog.connect("response", self.on_response_dialog)
        
        dialog.set_visible(True)

        pass

    def on_response_dialog(self, widget, response):
        # print(response)

        dialog = Gtk.FileDialog.new()
        if response == Gtk.ResponseType.OK:
            #guardar archivo
            print("VOY A GUARDAR EL ARCHIVO")
            dialog.save(self, None, self.save_dialog_open_response)
        elif response == Gtk.ResponseType.CLOSE:
            #no guardar el archivo
            print("NO QUISITE GUARDAR EL ARCHIVO")
        elif response == Gtk.ResponseType.DELETE_EVENT:
            print("Te saliste apretando ESC")
        #widget.destroy()
        widget.set_visible(False)


    def save_dialog_open_response(self, widget, response):
        archivo = widget.save_finish(response)
        print(f"File path is {archivo.get_path()}")
        chiste = self.texto.get_text()
        print(f"SE VA A GUARDAR: {chiste}")

        with open(archivo.get_path(), "w") as archivo:
            archivo.write(chiste)

        self.texto.set_text("")

    def on_clicked_print_chiste(self, widget):
        
        chiste = self.texto.get_text()
        print(f"El chiste es: {chiste}")
    
        pass





class MiAplicacion(Gtk.Application):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def do_activate(self):
        print("Se activa la Aplicacion")
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = VentanaPrincipal(application = self)
            self.win.present()

    def do_startup(self):
        print("Aplicación iniciada")
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        print("Aplicación cerrada")
        Gtk.Application.do_shutdown(self)



app = MiAplicacion()
app.run(sys.argv)



from PyQt5.QtWidgets import QApplication,QMainWindow, QDialog, QMessageBox, QFileDialog;
# from login import setupUi;
# from log_in import Ui_inicio_de_sesion
from PyQt5.uic import loadUi;
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore
import os
import pydicom
from PyQt5.QtGui import QPixmap

class Ventanaprincipal(QMainWindow):
    #constructor
    def __init__(self, ppal=None):
        super(Ventanaprincipal,self).__init__(ppal)
        loadUi("login.ui",self)
        self.setup()
        self.__carpeta = ""
        # self.ui=Ui_inicio_de_sesion()
        # self.ui.setupUi(self)
        
    #metodo para configurar las senales-slots y otros de la interfaz
    
    def setup(self):
        #se programa la senal para el boton
        self.login.clicked.connect(self.accion_ingresar)
    
    def asignarControlador(self,c):
        self.__controlador = c

    def accion_ingresar(self):
        # print("Boton presionado")
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()
        #esta informacion la debemos pasar al controlador
        resultado = self.__controlador.validar_usuario(usuario,password)
        #se crea la ventana de resultado
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Resultado")
        #se selecciona el resultado de acuerdo al resultado de la operacion
        if resultado == True:
            self.abrirVentanaBuscarCarpeta()
        else:
            msg.setText("Usuario no Valido")
        #se muestra la ventana
            msg.show()

    def abrirVentanaBuscarCarpeta(self):
        ventana_browse=VentanaBuscarCarpeta(self)
        self.hide()
        ventana_browse.show()

    def recibir_imagen(self,imagen):
        self.__controlador.img_conextion(imagen)

    def recibir_imagen2(self,imagen):
        return self.__controlador.dcm_info(imagen)

class VentanaBuscarCarpeta(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('dialog_filesearch.ui',self)
        self.__ventanaPadre = ppal
        self.folder=""
        self.setup()

    def setup(self):
        self.browse.clicked.connect(self.browsefiles)
        self.buttonBox.accepted.connect(self.abrirVentanaVisualizacion)
        self.buttonBox.rejected.connect(self.cerrar)

    def browsefiles(self):
        carpeta=QFileDialog.getExistingDirectory(self,"Open File")
        self.filepath.setText(carpeta)
        self.folder=carpeta

    def cerrar(self):
        self.__ventanaPadre.show()

    def abrirVentanaVisualizacion(self):
        ventana_visualizacion=VentanaVisualizacion(self)
        self.hide()
        ventana_visualizacion.show()

    def recibir_imagen(self,imagen):
        self.__ventanaPadre.recibir_imagen(imagen)

    def recibir_imagen2(self,imagen):
        return self.__ventanaPadre.recibir_imagen2(imagen)

class VentanaVisualizacion(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('visualization.ui',self)
        self.__ventanaPadre = ppal
        self.file_number=0
        self.setup()

    def setup(self):
        self.cargar()
        self.buttonBox.rejected.connect(self.cerrar)
        self.hslider.valueChanged.connect(self.slider)

    def slider(self,value):
        self.file_number=value
        self.cargar()

    def cargar(self):
        folder=self.__ventanaPadre.folder
        archivos = os.listdir(folder)
        slider_max= len(archivos)-1
        self.hslider.setMaximum(slider_max)
        filename = archivos[self.file_number]
        imagen = f"{folder}/{filename}"
        self.__ventanaPadre.recibir_imagen(imagen)
        pixmap = QPixmap("temp_image.png")
        self.img.setPixmap(pixmap)
        os.remove('temp_image.png')
        # ds = pydicom.dcmread(imagen)
        # slice = str(ds["SliceLocation"])
        # image_type = str(ds["ImageType"])
        # study_description = str(ds["StudyDescription"])
        # series_decription = str(ds["SeriesDescription"])
        # modality = str(ds["Modality"])
        # dcm_info = f"{filename}\n\n{image_type}\n{study_description}\n{series_decription}\n{modality}\n{slice}"
        dcm_info = self.__ventanaPadre.recibir_imagen2(imagen)
        self.label.setText(f"{filename}\n\n{dcm_info}")

    def cerrar(self):
        self.__ventanaPadre.show()


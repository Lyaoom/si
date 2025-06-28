from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.utils import platform
import threading
import os
import sys

# Configuración específica para Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])

# Importar yt-dlp con manejo de errores
try:
    import yt_dlp as yt
except ImportError:
    print("yt-dlp no disponible, usando funcionalidad básica")
    yt = None

class YouTubeDownloaderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_downloading = False
        
    def build(self):
        self.title = "YouTube Downloader"
        
        # Layout principal con mejor espaciado para móvil
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # Título más grande para móvil
        title = Label(text='YouTube Downloader', 
                     size_hint_y=None, height=60,
                     font_size=28, bold=True)
        main_layout.add_widget(title)
        
        # Input para URL con mejor tamaño para móvil
        url_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100, spacing=5)
        url_layout.add_widget(Label(text='URL del video:', size_hint_y=None, height=30, font_size=16))
        self.url_input = TextInput(
            multiline=False, 
            hint_text='https://youtube.com/watch?v=...',
            size_hint_y=None, 
            height=50,
            font_size=14
        )
        url_layout.add_widget(self.url_input)
        main_layout.add_widget(url_layout)
        
        # Botón para ver información más grande
        self.info_button = Button(
            text='Ver Información del Video',
            size_hint_y=None, 
            height=60,
            font_size=16,
            background_color=(0.3, 0.6, 0.9, 1)
        )
        self.info_button.bind(on_press=self.mostrar_info)
        main_layout.add_widget(self.info_button)
        
        # Separador
        main_layout.add_widget(Label(
            text='--- Opciones de Descarga ---',
            size_hint_y=None, 
            height=40,
            font_size=16
        ))
        
        # Configuración de descarga con mejor layout para móvil
        config_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        
        # Directorio
        dir_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=60, spacing=5)
        dir_layout.add_widget(Label(text='Directorio:', size_hint_y=None, height=25, font_size=14))
        self.directorio_input = TextInput(
            text=self.get_default_directory(), 
            multiline=False,
            size_hint_y=None, 
            height=40,
            font_size=12
        )
        dir_layout.add_widget(self.directorio_input)
        config_layout.add_widget(dir_layout)
        
        # Tipo y Calidad en layout horizontal
        options_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        
        # Tipo
        tipo_layout = BoxLayout(orientation='vertical', spacing=5)
        tipo_layout.add_widget(Label(text='Tipo:', size_hint_y=None, height=25, font_size=14))
        self.tipo_spinner = Spinner(
            text='video',
            values=['video', 'musica'],
            size_hint_y=None, 
            height=40,
            font_size=14
        )
        self.tipo_spinner.bind(text=self.actualizar_calidades)
        tipo_layout.add_widget(self.tipo_spinner)
        options_layout.add_widget(tipo_layout)
        
        # Calidad
        calidad_layout = BoxLayout(orientation='vertical', spacing=5)
        calidad_layout.add_widget(Label(text='Calidad:', size_hint_y=None, height=25, font_size=14))
        self.resolucion_spinner = Spinner(
            text='720p',
            values=['360p', '480p', '720p', '1080p'],
            size_hint_y=None, 
            height=40,
            font_size=14
        )
        calidad_layout.add_widget(self.resolucion_spinner)
        options_layout.add_widget(calidad_layout)
        
        config_layout.add_widget(options_layout)
        main_layout.add_widget(config_layout)
        
        # Botón de descarga más grande
        self.download_button = Button(
            text='Descargar',
            size_hint_y=None, 
            height=70,
            font_size=18,
            background_color=(0.2, 0.7, 0.2, 1)
        )
        self.download_button.bind(on_press=self.iniciar_descarga)
        main_layout.add_widget(self.download_button)
        
        # Barra de progreso más visible
        self.progress_bar = ProgressBar(
            max=100, 
            value=0,
            size_hint_y=None, 
            height=30
        )
        main_layout.add_widget(self.progress_bar)
        
        # Label para estado más grande
        self.status_label = Label(
            text='Listo para descargar',
            size_hint_y=None, 
            height=40,
            font_size=14,
            text_size=(None, None)
        )
        main_layout.add_widget(self.status_label)
        
        # Inicializar calidades
        self.actualizar_calidades(None, 'video')
        
        return main_layout
    
    def get_default_directory(self):
        """Obtener directorio por defecto según la plataforma"""
        if platform == 'android':
            try:
                # Usar almacenamiento externo en Android
                external_path = primary_external_storage_path()
                return os.path.join(external_path, 'Download', 'YouTube')
            except:
                return '/storage/emulated/0/Download/YouTube'
        else:
            return './descargas'
    
    def actualizar_calidades(self, instance, value):
        """Actualizar opciones de calidad según el tipo seleccionado"""
        if value == 'musica':
            self.resolucion_spinner.values = ['128kbps', '192kbps', '320kbps']
            self.resolucion_spinner.text = '192kbps'
        else:
            self.resolucion_spinner.values = ['360p', '480p', '720p', '1080p']
            self.resolucion_spinner.text = '720p'
    
    def mostrar_info(self, instance):
        """Mostrar información del video en un popup"""
        if self.is_downloading:
            self.mostrar_popup("Aviso", "Hay una descarga en progreso")
            return
            
        url = self.url_input.text.strip()
        if not url:
            self.mostrar_popup("Error", "Por favor ingresa una URL")
            return
        
        if not yt:
            self.mostrar_popup("Error", "yt-dlp no está disponible")
            return
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=self.obtener_info_video, args=(url,), daemon=True).start()
    
    def obtener_info_video(self, url):
        """Obtener información del video (ejecutar en hilo separado)"""
        try:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Obteniendo información...'))
            
            yt_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False
            }
            
            with yt.YoutubeDL(yt_opts) as link:
                info = link.extract_info(url, download=False)
                
                titulo = info.get('title', 'No disponible')[:50] + ('...' if len(info.get('title', '')) > 50 else '')
                canal = info.get('uploader', 'No disponible')
                duracion = info.get('duration', 0)
                duracion_min = f"{duracion // 60}:{duracion % 60:02d}" if duracion else "No disponible"
                vistas = info.get('view_count', 0)
                vistas_texto = f"{vistas:,}" if vistas else "No disponible"
                
                info_text = f"""Título:
{titulo}

Canal: {canal}
Duración: {duracion_min}
Vistas: {vistas_texto}

¡Video encontrado correctamente!
Puedes proceder con la descarga."""
                
                # Mostrar popup en el hilo principal
                Clock.schedule_once(lambda dt: self.mostrar_popup("Información del Video", info_text))
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Información obtenida ✓'))
                
        except Exception as error:
            error_msg = str(error)[:100] + ('...' if len(str(error)) > 100 else '')
            Clock.schedule_once(lambda dt: self.mostrar_popup("Error", f"Error al obtener información:\n{error_msg}"))
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Error al obtener información ✗'))
    
    def iniciar_descarga(self, instance):
        """Iniciar descarga en hilo separado"""
        if self.is_downloading:
            self.mostrar_popup("Aviso", "Ya hay una descarga en progreso")
            return
            
        url = self.url_input.text.strip()
        if not url:
            self.mostrar_popup("Error", "Por favor ingresa una URL")
            return
        
        if not yt:
            self.mostrar_popup("Error", "yt-dlp no está disponible para descargas")
            return
        
        directorio = self.directorio_input.text.strip() or self.get_default_directory()
        tipo = self.tipo_spinner.text
        resolucion = self.resolucion_spinner.text
        
        # Marcar como descargando
        self.is_downloading = True
        self.download_button.disabled = True
        self.download_button.text = "Descargando..."
        self.download_button.background_color = (0.5, 0.5, 0.5, 1)
        
        # Ejecutar descarga en hilo separado
        threading.Thread(target=self.descargar_video, 
                        args=(url, directorio, tipo, resolucion), 
                        daemon=True).start()
    
    def hook_progreso(self, d):
        """Hook para mostrar progreso de descarga"""
        if d['status'] == 'downloading':
            try:
                if 'total_bytes' in d and d['total_bytes']:
                    porcentaje = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                    porcentaje = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                else:
                    porcentaje = 0
                
                Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', min(porcentaje, 100)))
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f'Descargando... {porcentaje:.1f}%'))
            except:
                pass
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 100))
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Procesando...'))
    
    def configurar_opciones(self, directorio, tipo, resolucion):
        """Configurar opciones de yt-dlp"""
        base_opts = {
            'outtmpl': os.path.join(directorio, '%(title)s.%(ext)s'),
            'progress_hooks': [self.hook_progreso],
            'no_warnings': True
        }
        
        if tipo.lower() == 'musica':
            if 'kbps' in resolucion:
                calidad = resolucion.replace('kbps', '')
            else:
                calidad = '192'
            
            base_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': calidad,
                }]
            })
        
        elif tipo.lower() == 'video':
            if 'p' in resolucion:
                altura = resolucion.replace('p', '')
                # Formato que funciona mejor en Android
                formato = f'best[height<={altura}]/best'
            else:
                formato = 'best'
            
            base_opts.update({
                'format': formato
            })
        
        return base_opts
    
    def descargar_video(self, url, directorio, tipo, resolucion):
        """Descargar video (ejecutar en hilo separado)"""
        try:
            # Crear directorio si no existe
            if not os.path.exists(directorio):
                os.makedirs(directorio)
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f'Directorio creado: {directorio}'))
            
            # Configurar opciones
            yt_opts = self.configurar_opciones(directorio, tipo, resolucion)
            
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 
                                                  f'Iniciando descarga {tipo} {resolucion}...'))
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 0))
            
            with yt.YoutubeDL(yt_opts) as link:
                link.download([url])
            
            # Actualizar UI en el hilo principal
            Clock.schedule_once(lambda dt: self.descarga_completada(True))
            
        except Exception as error:
            Clock.schedule_once(lambda dt: self.descarga_completada(False, str(error)))
    
    def descarga_completada(self, exito, error=None):
        """Manejar finalización de descarga"""
        self.is_downloading = False
        self.download_button.disabled = False
        self.download_button.text = "Descargar"
        self.download_button.background_color = (0.2, 0.7, 0.2, 1)
        self.progress_bar.value = 0
        
        if exito:
            self.status_label.text = "✅ Descarga completada!"
            self.mostrar_popup("Éxito", f"¡Descarga completada exitosamente!\n\nArchivo guardado en:\n{self.directorio_input.text}")
        else:
            error_msg = str(error)[:150] + ('...' if len(str(error)) > 150 else '')
            self.status_label.text = f"❌ Error en descarga"
            self.mostrar_popup("Error", f"Error durante la descarga:\n\n{error_msg}")
    
    def mostrar_popup(self, titulo, mensaje):
        """Mostrar popup con mensaje optimizado para móvil"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Label con texto ajustable
        label = Label(
            text=mensaje, 
            text_size=(350, None),
            halign='left',
            valign='middle',
            font_size=14
        )
        content.add_widget(label)
        
        # Botón más grande para móvil
        close_button = Button(
            text='Cerrar', 
            size_hint_y=None, 
            height=50,
            font_size=16,
            background_color=(0.3, 0.6, 0.9, 1)
        )
        content.add_widget(close_button)
        
        popup = Popup(
            title=titulo, 
            content=content, 
            size_hint=(0.9, 0.8),
            title_size=18
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()

# Ejecutar la aplicación
if __name__ == '__main__':
    YouTubeDownloaderApp().run()

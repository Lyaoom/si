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
import yt_dlp as yt
import os
import threading

class YouTubeDownloaderApp(App):
    def build(self):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(text='YouTube Downloader', 
                     size_hint_y=None, height=50,
                     font_size=24)
        main_layout.add_widget(title)
        
        # Input para URL
        url_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        url_layout.add_widget(Label(text='URL del video:', size_hint_x=0.3))
        self.url_input = TextInput(multiline=False, hint_text='https://youtube.com/watch?v=...')
        url_layout.add_widget(self.url_input)
        main_layout.add_widget(url_layout)
        
        # Botón para ver información
        self.info_button = Button(text='Ver Información del Video',
                                 size_hint_y=None, height=50)
        self.info_button.bind(on_press=self.mostrar_info)
        main_layout.add_widget(self.info_button)
        
        # Separador
        main_layout.add_widget(Label(text='--- Opciones de Descarga ---',
                                   size_hint_y=None, height=30))
        
        # Configuración de descarga
        config_layout = GridLayout(cols=2, size_hint_y=None, height=120, spacing=5)
        
        # Directorio
        config_layout.add_widget(Label(text='Directorio:'))
        self.directorio_input = TextInput(text='./descargas', multiline=False)
        config_layout.add_widget(self.directorio_input)
        
        # Tipo (Video o Audio)
        config_layout.add_widget(Label(text='Tipo:'))
        self.tipo_spinner = Spinner(text='video',
                                   values=['video', 'musica'])
        config_layout.add_widget(self.tipo_spinner)
        
        # Resolución
        config_layout.add_widget(Label(text='Calidad:'))
        self.resolucion_spinner = Spinner(text='720p',
                                         values=['144p', '240p', '360p', '480p', 
                                                '720p', '1080p', '4k', '128kbps', '192kbps', '320kbps'])
        config_layout.add_widget(self.resolucion_spinner)
        
        main_layout.add_widget(config_layout)
        
        # Botón de descarga
        self.download_button = Button(text='Descargar',
                                     size_hint_y=None, height=50,
                                     background_color=(0.2, 0.7, 0.2, 1))
        self.download_button.bind(on_press=self.iniciar_descarga)
        main_layout.add_widget(self.download_button)
        
        # Barra de progreso
        self.progress_bar = ProgressBar(max=100, value=0,
                                       size_hint_y=None, height=20)
        main_layout.add_widget(self.progress_bar)
        
        # Label para estado
        self.status_label = Label(text='Listo para descargar',
                                 size_hint_y=None, height=30)
        main_layout.add_widget(self.status_label)
        
        return main_layout
    
    def mostrar_info(self, instance):
        """Mostrar información del video en un popup"""
        url = self.url_input.text.strip()
        if not url:
            self.mostrar_popup("Error", "Por favor ingresa una URL")
            return
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=self.obtener_info_video, args=(url,)).start()
    
    def obtener_info_video(self, url):
        """Obtener información del video (ejecutar en hilo separado)"""
        try:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Obteniendo información...'))
            
            yt_opts = {
                'listformats': True,
                'quiet': True
            }
            
            with yt.YoutubeDL(yt_opts) as link:
                info = link.extract_info(url, download=False)
                
                titulo = info.get('title', 'No disponible')
                canal = info.get('uploader', 'No disponible')
                duracion = info.get('duration', 0)
                duracion_min = f"{duracion // 60}:{duracion % 60:02d}" if duracion else "No disponible"
                
                info_text = f"""Título: {titulo}
Canal: {canal}
Duración: {duracion_min}

Formatos disponibles:
"""
                
                # Mostrar algunos formatos principales
                formatos_mostrar = []
                for formato in info['formats'][:10]:  # Solo primeros 10
                    format_id = formato.get('format_id', 'N/A')
                    ext = formato.get('ext', 'N/A')
                    resolution = formato.get('resolution', formato.get('height', 'Audio'))
                    formatos_mostrar.append(f"• {format_id}: {ext} - {resolution}")
                
                info_text += "\n".join(formatos_mostrar)
                
                # Mostrar popup en el hilo principal
                Clock.schedule_once(lambda dt: self.mostrar_popup("Información del Video", info_text))
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Información obtenida'))
                
        except Exception as error:
            Clock.schedule_once(lambda dt: self.mostrar_popup("Error", f"Error al obtener información: {error}"))
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Error al obtener información'))
    
    def iniciar_descarga(self, instance):
        """Iniciar descarga en hilo separado"""
        url = self.url_input.text.strip()
        if not url:
            self.mostrar_popup("Error", "Por favor ingresa una URL")
            return
        
        directorio = self.directorio_input.text.strip() or './descargas'
        tipo = self.tipo_spinner.text
        resolucion = self.resolucion_spinner.text
        
        # Deshabilitar botón durante descarga
        self.download_button.disabled = True
        self.download_button.text = "Descargando..."
        
        # Ejecutar descarga en hilo separado
        threading.Thread(target=self.descargar_video, 
                        args=(url, directorio, tipo, resolucion)).start()
    
    def configurar_opciones(self, directorio, tipo, resolucion):
        """Configurar opciones de yt-dlp"""
        base_opts = {
            'outtmpl': f'{directorio}/%(title)s_{resolucion}.%(ext)s'
        }
        
        if tipo.lower() == 'musica':
            if 'kbps' in resolucion:
                calidad = resolucion.replace('kbps', '')
            else:
                calidad = '128'
            
            base_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': calidad,
                }]
            })
        
        elif tipo.lower() == 'video':
            if resolucion.lower() == '4k':
                formato = 'best[height<=2160]'
            elif 'p' in resolucion:
                altura = resolucion.replace('p', '')
                formato = f'best[height<={altura}]'
            else:
                formato = 'best[height<=720]'
            
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
            
            # Configurar opciones
            yt_opts = self.configurar_opciones(directorio, tipo, resolucion)
            
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 
                                                  f'Descargando {tipo} en {resolucion}...'))
            
            with yt.YoutubeDL(yt_opts) as link:
                link.download([url])
            
            # Actualizar UI en el hilo principal
            Clock.schedule_once(lambda dt: self.descarga_completada(True))
            
        except Exception as error:
            Clock.schedule_once(lambda dt: self.descarga_completada(False, str(error)))
    
    def descarga_completada(self, exito, error=None):
        """Manejar finalización de descarga"""
        self.download_button.disabled = False
        self.download_button.text = "Descargar"
        
        if exito:
            self.status_label.text = "✅ Descarga completada!"
            self.mostrar_popup("Éxito", "¡Descarga completada exitosamente!")
        else:
            self.status_label.text = f"❌ Error en descarga"
            self.mostrar_popup("Error", f"Error durante la descarga: {error}")
    
    def mostrar_popup(self, titulo, mensaje):
        """Mostrar popup con mensaje"""
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=mensaje, text_size=(400, None)))
        
        close_button = Button(text='Cerrar', size_hint_y=None, height=40)
        content.add_widget(close_button)
        
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.6))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

# Ejecutar la aplicación
if __name__ == '__main__':
    YouTubeDownloaderApp().run()
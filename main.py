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
import os
import threading
import requests
import json
import re

# Importaciones específicas para Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    from android import mActivity
    from jnius import autoclass, PythonJavaClass, java_method

class YouTubeDownloaderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_path = self.get_download_directory()
        
    def build(self):
        # Solicitar permisos en Android
        if platform == 'android':
            self.request_android_permissions()
        
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
        
        # Directorio (solo mostrar, se maneja automáticamente en Android)
        config_layout.add_widget(Label(text='Directorio:'))
        self.directorio_input = TextInput(text=self.download_path, multiline=False, readonly=True)
        config_layout.add_widget(self.directorio_input)
        
        # Tipo (Video o Audio)
        config_layout.add_widget(Label(text='Tipo:'))
        self.tipo_spinner = Spinner(text='video',
                                   values=['video', 'audio'])
        config_layout.add_widget(self.tipo_spinner)
        
        # Calidad
        config_layout.add_widget(Label(text='Calidad:'))
        self.calidad_spinner = Spinner(text='720p',
                                      values=['360p', '480p', '720p', '1080p', 'audio_128k', 'audio_320k'])
        config_layout.add_widget(self.calidad_spinner)
        
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
    
    def request_android_permissions(self):
        """Solicitar permisos necesarios en Android"""
        permissions = [
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.INTERNET
        ]
        request_permissions(permissions)
    
    def get_download_directory(self):
        """Obtener directorio de descarga apropiado para la plataforma"""
        if platform == 'android':
            try:
                # Usar el directorio de descargas público
                return os.path.join(primary_external_storage_path(), 'Download', 'YouTubeDownloader')
            except:
                # Fallback al directorio de la app
                return os.path.join(App.get_running_app().user_data_dir, 'downloads')
        else:
            return './descargas'
    
    def extract_video_id(self, url):
        """Extraer ID del video de YouTube de la URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_info_api(self, video_id):
        """Obtener información del video usando API alternativa"""
        try:
            # Usar una API pública para obtener información básica
            api_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'title': data.get('title', 'Video sin título'),
                    'author': data.get('author_name', 'Canal desconocido'),
                    'thumbnail': data.get('thumbnail_url', ''),
                    'duration': 'No disponible'
                }
        except Exception as e:
            print(f"Error obteniendo info del video: {e}")
        
        return None
    
    def mostrar_info(self, instance):
        """Mostrar información del video en un popup"""
        url = self.url_input.text.strip()
        if not url:
            self.mostrar_popup("Error", "Por favor ingresa una URL de YouTube")
            return
        
        video_id = self.extract_video_id(url)
        if not video_id:
            self.mostrar_popup("Error", "URL de YouTube no válida")
            return
        
        # Ejecutar en hilo separado
        threading.Thread(target=self.obtener_info_video, args=(video_id,)).start()
    
    def obtener_info_video(self, video_id):
        """Obtener información del video (ejecutar en hilo separado)"""
        try:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Obteniendo información...'))
            
            info = self.get_video_info_api(video_id)
            
            if info:
                info_text = f"""Título: {info['title']}
Canal: {info['author']}
Duración: {info['duration']}

ID del video: {video_id}
Estado: Listo para descargar"""
                
                Clock.schedule_once(lambda dt: self.mostrar_popup("Información del Video", info_text))
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Información obtenida'))
            else:
                Clock.schedule_once(lambda dt: self.mostrar_popup("Error", "No se pudo obtener información del video"))
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Error al obtener información'))
                
        except Exception as error:
            Clock.schedule_once(lambda dt: self.mostrar_popup("Error", f"Error: {str(error)}"))
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Error de conexión'))
    
    def iniciar_descarga(self, instance):
        """Iniciar descarga"""
        url = self.url_input.text.strip()
        if not url:
            self.mostrar_popup("Error", "Por favor ingresa una URL de YouTube")
            return
        
        video_id = self.extract_video_id(url)
        if not video_id:
            self.mostrar_popup("Error", "URL de YouTube no válida")
            return
        
        directorio = self.download_path
        tipo = self.tipo_spinner.text
        calidad = self.calidad_spinner.text
        
        # Deshabilitar botón durante descarga
        self.download_button.disabled = True
        self.download_button.text = "Preparando..."
        
        # Mostrar popup informativo para Android
        if platform == 'android':
            info_msg = """NOTA IMPORTANTE:
Este es un downloader básico para demostración.

Para descargas reales de YouTube en Android, 
necesitarías:
1. Usar bibliotecas nativas Android
2. Implementar extractores propios
3. Manejar restricciones de la plataforma

¿Continuar con la simulación?"""
            self.mostrar_popup_confirmacion("Información", info_msg, 
                                           lambda: self.simular_descarga(video_id, directorio, tipo, calidad))
        else:
            # En desktop, mostrar mensaje similar
            self.simular_descarga(video_id, directorio, tipo, calidad)
    
    def mostrar_popup_confirmacion(self, titulo, mensaje, callback):
        """Mostrar popup de confirmación"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=mensaje, text_size=(350, None), halign='left'))
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        
        ok_button = Button(text='Continuar', size_hint_x=0.5)
        cancel_button = Button(text='Cancelar', size_hint_x=0.5)
        
        button_layout.add_widget(ok_button)
        button_layout.add_widget(cancel_button)
        content.add_widget(button_layout)
        
        popup = Popup(title=titulo, content=content, size_hint=(0.9, 0.7))
        
        def on_ok(instance):
            popup.dismiss()
            callback()
        
        def on_cancel(instance):
            popup.dismiss()
            self.download_button.disabled = False
            self.download_button.text = "Descargar"
        
        ok_button.bind(on_press=on_ok)
        cancel_button.bind(on_press=on_cancel)
        popup.open()
    
    def simular_descarga(self, video_id, directorio, tipo, calidad):
        """Simular proceso de descarga"""
        threading.Thread(target=self.proceso_descarga_simulada, 
                        args=(video_id, directorio, tipo, calidad)).start()
    
    def proceso_descarga_simulada(self, video_id, directorio, tipo, calidad):
        """Simular descarga con barra de progreso"""
        try:
            # Crear directorio si no existe
            os.makedirs(directorio, exist_ok=True)
            
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 
                                                  f'Descargando {tipo} en {calidad}...'))
            
            # Simular progreso de descarga
            for i in range(0, 101, 5):
                Clock.schedule_once(lambda dt, progress=i: setattr(self.progress_bar, 'value', progress))
                Clock.schedule_once(lambda dt, progress=i: setattr(self.status_label, 'text', 
                                                                  f'Descargando... {progress}%'))
                threading.Event().wait(0.1)  # Simular tiempo de descarga
            
            # Crear archivo de ejemplo
            filename = f"video_{video_id}_{calidad}.{'mp4' if tipo == 'video' else 'mp3'}"
            filepath = os.path.join(directorio, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"Archivo de demostración\nTipo: {tipo}\nCalidad: {calidad}\nVideo ID: {video_id}")
            
            Clock.schedule_once(lambda dt: self.descarga_completada(True, filepath))
            
        except Exception as error:
            Clock.schedule_once(lambda dt: self.descarga_completada(False, str(error)))
    
    def descarga_completada(self, exito, resultado=None):
        """Manejar finalización de descarga"""
        self.download_button.disabled = False
        self.download_button.text = "Descargar"
        self.progress_bar.value = 0
        
        if exito:
            self.status_label.text = "✅ Descarga completada!"
            mensaje = f"¡Descarga completada!\n\nArchivo guardado en:\n{resultado}"
            self.mostrar_popup("Éxito", mensaje)
        else:
            self.status_label.text = f"❌ Error en descarga"
            self.mostrar_popup("Error", f"Error durante la descarga:\n{resultado}")
    
    def mostrar_popup(self, titulo, mensaje):
        """Mostrar popup con mensaje"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(text=mensaje, text_size=(350, None), halign='left')
        content.add_widget(label)
        
        close_button = Button(text='Cerrar', size_hint_y=None, height=40)
        content.add_widget(close_button)
        
        popup = Popup(title=titulo, content=content, size_hint=(0.9, 0.6))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

# Ejecutar la aplicación
if __name__ == '__main__':
    YouTubeDownloaderApp().run()

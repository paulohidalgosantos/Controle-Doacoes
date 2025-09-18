import os
import sys
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from constants import RED_WINE, WHITE, BACKGROUND


def resource_path(relative_path):
    """Retorna o caminho do recurso, compatível com PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco
        with self.canvas.before:
            Color(*BACKGROUND)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda inst, val: setattr(self.rect, 'size', val))
        self.bind(pos=lambda inst, val: setattr(self.rect, 'pos', val))

        layout = FloatLayout()

        # Logo no topo centralizado
        logo_path = resource_path(os.path.join("assets", "logo.jpg"))
        logo = Image(
            source=logo_path,
            size_hint=(None, None),
            size=(350, 350),
            pos_hint={"center_x": 0.5, "top": 0.95}
        )
        layout.add_widget(logo)

        # Título abaixo do logo
        titulo = Label(
            text="Controle de Doações",
            font_size=32,
            bold=True,
            color=RED_WINE,
            size_hint=(None, None),
            size=(400, 50),
            pos_hint={"center_x": 0.5, "top": 0.55}
        )
        layout.add_widget(titulo)

        # Botão Cadastrar Nova Doação (abaixo do título)
        btn_cadastro = Button(
            text="Cadastrar Nova Doação",
            size_hint=(0.8, None),
            height=60,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE,
            pos_hint={"center_x": 0.5, "top": 0.38}
        )
        btn_cadastro.bind(on_release=lambda x: setattr(self.manager, "current", "cadastro"))
        layout.add_widget(btn_cadastro)

        # Botão Próximas Doações (abaixo do primeiro botão)
        btn_lista = Button(
            text="Próximas Doações",
            size_hint=(0.8, None),
            height=60,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE,
            pos_hint={"center_x": 0.5, "top": 0.26}
        )
        btn_lista.bind(on_release=lambda x: setattr(self.manager, "current", "lista"))
        layout.add_widget(btn_lista)

        self.add_widget(layout)

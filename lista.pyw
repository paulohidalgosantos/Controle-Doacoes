from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from constants import RED_WINE, WHITE, BACKGROUND, DEFAULT_PADDING, DEFAULT_SPACING
import json
import os
from kivy.utils import platform

class TelaLista(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Caminho do arquivo JSON
        if platform == "android":
            try:
                from android.storage import app_storage_path
                pasta_app = app_storage_path()
            except:
                pasta_app = os.getcwd()
        else:
            pasta_app = os.getcwd()
        self.arquivo_json = os.path.join(pasta_app, "doacoes.json")

        # Fundo
        with self.canvas.before:
            Color(*BACKGROUND)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda inst, val: setattr(self.rect, 'size', val))
        self.bind(pos=lambda inst, val: setattr(self.rect, 'pos', val))

        self.layout_principal = BoxLayout(orientation="vertical", padding=DEFAULT_PADDING, spacing=DEFAULT_SPACING)

        # Título
        self.layout_principal.add_widget(Label(text="Lista de Doações", font_size=22, bold=True, size_hint=(1, None), height=40))

        # Entrada para selecionar dia
        self.input_dia = TextInput(size_hint=(1, None), height=40, hint_text="Digite o dia (DD/MM/AAAA)")
        self.layout_principal.add_widget(self.input_dia)

        # Botão filtrar
        btn_filtrar = Button(
            text="Filtrar",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE
        )
        btn_filtrar.bind(on_release=self.mostrar_doacoes)
        self.layout_principal.add_widget(btn_filtrar)

        # ScrollView para mostrar as doações
        self.scroll = ScrollView(size_hint=(1, 1))
        self.box_doacoes = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
        self.box_doacoes.bind(minimum_height=self.box_doacoes.setter('height'))
        self.scroll.add_widget(self.box_doacoes)
        self.layout_principal.add_widget(self.scroll)

        # Botão voltar
        btn_voltar = Button(
            text="Voltar",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE
        )
        btn_voltar.bind(on_release=lambda x: setattr(self.manager, "current", "menu"))
        self.layout_principal.add_widget(btn_voltar)

        self.add_widget(self.layout_principal)

    def mostrar_doacoes(self, instance):
        dia = self.input_dia.text.strip()
        self.box_doacoes.clear_widgets()

        if not os.path.exists(self.arquivo_json):
            return

        with open(self.arquivo_json, "r", encoding="utf-8") as f:
            try:
                doacoes = json.load(f)
            except json.JSONDecodeError:
                doacoes = []

        # Filtra as doações pelo dia informado
        doacoes_filtradas = [d for d in doacoes if d.get("dia") == dia]

        if not doacoes_filtradas:
            self.box_doacoes.add_widget(Label(text="Nenhuma doação encontrada neste dia.", size_hint_y=None, height=30))
            return

        for doacao in doacoes_filtradas:
            texto = f"Nome: {doacao['nome']}\nEndereço: {doacao['endereco']}\nItens: {doacao['itens']}"
            self.box_doacoes.add_widget(Label(text=texto, size_hint_y=None, height=80))

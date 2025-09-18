from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import platform
from kivy.clock import Clock
from kivy.app import App
import os
import json

from constants import (
    BACKGROUND, DEFAULT_PADDING, DEFAULT_SPACING, RED_WINE, WHITE,
    TITLE_SIZE, BUTTON_SIZE, BUTTON_HEIGHT
)


class TelaLista(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco do Screen
        with self.canvas.before:
            Color(*BACKGROUND)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda inst, val: setattr(self.rect, 'size', val))
        self.bind(pos=lambda inst, val: setattr(self.rect, 'pos', val))

        # Caminho do JSON
        if platform == "android":
            app = App.get_running_app()
            if app and getattr(app, "user_data_dir", None):
                pasta_app = app.user_data_dir
                
            else:
                pasta_app = os.getcwd()
        else:
            pasta_app = os.getcwd()
            
        self.arquivo_json = os.path.join(pasta_app, "doacoes.json")

        # Layout principal
        self.layout_principal = BoxLayout(
            orientation="vertical",
            padding=DEFAULT_PADDING,
            spacing=DEFAULT_SPACING
        )

        # Fundo branco do layout principal
        with self.layout_principal.canvas.before:
            Color(*BACKGROUND)
            rect_layout = Rectangle(size=self.layout_principal.size, pos=self.layout_principal.pos)
        self.layout_principal.bind(size=lambda inst, val: setattr(rect_layout, 'size', val))
        self.layout_principal.bind(pos=lambda inst, val: setattr(rect_layout, 'pos', val))

        # Campo de filtro por data
        filtro_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=40, spacing=10)
        self.input_data = TextInput(
            hint_text="Digite a data apenas com números (ddmmaaaa)",
            multiline=False,
            size_hint=(0.7, 1),
            font_size=BUTTON_SIZE,
            input_filter="int"
        )
        btn_filtrar = Button(
            text="Filtrar",
            size_hint=(0.3, 1),
            background_normal='',
            background_color=RED_WINE,
            color=WHITE,
            font_size=BUTTON_SIZE
        )
        btn_filtrar.bind(on_release=self.filtrar_doacoes)
        filtro_layout.add_widget(self.input_data)
        filtro_layout.add_widget(btn_filtrar)
        self.layout_principal.add_widget(filtro_layout)

        # Título
        self.layout_principal.add_widget(Label(
            text="Doações Cadastradas",
            font_size=TITLE_SIZE,
            bold=True,
            size_hint=(1, None),
            height=TITLE_SIZE*2,
            color=(0, 0, 0, 1)
        ))

        # ScrollView para rolagem das doações
        self.scrollview = ScrollView(size_hint=(1, 1))

        # BoxLayout que vai conter os cards
        self.box_doacoes = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None,
            padding=(0, 0, 0, 0)
        )
        self.box_doacoes.bind(minimum_height=self.box_doacoes.setter('height'))

        self.scrollview.add_widget(self.box_doacoes)
        self.layout_principal.add_widget(self.scrollview)

        # Botão Voltar
        btn_voltar = Button(
            text="Voltar",
            size_hint=(1, None),
            height=BUTTON_SIZE*BUTTON_HEIGHT*4,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE,
            font_size=BUTTON_SIZE
        )
        btn_voltar.bind(on_release=lambda x: setattr(self.manager, "current", "menu"))
        self.layout_principal.add_widget(btn_voltar)

        self.add_widget(self.layout_principal)

    def on_pre_enter(self, *args):
        self.carregar_doacoes()

    def filtrar_doacoes(self, instance):
        texto = self.input_data.text.strip()
        if texto and texto.isdigit() and len(texto) == 8:
            dia = texto[:2]
            mes = texto[2:4]
            ano = texto[4:]
            self.input_data.text = f"{dia}/{mes}/{ano}"
        self.carregar_doacoes(filtro=True)

    def carregar_doacoes(self, filtro=False):
        self.box_doacoes.clear_widgets()

        # Lê o arquivo JSON
        if os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, "r", encoding="utf-8") as f:
                try:
                    doacoes = json.load(f)
                except json.JSONDecodeError:
                    doacoes = []
        else:
            doacoes = []

        if filtro and self.input_data.text.strip():
            data_digitada = self.input_data.text.strip()
            doacoes = [d for d in doacoes if d.get('dia') == data_digitada]

        if not doacoes:
            self.box_doacoes.add_widget(Label(
                text="Nenhuma doação cadastrada.",
                size_hint_y=None,
                height=BUTTON_SIZE*2,
                color=(0, 0, 0, 1)
            ))
            return

        for doacao in doacoes:
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                size_hint_x=1,
                padding=20,
                spacing=DEFAULT_SPACING//2
            )

            # Fundo branco + borda
            with card.canvas.before:
                Color(1, 1, 1, 1)
                rect = Rectangle(pos=card.pos, size=card.size)
                Color(0, 0, 0, 1)
                border = Line(rectangle=(card.x, card.y, card.width, card.height), width=1.5)

            card.bind(pos=lambda inst, val, r=rect, b=border: (
                setattr(r, 'pos', inst.pos),
                setattr(b, 'rectangle', (inst.x, inst.y, inst.width, inst.height))
            ))
            card.bind(size=lambda inst, val, r=rect, b=border: (
                setattr(r, 'size', inst.size),
                setattr(b, 'rectangle', (inst.x, inst.y, inst.width, inst.height))
            ))

            # Texto da doação
            texto = (
                f"Nome: {doacao['nome']}\n"
                f"Endereço: {doacao['endereco']}\n"
                f"Dia: {doacao['dia']}\n"
                f"Itens: {doacao['itens']}"
            )

            label = Label(
                text=texto,
                color=(0,0,0,1),
                font_size=BUTTON_SIZE,
                halign="left",
                valign="top",
                size_hint_y=None,
                text_size=(self.scrollview.width - card.padding[0]*2, None)
            )

            # Ajusta altura do label conforme o texto renderiza
            def ajustar_label(inst, size):
                inst.height = size[1]
            label.bind(
                width=lambda inst, val, p=card.padding: setattr(inst, 'text_size', (val - p[0]*2, None)),
                texture_size=ajustar_label
            )

            card.add_widget(label)

            # 🔥 Agora cada card acompanha o SEU label
            def atualizar_altura_label(inst, h, c=card, l=label):
                nova_altura = l.height + c.padding[1] + c.padding[3]
                if c.height != nova_altura:
                    c.height = nova_altura

            label.bind(
                height=lambda inst, val, c=card, l=label: Clock.schedule_once(lambda dt: atualizar_altura_label(inst, val, c, l))
            )
            atualizar_altura_label(label, None, card, label)

            self.box_doacoes.add_widget(card)

        # Margem final
        self.box_doacoes.add_widget(Label(size_hint_y=None, height=10))

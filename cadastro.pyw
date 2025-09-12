# cadastro.pyw

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivymd.uix.picker import MDDatePicker
from constants import RED_WINE, WHITE, BACKGROUND, DEFAULT_PADDING, DEFAULT_SPACING, BUTTON_HEIGHT
import json
import os
from kivy.utils import platform

class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Determina o caminho do arquivo JSON
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

        layout = BoxLayout(orientation="vertical", padding=DEFAULT_PADDING, spacing=DEFAULT_SPACING)

        # Título
        layout.add_widget(Label(text="Cadastro de Doação", font_size=22, bold=True, size_hint=(1, None), height=40))

        # Campo: Nome do Doador
        layout.add_widget(Label(text="Nome do Doador:", size_hint=(1, None), height=30))
        self.input_nome = TextInput(size_hint=(1, None), height=40, hint_text="Digite o nome do doador")
        layout.add_widget(self.input_nome)

        # Campo: Endereço
        layout.add_widget(Label(text="Endereço:", size_hint=(1, None), height=30))
        self.input_endereco = TextInput(size_hint=(1, None), height=40, hint_text="Digite o endereço de retirada")
        layout.add_widget(self.input_endereco)

        # Campo: Dia da Retirada (com calendário)
        layout.add_widget(Label(text="Dia da Retirada:", size_hint=(1, None), height=30))
        self.input_dia = TextInput(size_hint=(1, None), height=40, hint_text="Clique no botão para escolher a data", readonly=True)
        layout.add_widget(self.input_dia)

        btn_calendario = Button(
            text="Selecionar Data",
            size_hint=(1, None),
            height=BUTTON_HEIGHT*300,  # ajusta tamanho proporcional
            background_normal='',
            background_color=RED_WINE,
            color=WHITE
        )
        btn_calendario.bind(on_release=self.abrir_calendario)
        layout.add_widget(btn_calendario)

        # Campo: Itens a serem retirados
        layout.add_widget(Label(text="Itens a serem retirados:", size_hint=(1, None), height=30))
        self.input_itens = TextInput(size_hint=(1, None), height=80, hint_text="Ex: 2 caixas de roupas, 3 cestas básicas")
        layout.add_widget(self.input_itens)

        # Botão Salvar
        btn_salvar = Button(
            text="Salvar Doação",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE
        )
        btn_salvar.bind(on_release=self.salvar_doacao)
        layout.add_widget(btn_salvar)

        # Botão Voltar
        btn_voltar = Button(
            text="Voltar",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE
        )
        btn_voltar.bind(on_release=lambda x: setattr(self.manager, "current", "menu"))
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def abrir_calendario(self, instance):
        date_dialog = MDDatePicker(callback=self.selecionar_data)
        date_dialog.open()

    def selecionar_data(self, date_obj):
        # Atualiza o TextInput com o formato DD/MM/AAAA
        self.input_dia.text = date_obj.strftime("%d/%m/%Y")

    def salvar_doacao(self, instance):
        # Ler dados atuais do JSON
        if os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, "r", encoding="utf-8") as f:
                try:
                    doacoes = json.load(f)
                except json.JSONDecodeError:
                    doacoes = []
        else:
            doacoes = []

        # Nova doação
        nova_doacao = {
            "nome": self.input_nome.text,
            "endereco": self.input_endereco.text,
            "dia": self.input_dia.text,
            "itens": self.input_itens.text
        }
        doacoes.append(nova_doacao)

        # Salvar no arquivo JSON
        with open(self.arquivo_json, "w", encoding="utf-8") as f:
            json.dump(doacoes, f, ensure_ascii=False, indent=4)

        # Limpar campos
        self.input_nome.text = ""
        self.input_endereco.text = ""
        self.input_dia.text = ""
        self.input_itens.text = ""

        print("Doação salva com sucesso!")

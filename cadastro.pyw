from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from constants import RED_WINE, WHITE, BACKGROUND, DEFAULT_PADDING, DEFAULT_SPACING
import json
import os
from kivy.app import App
from kivy.utils import platform
import sys

def resource_path(relative_path):
    """Retorna o caminho do recurso, compatível com PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Caminho do arquivo JSON
        if platform == "android":
            app = App.get_running_app()
            if app and getattr(app, "user_data_dir", None):
                pasta_app = app.user_data_dir
            else:
                pasta_app = os.getcwd()
        else:
            pasta_app = os.getcwd()

        os.makedirs(pasta_app, exist_ok=True)
        self.arquivo_json = os.path.join(pasta_app, "doacoes.json")

        # Fundo
        with self.canvas.before:
            Color(*BACKGROUND)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda inst, val: setattr(self.rect, 'size', val))
        self.bind(pos=lambda inst, val: setattr(self.rect, 'pos', val))

        # Layout principal
        self.layout = BoxLayout(orientation="vertical", padding=DEFAULT_PADDING, spacing=DEFAULT_SPACING)
        self.add_widget(self.layout)

        # Inicialmente mostra o formulário
        self.mostrar_formulario()

    def on_enter(self):
        """Garante que o formulário seja mostrado toda vez que a tela for exibida"""
        self.mostrar_formulario()

    def mostrar_formulario(self):
        """Mostra os campos de cadastro"""
        self.layout.clear_widgets()

        # Título
        self.layout.add_widget(Label(
            text="Cadastro de Doação",
            font_size=22,
            bold=True,
            size_hint=(1, None),
            height=40
        ))

        # Campo: Nome do Doador
        self.layout.add_widget(Label(text="Nome do Doador:", size_hint=(1, None), height=30))
        self.input_nome = TextInput(size_hint=(1, None), height=40, hint_text="Digite o nome do doador")
        self.layout.add_widget(self.input_nome)

        # Campo: Endereço
        self.layout.add_widget(Label(text="Endereço:", size_hint=(1, None), height=30))
        self.input_endereco = TextInput(size_hint=(1, None), height=40, hint_text="Digite o endereço de retirada")
        self.layout.add_widget(self.input_endereco)

        # Campo: Dia da Retirada
        self.layout.add_widget(Label(text="Dia da Retirada:", size_hint=(1, None), height=30))
        self.input_dia = TextInput(size_hint=(1, None), height=40, hint_text="DD/MM/AAAA")
        self.input_dia.bind(focus=self.formatar_data_apos_digitacao)
        self.layout.add_widget(self.input_dia)

        # Campo: Itens a serem retirados
        self.layout.add_widget(Label(text="Itens a serem retirados:", size_hint=(1, None), height=30))
        self.input_itens = TextInput(size_hint=(1, None), height=80, hint_text="Ex: 2 caixas de roupas, 3 cestas básicas")
        self.layout.add_widget(self.input_itens)

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
        self.layout.add_widget(btn_salvar)

        # Botão Voltar para menu
        btn_voltar = Button(
            text="Voltar",
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE
        )
        btn_voltar.bind(on_release=lambda x: setattr(self.manager, "current", "menu"))
        self.layout.add_widget(btn_voltar)

    def mostrar_confirmacao(self):
        """Mostra mensagem de sucesso com joinha e botão para voltar ao formulário de cadastro"""
        self.layout.clear_widgets()

        # Ícone de joinha centralizado usando resource_path
        joinha_path = resource_path(os.path.join("assets", "joinha.jpg"))
        icone = Image(
            source=joinha_path,
            size_hint=(None, None),
            size=(300, 300),
            pos_hint={"center_x": 0.5}
        )
        self.layout.add_widget(icone)

        # Mensagem de sucesso
        self.layout.add_widget(Label(
            text="Doação cadastrada com sucesso!",
            font_size=24,
            bold=True,
            color=RED_WINE,
            size_hint=(1, None),
            height=100
        ))

        # Botão Voltar para cadastro
        btn_voltar_cadastro = Button(
            text="Cadastrar Nova Doação",
            size_hint=(0.6, None),
            height=50,
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=RED_WINE,
            color=WHITE
        )
        btn_voltar_cadastro.bind(on_release=lambda x: self.mostrar_formulario())
        self.layout.add_widget(btn_voltar_cadastro)

    def formatar_data_apos_digitacao(self, instance, focused):
        if not focused:
            digits = ''.join(ch for ch in instance.text if ch.isdigit())
            if len(digits) == 8:
                instance.text = f"{digits[:2]}/{digits[2:4]}/{digits[4:]}"

    def salvar_doacao(self, instance):
        # Lê doações existentes
        if os.path.exists(self.arquivo_json):
            with open(self.arquivo_json, "r", encoding="utf-8") as f:
                try:
                    doacoes = json.load(f)
                except json.JSONDecodeError:
                    doacoes = []
        else:
            doacoes = []

        # Cria nova doação
        nova_doacao = {
            "nome": self.input_nome.text,
            "endereco": self.input_endereco.text,
            "dia": self.input_dia.text,
            "itens": self.input_itens.text
        }
        doacoes.append(nova_doacao)

        # Salva no JSON em arquivo temporário e substitui para evitar erros
        temp_file = self.arquivo_json + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(doacoes, f, ensure_ascii=False, indent=4)

        os.replace(temp_file, self.arquivo_json)

        # Tornar invisível no Windows
        if os.name == "nt":
            try:
                os.system(f'attrib +h "{self.arquivo_json}"')
            except Exception as e:
                print("Não foi possível ocultar o arquivo:", e)

        # Mostrar tela de confirmação com joinha
        self.mostrar_confirmacao()

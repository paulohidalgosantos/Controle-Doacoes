from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from constants import RED_WINE, WHITE, BACKGROUND

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # fundo branco
        with self.canvas.before:
            Color(*BACKGROUND)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=lambda inst, val: setattr(self.rect, 'size', val))
        self.bind(pos=lambda inst, val: setattr(self.rect, 'pos', val))

        layout = FloatLayout()

        # Logo no topo centralizado
        logo = Image(
            source="logo.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "top": 0.9}
        )
        layout.add_widget(logo)

        # Botão Cadastrar abaixo do logo com mais espaço
        btn_cadastro = Button(
            text="Cadastrar Nova Doação",
            size_hint=(0.8, None),
            height=60,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE,
            pos_hint={"center_x": 0.5, "top": 0.45}  # diminuiu top para aumentar espaço
        )
        btn_cadastro.bind(on_release=lambda x: setattr(self.manager, "current", "cadastro"))
        layout.add_widget(btn_cadastro)

        # Botão Próximas Doações abaixo do primeiro botão
        btn_lista = Button(
            text="Próximas Doações",
            size_hint=(0.8, None),
            height=60,
            background_normal='',
            background_color=RED_WINE,
            color=WHITE,
            pos_hint={"center_x": 0.5, "top": 0.30}  # ajusta posição vertical
        )
        btn_lista.bind(on_release=lambda x: setattr(self.manager, "current", "lista"))
        layout.add_widget(btn_lista)

        self.add_widget(layout)

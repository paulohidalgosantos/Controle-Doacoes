from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from menu import TelaInicial
from cadastro import TelaCadastro
from lista import TelaLista

class ControleDoacoesApp(App):
    def build(self):
        sm = ScreenManager()

        # adiciona telas
        sm.add_widget(TelaInicial(name="menu"))
        sm.add_widget(TelaCadastro(name="cadastro"))
        sm.add_widget(TelaLista(name="lista"))

        return sm

if __name__ == "__main__":
    ControleDoacoesApp().run()

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import sqlite3
import random
import configparser


def criar_tabela_usuarios():
    conn = sqlite3.connect('dados_loteria.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT NOT NULL,
                 senha TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def verificar_login(nome, senha):
    conn = sqlite3.connect('dados_loteria.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha))
    usuario = c.fetchone()
    conn.close()
    return usuario is not None


def cadastrar_usuario(nome, senha):
    conn = sqlite3.connect('dados_loteria.db')
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))
    conn.commit()
    conn.close()


def obter_credenciais_salvas():
    config = configparser.ConfigParser()
    config.read('credenciais.ini')
    if 'Credenciais' in config:
        nome = config['Credenciais'].get('nome')
        senha = config['Credenciais'].get('senha')
        return nome, senha
    return None, None


def salvar_credenciais(nome, senha):
    config = configparser.ConfigParser()
    config['Credenciais'] = {'nome': nome, 'senha': senha}
    with open('credenciais.ini', 'w') as configfile:
        config.write(configfile)


def gerar_dezenas_mega_sena():
    return random.sample(range(1, 61), 6)


def gerar_milhares_bicho():
    return [str(random.randint(0, 9999)).zfill(4) for _ in range(3)]


class CustomBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Fundo Branco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class LoteriaApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.salvar_checkbox = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"

        self.screen_manager = ScreenManager()

        self.mostrar_tela_login()

        return self.screen_manager

    def mostrar_tela_login(self, *args):  # Aceitando argumentos opcionais
        if not self.screen_manager.has_screen("login_screen"):
            screen = Screen(name="login_screen")
            layout = CustomBoxLayout(orientation="vertical", padding=50, spacing=30)
            
            # Adicionando o ícone
            icon_button = MDIconButton(icon="loteria_icon.png", icon_size="64sp")
            layout.add_widget(icon_button)

            self.nome_input = MDTextField(hint_text="Nome")
            self.nome_input.text_color = (0, 0, 0, 1)  # Definindo a cor do texto
            self.senha_input = MDTextField(hint_text="Senha", password=True)
            self.senha_input.text_color = (0, 0, 0, 1)  # Definindo a cor do texto
            self.salvar_checkbox = MDCheckbox(active=True, size_hint=(None, None), size=(48, 48))
            self.salvar_label = MDLabel(text="Salvar login e senha", theme_text_color="Custom", text_color=(0, 0, 0, 1))
            self.login_button = MDFlatButton(text="Login", text_color=(0, 0, 0, 1), md_bg_color=(0, 1, 0, 1), on_release=self.processar_login)
            self.cadastro_button = MDFlatButton(text="Cadastrar", text_color=(0, 0, 0, 1), md_bg_color=(0, 1, 0, 1), on_release=self.mostrar_tela_cadastro)
            self.login_message = MDLabel(theme_text_color="Custom", text_color=(0, 0, 0, 1))
            self.author_label = MDLabel(text="by Arleson Pontes, versão 1.0", halign="right", theme_text_color="Custom", text_color=(0, 0, 0, 1))

            layout.add_widget(self.nome_input)
            layout.add_widget(self.senha_input)
            layout.add_widget(self.salvar_checkbox)
            layout.add_widget(self.salvar_label)
            layout.add_widget(self.login_button)
            layout.add_widget(self.cadastro_button)
            layout.add_widget(self.login_message)
            layout.add_widget(self.author_label)

            screen.add_widget(layout)
            self.screen_manager.add_widget(screen)
        else:
            self.nome_input.text = ""
            self.senha_input.text = ""
            self.login_message.text = ""

        self.screen_manager.current = "login_screen"


    def processar_login(self, *args):
        nome = self.nome_input.text
        senha = self.senha_input.text
        if self.salvar_checkbox.active:
            salvar_credenciais(nome, senha)
        if verificar_login(nome, senha):
            self.mostrar_tela_principal(nome)
        else:
            self.login_message.text = "Login ou senha incorretos!"


    def mostrar_tela_cadastro(self, *args):
        if not self.screen_manager.has_screen("cadastro_screen"):
            screen = Screen(name="cadastro_screen")
            layout = CustomBoxLayout(orientation="vertical", padding=50, spacing=30)

            self.nome_input_cadastro = MDTextField(hint_text="Nome")
            self.nome_input_cadastro.text_color = (0, 0, 0, 1)  # Definindo a cor do texto
            self.senha_input_cadastro = MDTextField(hint_text="Senha", password=True)
            self.senha_input_cadastro.text_color = (0, 0, 0, 1)  # Definindo a cor do texto
            cadastro_button = MDFlatButton(text="Cadastrar", text_color=(0, 0, 0, 1), md_bg_color=(0, 1, 0, 1), on_release=self.processar_cadastro)
            self.cadastro_message = MDLabel(theme_text_color="Custom", text_color=(0, 0, 0, 1))
            voltar_login_button = MDFlatButton(text="Voltar ao Login", text_color=(0, 0, 0, 1), md_bg_color=(0, 1, 0, 1), on_release=self.mostrar_tela_login)
            self.author_label = MDLabel(text="by Arleson Pontes, versão 1.0", halign="right", theme_text_color="Custom", text_color=(0, 0, 0, 1))

            layout.add_widget(self.nome_input_cadastro)
            layout.add_widget(self.senha_input_cadastro)
            layout.add_widget(cadastro_button)
            layout.add_widget(self.cadastro_message)
            layout.add_widget(voltar_login_button)
            layout.add_widget(self.author_label)

            screen.add_widget(layout)
            self.screen_manager.add_widget(screen)
        self.screen_manager.current = "cadastro_screen"


    def processar_cadastro(self, *args):
        nome = self.nome_input_cadastro.text
        senha = self.senha_input_cadastro.text
        if nome and senha:
            if not verificar_login(nome, senha):
                cadastrar_usuario(nome, senha)
                self.nome_input_cadastro.text = ""
                self.senha_input_cadastro.text = ""
                self.screen_manager.current = "login_screen"
            else:
                self.cadastro_message.text = "Nome de usuário já em uso!"
        else:
            self.cadastro_message.text = "Preencha todos os campos!"

    def mostrar_tela_principal(self, nome):
        if not self.screen_manager.has_screen("principal_screen"):
            screen = Screen(name="principal_screen")
            layout = CustomBoxLayout(orientation="vertical", padding=50, spacing=30)

            bem_vindo_label = MDLabel(text=f"Bem-vindo, {nome}!", halign="center", theme_text_color="Custom", text_color=(0, 0, 0, 1), size_hint_y=None, height=dp(48))
            self.dezenas_label = MDLabel(theme_text_color="Custom", text_color=(0, 0, 0, 1))
            self.milhares_label = MDLabel(theme_text_color="Custom", text_color=(0, 0, 0, 1))
            mega_sena_button = MDFlatButton(text="Mega-Sena", text_color=(0, 0, 0, 1), md_bg_color=(0, 1, 0, 1), on_release=self.gerar_mega_sena)
            bicho_button = MDFlatButton(text="Jogo do Bicho", text_color=(0, 0, 0, 1), md_bg_color=(0, 1, 0, 1), on_release=self.gerar_bicho)
            logout_button = MDFlatButton(text="Logout", text_color=(0, 0, 0, 1), md_bg_color=(0, 1, 0, 1), on_release=self.mostrar_tela_login)
            self.author_label = MDLabel(text="by Arleson Pontes, versão 1.0", halign="right", theme_text_color="Custom", text_color=(0, 0, 0, 1))

            layout.add_widget(bem_vindo_label)
            layout.add_widget(self.dezenas_label)
            layout.add_widget(self.milhares_label)
            layout.add_widget(mega_sena_button)
            layout.add_widget(bicho_button)
            layout.add_widget(logout_button)
            layout.add_widget(self.author_label)

            screen.add_widget(layout)
            self.screen_manager.add_widget(screen)
        self.screen_manager.current = "principal_screen"

    def gerar_mega_sena(self, *args):
        dezenas = gerar_dezenas_mega_sena()
        self.dezenas_label.text = "Dezenas da Mega-Sena: " + ", ".join(map(str, dezenas))

    def gerar_bicho(self, *args):
        milhares = gerar_milhares_bicho()
        self.milhares_label.text = "Milhares do Jogo do Bicho: " + ", ".join(milhares)


if __name__ == "__main__":
    criar_tabela_usuarios()
    LoteriaApp().run()


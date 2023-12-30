from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QTimer
from PyQt5.QtGui import QIcon
import sqlite3

# FUNÇÕES

# Cria uma tabela no banco de dados quando o usuário abre o programa pela primeira vez
def cria_tabela():
    banco = sqlite3.connect('cadastro_de_pessoas.db')
    cursor = banco.cursor()

    while True:
        try:
            cursor.execute(""" CREATE TABLE "pessoa" (
"nome"	TEXT NOT NULL,
"dataNascimento" TEXT NOT NULL,
"nacionalidade"	TEXT NOT NULL,
"descricao"	TEXT NOT NULL
); """)
            banco.commit()

        except sqlite3.OperationalError:
            break # O laço de repetição é quebrado caso o usuário já tenha uma tabela criada
    banco.close()

def conectar_ao_database():
    banco = sqlite3.connect('cadastro_de_pessoas.db')
    return banco

def contagem_de_dados(banco):
    banco = conectar_ao_database()
    cursor = banco.cursor()
    cursor.execute('SELECT COUNT(*) FROM pessoa;')
    quantidade_de_dados = cursor.fetchone()[0]
    banco.close()

    if quantidade_de_dados > 0:
        tela_inicial_alternativa.show()
    else:
        tela_inicial.show()

def abrir_interface(): # Essa função determina se a interface "Tela Inicial" ou "Tela Inicial Alternativa" será mostrada na tela
    banco = conectar_ao_database()
    abrir = contagem_de_dados(banco)

def abrir_interface_de_cadastro():
    tela_inicial.close()
    tela_inicial_alternativa.close()

    cadastro.widget.hide()

    cadastro.show()

    # Reseta todos os widgets
    cadastro.dateEdit.setDate(QDate.currentDate())
    cadastro.dateEdit.setMaximumDate(QDate.currentDate()) # Define a data máxima que pode ser atribuída ao widget como a data atual
    cadastro.lineEdit.setText('')
    cadastro.lineEdit_2.setText('')
    cadastro.textEdit.setText('')

def sair_do_cadastro():
    cadastro.close()
    abrir_interface()

def abrir_listagem():
    tela_inicial_alternativa.close()
    listagem.show()
    listagem.lineEdit.setText('')

    listagem.listWidget.clear() # Reseta a listagem para mostrar os itens adicionados recentemente
    listagem.lineEdit.setPlaceholderText('Digite o nome aqui...')

    # Conecta ao banco de dados e cria um cursor
    banco = conectar_ao_database()
    cursor = banco.cursor()

    # O cursor executa um comando em SQL que faz com que apareça somente o nome das pessoas cadastradas na listagem
    cursor.execute('SELECT nome FROM pessoa;')
    dados_lidos = cursor.fetchall()
    for row in dados_lidos:
        item_text = row[0]
        listagem.listWidget.addItem(item_text)

    banco.close()

def pesquisar():

    banco = conectar_ao_database()
    cursor = banco.cursor()

    listagem.listWidget.clear()

    nome = listagem.lineEdit.text()

    cursor.execute(f"""SELECT * FROM pessoa WHERE nome LIKE '%{nome.strip().title()}%';""")
    dados_lidos = cursor.fetchall()
    for row in dados_lidos:
        item_text = row[0]
        listagem.listWidget.addItem(item_text)

    banco.close()

def abreBrowser():
    perfil_do_usuario.lineEdit.hide()
    perfil_do_usuario.dateEdit.hide()
    perfil_do_usuario.lineEdit_2.hide()
    perfil_do_usuario.textEdit.hide()

    perfil_do_usuario.pushButton_3.hide() # Botão: SALVAR
    perfil_do_usuario.pushButton_4.hide() # # Botão: CANCELAR

    perfil_do_usuario.textBrowser.show()
    perfil_do_usuario.textBrowser_2.show()
    perfil_do_usuario.textBrowser_3.show()
    perfil_do_usuario.textBrowser_4.show()

def fechaBrowser():
    perfil_do_usuario.textBrowser.hide()
    perfil_do_usuario.textBrowser_2.hide()
    perfil_do_usuario.textBrowser_3.hide()
    perfil_do_usuario.textBrowser_4.hide()
    
    perfil_do_usuario.lineEdit.show()
    perfil_do_usuario.dateEdit.show()
    perfil_do_usuario.lineEdit_2.show()
    perfil_do_usuario.textEdit.show()

    perfil_do_usuario.pushButton_3.show() # Botão: SALVAR
    perfil_do_usuario.pushButton_4.show() # # Botão: CANCELAR

def abrir_informacoes(nome):

    perfil_do_usuario.frame_5.hide()

    abreBrowser()
    perfil_do_usuario.pushButton.setText('EDITAR')
    perfil_do_usuario.pushButton_2.setText('VOLTAR')

    listagem.close()
    perfil_do_usuario.show()

    banco = conectar_ao_database()
    cursor = banco.cursor()

    nomeF = nome.text()
    cursor.execute(f'SELECT * FROM pessoa WHERE nome = "{nomeF}"')
    resultado = cursor.fetchone()

    if resultado:
        nomeF, dataNascimento, nacionalidade, descricao = resultado

        perfil_do_usuario.textBrowser.setPlainText(nomeF)
        perfil_do_usuario.textBrowser_2.setPlainText(dataNascimento)
        perfil_do_usuario.textBrowser_3.setPlainText(nacionalidade)
        perfil_do_usuario.textBrowser_4.setPlainText(descricao)

    banco.close()

def editar_informacoes():

    fechaBrowser()

    banco = conectar_ao_database()
    cursor = banco.cursor()

    nomeF = perfil_do_usuario.textBrowser.toPlainText()
    cursor.execute(f'SELECT * FROM pessoa WHERE nome = "{nomeF}"')
    resultado = cursor.fetchone()

    if resultado:
        nomeF, dataNascimento, nacionalidade, descricao = resultado

        data = QDate.fromString(dataNascimento, 'dd/MM/yyyy')

        perfil_do_usuario.lineEdit.setText(nomeF)
        perfil_do_usuario.dateEdit.setDate(data)
        perfil_do_usuario.lineEdit_2.setText(nacionalidade)
        perfil_do_usuario.textEdit.setPlainText(descricao)

    banco.close()

def clicar_em_excluir():
    perfil_do_usuario.frame_5.show()

def clica_em_nao():
    perfil_do_usuario.frame_5.hide()

def exclui_perfil():
    banco = conectar_ao_database()
    cursor = banco.cursor()

    nome = perfil_do_usuario.textBrowser.toPlainText()
    cursor.execute(f"""DELETE FROM pessoa
WHERE nome = '{nome}';""")
    
    banco.commit()
    banco.close()

    perfil_do_usuario.close()
    abrir_listagem()
    listagem.lineEdit.setText('')

def salvar_edicao():

    banco = conectar_ao_database()
    cursor = banco.cursor()

    nome = perfil_do_usuario.lineEdit.text()
    dataNascimento = perfil_do_usuario.dateEdit.date().toString('dd/MM/yyyy')
    nacionalidade = perfil_do_usuario.lineEdit_2.text()
    descricao = perfil_do_usuario.textEdit.toPlainText()

    if nome == '' or nacionalidade == '' or descricao == '':
        pass

    else:
        cursor.execute(f"""UPDATE pessoa
SET nome = '{nome.strip().title()}', dataNascimento = '{dataNascimento}', nacionalidade = '{nacionalidade.strip().capitalize()}', descricao = '{descricao.strip()}'
WHERE nome = '{perfil_do_usuario.textBrowser.toPlainText()}';""")
        banco.commit()
        banco.close()

        abreBrowser()

        perfil_do_usuario.textBrowser.setPlainText(nome)
        perfil_do_usuario.textBrowser_2.setPlainText(dataNascimento)
        perfil_do_usuario.textBrowser_3.setPlainText(nacionalidade)
        perfil_do_usuario.textBrowser_4.setPlainText(descricao)

def cancelar_edicao():

    abreBrowser()

def sair_do_perfil():
    perfil_do_usuario.close()
    abrir_listagem()
    listagem.lineEdit.setText('')

def sair_da_listagem():
    listagem.close()
    abrir_interface()

def fechar_widget():
    cadastro.widget.hide()

def cadastrando_pessoa():
    # Conecta ao banco de dados e cria um cursor
    banco = conectar_ao_database()
    cursor = banco.cursor()

    # Declarando variáveis para cada widget da interface gráfica
    nome = cadastro.lineEdit.text()
    dataNascimento = cadastro.dateEdit.date().toString('dd/MM/yyyy')
    nacionalidade = cadastro.lineEdit_2.text()
    descricao = cadastro.textEdit.toPlainText()

    # Se algum campo nos widgets estiver vazio ou o ano for maior que o atual, o programa não salvará nada
    if nome == '' or nacionalidade == '' or descricao == '':
        pass
    else:
        cursor.execute(f"""INSERT INTO pessoa (nome, dataNascimento, nacionalidade, descricao)
VALUES ('{nome.strip().title()}', '{dataNascimento}', '{nacionalidade.strip().capitalize()}', '{descricao.strip()}');""")
        
        banco.commit()
        banco.close()

        # Reseta todos os widgets
        cadastro.lineEdit.setText('')
        cadastro.dateEdit.setDate(QDate.currentDate())
        cadastro.lineEdit_2.setText('')
        cadastro.textEdit.setText('')

        cadastro.widget.timer = QTimer(cadastro.widget.show())
        cadastro.widget.timer.timeout.connect(fechar_widget)
        cadastro.widget.timer.start(2000)

# PROGRAMA PRINCIPAL

app = QtWidgets.QApplication([])

# Interfaces
tela_inicial = uic.loadUi('tela_inicial.ui')
tela_inicial_alternativa = uic.loadUi('tela_inicial_alternativa.ui')
cadastro = uic.loadUi('cadastro.ui')
listagem = uic.loadUi('listagem.ui')
perfil_do_usuario = uic.loadUi('perfil_do_usuario.ui')

icon = QIcon('icon.png')
tela_inicial.setWindowIcon(icon)
tela_inicial_alternativa.setWindowIcon(icon)
cadastro.setWindowIcon(icon)
listagem.setWindowIcon(icon)
perfil_do_usuario.setWindowIcon(icon)

cria_tabela()
abrir_interface()

# Atribuindo funções aos botões
tela_inicial.pushButton.clicked.connect(abrir_interface_de_cadastro)

cadastro.pushButton_2.clicked.connect(sair_do_cadastro)
cadastro.pushButton.clicked.connect(cadastrando_pessoa)

tela_inicial_alternativa.pushButton.clicked.connect(abrir_interface_de_cadastro)
tela_inicial_alternativa.pushButton_2.clicked.connect(abrir_listagem)

listagem.listWidget.itemClicked.connect(abrir_informacoes)
listagem.pushButton.clicked.connect(sair_da_listagem)
listagem.pushButton_2.clicked.connect(pesquisar)

perfil_do_usuario.pushButton.clicked.connect(editar_informacoes) # Botão: EDITAR
perfil_do_usuario.pushButton_2.clicked.connect(sair_do_perfil) # Botão: VOLTAR
perfil_do_usuario.pushButton_3.clicked.connect(salvar_edicao) # Botão: SALVAR
perfil_do_usuario.pushButton_4.clicked.connect(cancelar_edicao) # Botão: CANCELAR

perfil_do_usuario.pushButton_5.clicked.connect(clicar_em_excluir) # Botão: EXCLUIR
perfil_do_usuario.pushButton_6.clicked.connect(exclui_perfil) # Botão: Sim
perfil_do_usuario.pushButton_7.clicked.connect(clica_em_nao) # Botão: Não

app.exec()

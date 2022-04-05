from cgitb import text
import telebot
from telebot import  types    
from portalAlunoAtenas import Portal

CHAVE_API = "5222016126:AAGWngohEHyXs1b7KowefmdvvzKzEilbuDg"

bot = telebot.TeleBot(CHAVE_API)
portal = Portal()

messagemRequerimento = """
    Escolha uma opção?  (Clique em uma opção)
        /verTodos ver Todos requerimentos feitos por você
        /verTotal ver o total requerimentos feitos por você
        /verRecente ver o requerimento mais recente 

    /start voltar para o inicio"""

@bot.message_handler(commands=["verTodos"])
def verTodos(mensagem):

    bot.send_message(mensagem.chat.id, "Retornando todos os requerimentos...")
    
    texto = portal.MostrarTodosRequerimentos()

    bot.send_message(mensagem.chat.id, texto)

    texto = messagemRequerimento
    bot.send_message(mensagem.chat.id, texto)


@bot.message_handler(commands=["verTotal"])
def verTotal(mensagem):
    
    bot.send_message(mensagem.chat.id, "Retornando o total de requerimentos...")
    
    texto =  portal.TotalDeRequerimentos()

    bot.send_message(mensagem.chat.id, texto)

    texto = messagemRequerimento
    bot.send_message(mensagem.chat.id, texto)


@bot.message_handler(commands=["verRecente"])
def verRecente(mensagem):

    bot.send_message(mensagem.chat.id, "buscando o mais recente..")
    
    texto = portal.RequerimentoMaisRecente()

    bot.send_message(mensagem.chat.id, texto)

    texto = messagemRequerimento
    bot.send_message(mensagem.chat.id, texto)



@bot.message_handler(commands=["LogarPortal"])
def PegarCrendencialPortal(mensagem):

    
    markup = types.ForceReply( selective = False )
    msg = bot.send_message(mensagem.chat.id,"Qual é o seu login?", reply_markup = markup )

    bot.register_next_step_handler(msg, pegarLogin)


def pegarLogin(mensagem):
    user = mensagem.text
    portal.PegarLogin(user)
    markup = types.ForceReply( selective = False )
    msg = bot.send_message(mensagem.chat.id,f"Qual é a senha do Login '{user}' ?", reply_markup = markup )
    bot.register_next_step_handler(msg, pegarSenhaELogar)

def pegarSenhaELogar(mensagem):
    senha = mensagem.text

    portal.PegarSenha(senha)
    texto = ""

    try:

        bot.send_message(mensagem.chat.id, "Logando...")
        portal.Logar()
        bot.send_message(mensagem.chat.id, "Logado!")

        texto = """
        Escolha uma opção? (Clique em uma opção)
            /AbrirRequerimentoSolicitados Abrir menu sobre requerimentos"""

    except:
        texto = """Houve uma falha ao tentar logar
        /LogarPortal Tentar Logar no portal novamente?
        Clique na opção acima ou mandei qualquer mensagem
        """
    
    finally:
        bot.send_message(mensagem.chat.id, texto)
    

@bot.message_handler(commands=["AbrirRequerimentoSolicitados"])
def AbrirRequerimentosSolicitados(mensagem):

    texto = ""
    try:
        bot.send_message(mensagem.chat.id, "Abrindo...")
        portal.BuscarTodosRequementosFeito()
        bot.send_message(mensagem.chat.id, "Aberto...")

        texto = messagemRequerimento

    except:
        texto = """Houve uma falha ao tentar Abrir os Requerimentos
        /LogarPortal Tentar Logar no portal novamente?
        Clique na opção acima ou mandei qualquer mensagem
        """
    
    finally:
        bot.send_message(mensagem.chat.id, texto)




@bot.message_handler(commands=['start'])
def responder(mensagem):

    userName = mensagem.from_user.first_name
    texto = f"""
    Ola {userName}, sou o bot facul, o bot para acessar o portal do aluno Atenas😎!

    Escolha uma opção para continuar (Clique no item):
     /LogarPortal Logar no portal
    Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)

def generico(mensagem):
    return True

@bot.message_handler(func=generico)
def responder(mensagem):
    userName = mensagem.from_user.first_name
    texto = f"""
    Ola {userName}, 

    Escolha uma opção para continuar (Clique no item):
     /LogarPortal Logar no portal
    Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto)



bot.polling()
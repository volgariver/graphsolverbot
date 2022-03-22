import seaborn as sn
import networkx as nx
import matplotlib.pyplot as plt
from sympy import var
from sympy import sympify
import telebot
import PIL
from PIL import Image
from requests import get


bot = telebot.TeleBot('5184070809:AAFrb0k4GFSZSRGn5Dqb1eWChPZb5ERdDEw')

income2 = ['00','01','10','11']
income4 = ['000','001','010','011','100','101','110','111']


def fx(user_input, x, reduce=2):
    x = int(x, 2)
    
    ex = var('x')  
    expr = sympify(user_input)
    fa = expr.subs(ex, x)
    if fa<0:
            fa = '1'*reduce+bin(fa)[3:]
    else:
            fa = bin(fa)[2:]

    if len(fa)<3:
        fa = '00'+fa
    return fa[-reduce:]


def biectivnost(fnum):
    ans = 'Биективность для ' + fnum
    graphz = nx.MultiDiGraph()
    
    for i in income2:
        node = fx(fnum, i)
        ans += '\nx = ...***'+i +' -> f(x) = ...***' + node
        
        graphz.add_node(i)
        graphz.add_node(node)
        graphz.add_edge(i, node)
        
    nx.draw_circular(graphz,node_color='blue',
    node_size=1000,
    connectionstyle='arc3, rad = 0.1',
    with_labels=True)
    
    plt.savefig("biectivnost.png", format="PNG")
    plt.clf()
    return ans


def transitivnost(fnum):
    ans = 'Транзитивность для '+fnum
    graphz = nx.MultiDiGraph()
    arr = dict.fromkeys(income4)
    stateTr = True
    
    for i in income4:
        node = fx(fnum, i, 3)
        ans += '\nx = ...***'+i +' -> f(x) = ...***' + node
        
        arr[i]=node
        graphz.add_node(i)
        graphz.add_node(node)
        graphz.add_edge(i, node)
        
    for i in range(0, len(income4)-1):
        if arr[income4[i]] != income4[i+1]:
            stateTr = False
            break
    
    if stateTr:
        ans += '\n\nФункция транзитивна'
    else:
        ans += '\n\nФункция не транзитивна'
        
    nx.draw_circular(graphz,
    node_color='blue',
    node_size=1000,
    connectionstyle='arc3, rad = 0.1',
    with_labels=True)

    plt.savefig("transitivnost.png", format="PNG")
    plt.clf()
    return ans


def starterB(user_input):
    
    if '/' in user_input: 
        return "Данные введены некорректно :(\nПопробуйте заново.", False
       
    ex = var('x')  
    expr = sympify(user_input)
    fa = expr.subs(ex, 0)
    try:
        fa = bin(fa)[2:]
    except:
        KeyError
        return "Данные введены некорректно :(\nПопробуйте заново.", False
        
    return(biectivnost(user_input), True)
    
    
def starterT(user_input):
    if '/' in user_input: 
        return "Данные введены некорректно :(\nПопробуйте заново.",False
       
    ex = var('x')  
    expr = sympify(user_input)
    fa = expr.subs(ex, 0)
    try:
        fa = bin(fa)[2:]
    except:
        KeyError
        return "Данные введены некорректно :(\nПопробуйте заново.", False    
        
    return(transitivnost(user_input), True)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Напиши функцию, например такую:\n x*5+1-2')
                     
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() != '':
        
        bi =  starterB(message.text.lower())[0]
        tr = starterT(message.text.lower())[0]
        
        bistate = starterB(message.text.lower())[1]
        trstate = starterT(message.text.lower())[1]
        
        if bistate:
            bot.send_message(message.chat.id, bi)
            img = open('biectivnost.png', 'rb')
            bot.send_document(message.chat.id, img) 
        
        bot.send_message(message.chat.id, tr)
        
        if trstate:
            img = open('transitivnost.png', 'rb')
            bot.send_document(message.chat.id, img) 

        
    else:
        bot.send_message(message.chat.id, 'Hе читается, попробуй еще раз')

bot.polling()





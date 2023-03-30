import telebot 
import os
from telebot import types

class Gra():
    def __init__(self):
        f = open(os.path.join(os.path.dirname(__file__), "TOKEN.ini"), "r", encoding="UTF-8")
        self.bot = telebot.TeleBot(f.read())
        f.close()
        self.game = False

        @self.bot.message_handler(commands=["start"])
        def start(m):
            self.game = True
            self.board = [" "] * 9
            reply_markup = types.InlineKeyboardMarkup()
            buttons=[]
            for number in range(1,10):
                buttons.append(types.InlineKeyboardButton(text=str(number), callback_data=str(number)))
            reply_markup.row(buttons[0], buttons[1], buttons[2])
            reply_markup.row(buttons[3], buttons[4], buttons[5])
            reply_markup.row(buttons[6], buttons[7], buttons[8])
            self.bot.send_message(m.chat.id, "Zapraszam do gry \"tic tac tae\"! \n Naciśnij na przycisk poto żeby zagrać w swoją kolej", reply_markup=reply_markup)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.bot.send_message(call.message.chat.id, "Coś na pewno działa!")
            self.board=[" "] * 9
            reply_markup=self.zmienić_pole()
            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
            '''if self.game:
                index = int(call.data) - 1
                if self.is_valid_move(self.board, index):
                    self.make_move(self.board, index, "X")
                    winner = self.check_winner(self.board)
                    if winner:
                        reply_markup=self.zmienić_pole
                        self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
                        reply_markup = types.ReplyKeyboardRemove()
                        self.bot.send_message(call.message.chat.id, f"Wygrał {winner}", reply_markup=reply_markup)
                        self.game=False
                    elif self.any_is_empty(self.board):
                        index = self.get_computer_move(self.board)
                        self.make_move(self.board, index, "O")
                        winner = self.check_winner(self.board)
                        if winner:
                            reply_markup=self.zmienić_pole()
                            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
                            reply_markup = types.ReplyKeyboardRemove()
                            self.bot.send_message(call.message.chat.id, f"Wygrał {winner}", reply_markup=reply_markup)
                            self.game=False
                        else:
                            reply_markup=self.zmienić_pole
                            self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
                    else:
                        reply_markup=self.zmienić_pole(self.board)
                        self.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=reply_markup)
                        reply_markup = types.ReplyKeyboardRemove()
                        self.bot.send_message(call.message.chat.id, "Remis!", reply_markup=reply_markup)
                        self.game = False
                else:
                    self.bot.answer_callback_query(call.id, "Chybo źle grasz... Proszę spróbuj jeszcze raz.")
            else:
                self.bot.answer_callback_query(call.id, "Gra się skończyła, użyj komandy \"\\start\" żeby zacząć ponownie.")'''
    
    def zmienić_pole(self):
        reply_markup = types.InlineKeyboardMarkup()
        buttons = []
        for i in range(0,9):
            if self.is_empty(self.board, i):
                buttons.append(types.InlineKeyboardButton(text=" ", callback_data=str(i + 1)))
            else:
                buttons.append(types.InlineKeyboardButton(text=self.board[i], callback_data=str(i + 1)))
        reply_markup.row(buttons[0], buttons[1], buttons[2])
        reply_markup.row(buttons[3], buttons[4], buttons[5])
        reply_markup.row(buttons[6], buttons[7], buttons[8])
        return reply_markup


    def diplay_board(self, b):
        line = "|".join(b[0:3])
        print(line)
        print("-" * 5)
        line = "|".join(b[3:6])
        print(line)
        print("-" * 5)
        line = "|".join(b[6:9])
        print(line)

    def is_empty(self, b, index):
        return b[index] == " "

    def is_valid_move(self, b, index):
        res = (index >= 0) and (index <= 8) and self.is_empty(b, index)
        return res

    def check_winner(self, b):
        winners = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for winner in winners:
            if b[winner[0]] == b[winner[1]] == b[winner[2]] and b[winner[0]] != " ":
                return b[winner[0]]
        return False

    def make_move(self, b, index, symbol):
        b[index] = symbol
    
    def get_computer_move(self, b):
        for i in range(0, 9):
            if self.is_empty(b, i):
                board_copy = b[:]
                self.make_move(board_copy, i, "O")
                if self.check_winner(board_copy):
                    return i
        for i in [4, 0 ,2 ,6 ,8, 1, 3, 5, 7]:
            if self.is_empty(b, i):
                return i
    
    def any_is_empty(self, b):
        for i in range(9):
            point = self.is_empty(b, i)
            if point == True:
                break
        return point



gra = Gra()    
gra.bot.polling()
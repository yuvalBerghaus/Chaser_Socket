import json
import sys
import socket
import selectors
import types
import random
sel = selectors.DefaultSelector()


class Game:
    def __init__(self):
        self.players = {}
        self.chaser_stage = 0

        self.questions = {
            'A': [],
            'B': [],
            'C': [],
            'C+': []
        }
    def get_money(self,player_id):
        return self.players[player_id]['money']    
    def add_player(self, player_id, connection):
        self.players[player_id] = {
            'stage': 'A',
            'money': 0,
            'answered_count' : 0,
            'lifeline': True,
            'connection': connection,
            'correct_answers' : 0,
            'board_step' : 1
        }
    
    def remove_player(self, player_id):
        del self.players[player_id]
    
    def update_step_player(self, player_id, board_step):
        self.players[player_id]['board_step'] = int(board_step)

    def update_money(self, player_id, money):
        self.players[player_id]['money'] = money

    def generate_questions(self):
        level_a_questions = [
            {
                'id' : 1,
                'question': 'Who painted the Mona Lisa?',
                'options': ['Leonardo da Vinci', 'Vincent van Gogh', 'Pablo Picasso', 'Michelangelo'],
                'correct': 'A',
                'type' : 'question'
            },
            {
                'id' : 2,
                'question': 'Which planet is known as the "Red Planet"?',
                'options': ['Mars', 'Jupiter', 'Venus', 'Saturn'],
                'correct': 'A',
                'type' : 'question'
            },
            {
                'id' : 3,
                'question' : 'Who is the author of the famous novel "To Kill a Mockingbird"?',
                'options': ['J.D. Salinger', 'Harper Lee', 'F. Scott Fitzgerald', 'Ernest Hemingway'],
                'correct': 'B',
                'type' : 'question'
            }
        ]
        self.questions['A'] = random.sample(level_a_questions, 3)

        
        # Level B questions
        level_b_questions = [
            {
                'id' : 1,
                'question': 'What is the capital city of Australia?',
                'options': ['Sydney', 'Canberra', 'Melbourne', 'Perth'],
                'correct': 'B',
                'type' : 'question'
            },
            {
                'id' : 2,
                'question': 'Which country is famous for the Taj Mahal?',
                'options': ['India', 'China', 'Egypt', 'Italy'],
                'correct': 'A',
                'type' : 'question'
            },
            {
                'id' : 3,
                'question': 'Who wrote the novel "1984"?',
                'options': ['George Orwell', 'J.R.R. Tolkien', 'Jane Austen', 'F. Scott Fitzgerald'],
                'correct': 'A',
                'type' : 'question'
            }
        ]
        self.questions['B'] = random.sample(level_b_questions, 3)
        
        # Level C questions
        level_c_questions = [
            {
                'id' : 1,
                'question': 'Who wrote the play "Romeo and Juliet"?',
                'options': ['William Shakespeare', 'Charles Dickens', 'Jane Austen', 'F. Scott Fitzgerald'],
                'correct': 'A',
                'type' : 'question'
            },
            {
                'id' : 2,
                'question': 'Which animal is the largest living mammal?',
                'options': ['Blue whale', 'African elephant', 'Giraffe', 'Hippopotamus'],
                'correct': 'A',
                'type' : 'question'
            },
            {
                'id' : 3,
                'question': 'What is the largest organ in the human body?',
                'options': ['Liver', 'Heart', 'Skin', 'Brain'],
                'correct': 'C',
                'type' : 'question'
            }
        ]
        self.questions['C'] = random.sample(level_c_questions, 3)
        
        # Level C+ questions
        level_c_plus_questions = [
            {
                'question': 'What is the chemical symbol for gold?',
                'options': ['Au', 'Ag', 'Fe', 'Hg'],
                'correct': 'A',
                'type' : 'question'
            },
            {
                'question': 'Who discovered penicillin?',
                'options': ['Alexander Fleming', 'Marie Curie', 'Albert Einstein', 'Isaac Newton'],
                'correct': 'A',
                'type' : 'question'
            }
        ]
        self.questions['C+'] = random.sample(level_c_plus_questions, 2)

    #this function handles the answer and updates a new question!   
    def process_answer(self, player_id, answer):
        player = self.players[player_id]
        if str(answer).lower() == "correct":
            player['correct_answers'] += 1
            if player['stage'] == 'A':
                player['money'] += 5000
        #else incorrect answer
        elif str(answer).lower() == "incorrect":
            #TODO - handle
            print("incorrect!")
        player['answered_count'] += 1

        # handle stage to stage!
        if player['answered_count'] == 4 and player['stage'] == 'A':
            if player['correct_answers'] > 0:
                #TODO - check if he was on stage A and if he was then send him the options of how much he wants to continue with - 2*current_amount or current_amount/2 or current
                self.move_player_forward(player_id)
            #meaning that he didnt answer any of the questions right
            else:
                player['stage'] = 'A'

    def get_next_stage(self, current_stage):
        if current_stage == 'A':
            return 'B'
        elif current_stage == 'B':
            return 'C'
        elif current_stage == 'C':
            return 'C+'

    def move_player_forward(self, player_id):
        player = self.players[player_id]
        player['answered_count'] = 0
        player['correct_answers'] = 0
        current_stage = player['stage']
        # current_position = self.get_stage_position(current_stage) # TODO - finished stage A!!!!
        next_stage = self.get_next_stage(current_stage)        
        # Update player's stage and position
        player['stage'] = next_stage

    def get_current_question(self, player_id):
        player = self.players[player_id]
        current_stage = player['stage']
        # current_question_index = self.get_stage_position(current_stage, player['answered_count']) - 1
        current_question_index = player['answered_count']-1
        if len(self.questions[current_stage]) > current_question_index:
            return self.questions[current_stage][current_question_index]
        else:
            return None



def accept_wrapper(sock, game):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    player_id = addr[1]  # Assuming unique port numbers as player IDs
    game.add_player(player_id, conn)
    # game.generate_questions()
    # send_question(conn, game.get_current_question(player_id))
    


def send_phaseB_message(conn, current_amount):
    divided = current_amount / 2
    double = current_amount * 2
    
    instructions = {
        "message": "Congratz!",
        "type" : "B",
        "current_amount": current_amount,
        "choices": [
            {"step": 2, "value": double},
            {"step": 3, "value": current_amount},
            {"step": 4, "value": divided}
        ]
    }
    
    instructions_json = json.dumps(instructions)
    conn.sendall(instructions_json.encode())



def send_question(conn, question):
    if question is None:
        send_game_summary(conn)
    else:
        data_json = json.dumps(question)
        conn.sendall(data_json.encode())


def handle_question_response(sock, game, player_id, response):
    current_stage = game.players[player_id]['stage']
    current_question = game.get_current_question(player_id)
    game.process_answer(player_id, response.lower())
    # WHEN THE PLAYER GETS TO PHASE B IM ASKING HIM IF HE WANTS TO DOUBLE OR CURRENT OR DIVIDED 
    if game.players[player_id]['stage'] == 'B':
        send_phaseB_message(sock,game.players[player_id]['money'])
    else:
        next_question = game.get_current_question(player_id)
        if next_question:
            send_question(sock, next_question)
        else:
            print("GAME OVER")



def handle_initial_response(sock, game, player_id, response):
    if response.lower() == 'yes':
        # Player wants to play, generate questions and send Level A question
        game.generate_questions()
        # send_question(sock, game.get_current_question(player_id))
    else:
        # Player does not want to play, end the connection
        sock.sendall("Thank you for playing!".encode())
        sel.unregister(sock)
        sock.close()
        game.remove_player(player_id)


def handle_phase_B(sock,game,player_id,board_step):
    game.update_step_player(player_id, board_step)
    if board_step == '2':
        game.update_money(player_id, game.get_money(player_id)*2) #TODO
    elif board_step == '4':
        game.update_money(player_id, game.get_money(player_id) / 2) #TODO
def service_connection(key, mask, game):
    sock = key.fileobj
    data = key.data
    
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            message = recv_data.decode().strip()
            player_id = data.addr[1]
            #TODO - handle all phases first response!
            if player_id in game.players:
                if message.lower() == 'yes':
                    handle_initial_response(sock, game, player_id, message)
                    handle_question_response(sock, game, player_id, message)
                elif game.players[player_id]['stage'] == 'C+':
                    handle_game_over_response(sock, game, player_id, message)
                elif game.players[player_id]['stage'] == 'B':
                    handle_phase_B(sock,game,player_id,message)
                else:
                    handle_question_response(sock, game, player_id, message)

        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
            player_id = data.addr[1]
            game.remove_player(player_id)
    
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]




# Server setup
host, port = "127.0.0.1", 65432
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

game = Game()

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj, game)
            else:
                service_connection(key, mask, game)

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

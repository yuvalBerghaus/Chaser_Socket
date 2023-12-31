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
        self.chaser_step = 1
        self.questions = {
            'A': [],
            'B': [],
            'C': [],
            'C+': []
        }
    def send_board_info(self, player_id):
        player = self.players[player_id]
        current_step = player['board_step']
        chaser_step = game.chaser_step
        message_type = "board_info"
        current_money = player['money']
        lifeline = player['lifeline']
        # Prepare board info message
        message = f"Money: {current_money} | Player_Stage: {current_step} | Chaser: {chaser_step} | Lifeline: {lifeline}\n"

        # Send board info to the player
        conn = player['connection']

        conn.send(message.encode())

    def get_board_info(self, player_id):
        player = self.players[player_id]
        current_step = player['board_step']
        chaser_step = game.chaser_step
        message_type = "board_info"
        current_money = player['money']
        lifeline = player['lifeline']
        # Prepare board info message
        message = f"Money: {current_money} | Player_Stage: {current_step} | Chaser: {chaser_step} | Lifeline: {lifeline}\n"
        return message

    def has_lifeline(self,player_id):
        return self.players[player_id]['lifeline']
    def get_step(self,player_id):
        return self.players[player_id]['board_step']
    def get_money(self,player_id):
        return self.players[player_id]['money']  
    def get_stage(self,player_id):
        return self.players[player_id]["stage"]  
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
    def turn_off_lifeline(self,player_id):
        self.players[player_id]['lifeline'] = False
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

        # Level C questions
        level_c_questions = [
        {
            'question': 'Who wrote the play "Romeo and Juliet"?',
            'options': ['William Shakespeare', 'Charles Dickens', 'Jane Austen', 'F. Scott Fitzgerald'],
            'correct': 'A',
            'reduced_options': ['William Shakespeare', 'Jane Austen'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Which animal is the largest living mammal?',
            'options': ['Blue whale', 'African elephant', 'Giraffe', 'Hippopotamus'],
            'reduced_options': ['Blue whale', 'African elephant'],
            'correct': 'A',
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'What is the chemical symbol for gold?',
            'options': ['Au', 'Ag', 'Fe', 'Hg'],
            'correct': 'A',
            'reduced_options': ['Au', 'Fe'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'What is the largest organ in the human body?',
            'options': ['Liver', 'Heart', 'Skin', 'Brain'],
            'reduced_options': ['Skin', 'Brain'],
            'reduced_correct': 'A',
            'correct': 'C',
            'type': 'question'
        },
        {
            'question': 'Who discovered penicillin?',
            'options': ['Alexander Fleming', 'Marie Curie', 'Albert Einstein', 'Isaac Newton'],
            'reduced_options': ['Alexander Fleming', 'Albert Einstein'],
            'correct': 'A',
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'What is the capital city of Australia?',
            'options': ['Sydney', 'Canberra', 'Melbourne', 'Perth'],
            'correct': 'B',
            'reduced_correct': 'A',
            'reduced_options': ['Canberra', 'Perth'],
            'type': 'question'
        },
        {
            'question': 'Which country is famous for the Taj Mahal?',
            'options': ['India', 'China', 'Egypt', 'Italy'],
            'correct': 'A',
            'reduced_correct': 'A',
            'type': 'question',
            'reduced_options': ['India', 'Egypt'],
        },
        {
            'question': 'Who wrote the novel "1984"?',
            'options': ['George Orwell', 'J.R.R. Tolkien', 'Jane Austen', 'F. Scott Fitzgerald'],
            'correct': 'A',
            'reduced_correct': 'A',
            'reduced_options': ['George Orwell', 'Jane Austen'],
            'type': 'question'
        },
        {
            'question': 'What is the tallest mountain in the world?',
            'options': ['Mount Everest', 'K2', 'Kangchenjunga', 'Makalu'],
            'correct': 'A',
            'reduced_options': ['Mount Everest', 'Kangchenjunga'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Which planet is known as the "Red Planet"?',
            'options': ['Mars', 'Jupiter', 'Venus', 'Saturn'],
            'correct': 'A',
            'reduced_options': ['Mars', 'Venus'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Who is the author of the famous novel "Pride and Prejudice"?',
            'options': ['Jane Austen', 'Charles Dickens', 'Charlotte Brontë', 'Emily Brontë'],
            'correct': 'A',
            'reduced_options': ['Jane Austen', 'Charlotte Brontë'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Which country won the FIFA World Cup in 2018?',
            'options': ['France', 'Brazil', 'Germany', 'Argentina'],
            'correct': 'A',
            'reduced_options': ['France', 'Germany'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Who painted the famous artwork "The Starry Night"?',
            'options': ['Vincent van Gogh', 'Leonardo da Vinci', 'Pablo Picasso', 'Claude Monet'],
            'correct': 'A',
            'reduced_options': ['Vincent van Gogh', 'Pablo Picasso'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'What is the largest ocean in the world?',
            'options': ['Pacific Ocean', 'Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean'],
            'correct': 'A',
            'reduced_options': ['Pacific Ocean', 'Indian Ocean'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Which country is famous for the Great Wall?',
            'options': ['China', 'Japan', 'India', 'Italy'],
            'correct': 'A',
            'reduced_options': ['China', 'India'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Which scientist developed the theory of relativity?',
            'options': ['Albert Einstein', 'Isaac Newton', 'Galileo Galilei', 'Marie Curie'],
            'correct': 'A',
            'reduced_options': ['Albert Einstein', 'Galileo Galilei'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'What is the currency of Japan?',
            'options': ['Yen', 'Euro', 'Dollar', 'Pound'],
            'correct': 'A',
            'reduced_options': ['Yen', 'Dollar'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Who is the Greek god of thunder?',
            'options': ['Zeus', 'Poseidon', 'Hades', 'Apollo'],
            'correct': 'A',
            'reduced_options': ['Zeus', 'Hades'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Which country is famous for the Eiffel Tower?',
            'options': ['France', 'Spain', 'Italy', 'United Kingdom'],
            'correct': 'A',
            'reduced_options': ['France', 'Italy'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Who wrote the novel "To Kill a Mockingbird"?',
            'options': ['Harper Lee', 'J.D. Salinger', 'F. Scott Fitzgerald', 'Mark Twain'],
            'correct': 'A',
            'reduced_options': ['Harper Lee', 'F. Scott Fitzgerald'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'What is the chemical symbol for sodium?',
            'options': ['Na', 'Ca', 'Fe', 'K'],
            'correct': 'A',
            'reduced_options': ['Na', 'Fe'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Which planet is known as the "Blue Planet"?',
            'options': ['Earth', 'Mars', 'Venus', 'Neptune'],
            'correct': 'A',
            'reduced_options': ['Earth', 'Venus'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Who painted the famous artwork "The Last Supper"?',
            'options': ['Leonardo da Vinci', 'Vincent van Gogh', 'Pablo Picasso', 'Michelangelo'],
            'correct': 'A',
            'reduced_options': ['Leonardo da Vinci', 'Pablo Picasso'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'What is the capital city of Canada?',
            'options': ['Ottawa', 'Toronto', 'Vancouver', 'Montreal'],
            'correct': 'A',
            'reduced_options': ['Ottawa', 'Vancouver'],
            'reduced_correct': 'A',
            'type': 'question'
        },
        {
            'question': 'Who is the author of the famous play "Hamlet"?',
            'options': ['William Shakespeare', 'George Orwell', 'Jane Austen', 'Charles Dickens'],
            'correct': 'A',
            'reduced_options': ['William Shakespeare', 'Jane Austen'],
            'reduced_correct': 'A',
            'type': 'question'
        }

        ]
        self.questions['C'] = random.sample(level_c_questions, 15)


    #this function handles the answer and updates a new question!   
    def process_answer(self, player_id, answer):
        player = self.players[player_id]
        if str(answer).lower() == "correct":
            player['correct_answers'] += 1
            if player['stage'] == 'A':
                player['money'] += 5000
            elif player['stage'] == "C":
                player["board_step"] += 1
                

                # self.chaser_step += 1
        #else incorrect answer
        elif str(answer).lower() == "incorrect_c" and player['stage'] == 'C':
            #TODO - handle
            print("incorrect!")
            self.chaser_step += 1
            
        player['answered_count'] += 1

        # handle stage to stage!
        if player['answered_count'] == 3 and player['stage'] == 'A':
            if player['correct_answers'] > 0:
                #TODO - check if he was on stage A and if he was then send him the options of how much he wants to continue with - 2*current_amount or current_amount/2 or current
                self.move_player_forward(player_id)
                if self.players[player_id]['stage'] == 'B':
                    # WHEN THE PLAYER GETS TO PHASE B IM ASKING HIM IF HE WANTS TO DOUBLE OR CURRENT OR DIVIDED 
                    send_phaseB_message(game.players[player_id]['connection'],game.players[player_id]['money'])
            #meaning that he didnt answer any of the questions right
            else:
                player['stage'] = 'A'
                player['correct_answers'] = 0
        
        elif player['stage'] == 'C':
            # if the player was correct on phase C then we need to jump one step up
            if player['board_step'] == 7:
                print("player wins!!!!")
                message = "The player won the game!!!! good job! :)"
                response = {
                    "data" : {
                        "type" : "win_game",
                        "message" : message
                    }

                }
                print(response)
                json_object = json.dumps(response)
                player["connection"].send(json_object.encode()) 
            
            if player['board_step'] <= self.chaser_step: # here i check if the chaser reached the player
                print("player lost!!! chaser wins! :(")
                message = "player lost!!! chaser wins! :("
                response = {
                    "data" : {
                        "type" : "game_over",
                        "message" : message
                    }

                }
                print(response)
                json_object = json.dumps(response)
                player["connection"].send(json_object.encode())                
                
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

    
    def handle_sos(self, player_id):
        self.players[player_id]['lifeline'] = False


    def get_current_question(self, player_id):
        player = self.players[player_id]
        current_stage = player['stage']
        # current_question_index = self.get_stage_position(current_stage, player['answered_count']) - 1
        current_question_index = player['answered_count']
        if len(self.questions[current_stage]) > current_question_index:
            return self.questions[current_stage][current_question_index]
        else:
            return None

# this move 
def computer_move(options, correct_answer):
    # Randomly choose the correct answer 75% of the time
    if random.random() < 0.75:
        answer = correct_answer
    else:
        # Choose a random incorrect answer
        options.remove(correct_answer)
        answer = random.choice(options)
    return answer


def send_game_summary(sock):
    summary = "Game over!\n"
    summary += "Thank you for playing!"
    sock.send(summary.encode())


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
        "data": {
        "type" : "B",
        "message": "Congratz!",
        "current_amount": current_amount,
        "choices": [
            {"step": 2, "value": double},
            {"step": 3, "value": current_amount},
            {"step": 4, "value": divided}
        ]
        }
    }
    
    instructions_json = json.dumps(instructions)
    conn.send(instructions_json.encode())



def send_question(conn, question, player_id):
    if question is None:
        send_game_summary(conn)
    else:
        data = {}
        data['data'] = question
        data['lifeline'] = game.has_lifeline(player_id)
        data['stage'] = game.get_stage(player_id)
        data_json = json.dumps(data)
        conn.send(data_json.encode())

def handle_question_response(sock, game, player_id, response):
    if str(response) == 'sos':
        game.handle_sos(player_id)
        return
    game.process_answer(player_id, response.lower())

    next_question = None
    if game.get_stage(player_id) != "B":
        next_question = game.get_current_question(player_id)
        if game.chaser_step >= game.get_step(player_id) and game.get_stage(player_id) == "C":
            message = {
                "data" : {
                    "type" : "game_over",
                    "message" : "GAME OVER - CHASER WINS!"
                }
            }
            json_object = json.dumps(message)
            sock.send(json_object.encode())
    if game.get_stage(player_id) == "C":
        print(game.get_board_info(player_id))

    if next_question:
        
        send_question(sock, next_question, player_id)
    elif game.get_stage(player_id) == "B":
        print("")



def handle_initial_response(sock, game, player_id, response):
    if response.lower() == 'yes':
        # Player wants to play, generate questions and send Level A question
        game.generate_questions()
        send_question(sock, game.get_current_question(player_id), player_id)
    else:
        # Player does not want to play, end the connection
        sock.send("Thank you for playing!".encode())
        sel.unregister(sock)
        sock.close()
        game.remove_player(player_id)


def handle_phase_B_response(sock,game,player_id,board_step):
    # updating the step of the player in the board
    game.update_step_player(player_id, board_step)
    # updating money of the player in the board
    if board_step == '2':
        game.update_money(player_id, game.get_money(player_id) * 2) #TODO
    elif board_step == '4':
        game.update_money(player_id, game.get_money(player_id) / 2) #TODO
    
    game.move_player_forward(player_id)
    # move to phase C #TODO
    handle_question_response(sock,game,player_id,board_step)



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
                elif message.lower() == '2' or message.lower() == '3' or message.lower() == '4':
                    handle_phase_B_response(sock, game , player_id , message)
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
                if len(game.players) < 3:
                    accept_wrapper(key.fileobj, game)
                else:
                    sock, addr = lsock.accept()
                    data = {
                        "data" : {
                            "type" : "reject",
                            "message" : f"Rejected connection from {addr}\nConnection limit reached. Please try again later."
                        }
                    }
                    reject_object = json.dumps(data)
                    sock.send(reject_object.encode())
                    sock.close()

            else:
                service_connection(key, mask, game)

except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()

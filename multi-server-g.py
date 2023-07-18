import json
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

    def add_player(self, player_id, connection):
        self.players[player_id] = {
            'stage': 'A',
            'money': 0,
            'answered_count': 0,
            'lifeline': True,
            'connection': connection,
            'correct_answers': 0,
            'board_step': 1
        }

    def remove_player(self, player_id):
        del self.players[player_id]

    def generate_questions(self):
        level_a_questions = [
            {
                'id': 1,
                'question': 'Who painted the Mona Lisa?',
                'options': ['Leonardo da Vinci', 'Vincent van Gogh', 'Pablo Picasso', 'Michelangelo'],
                'correct': 'A',
                'type': 'question'
            },
            {
                'id': 2,
                'question': 'Which planet is known as the "Red Planet"?',
                'options': ['Mars', 'Jupiter', 'Venus', 'Saturn'],
                'correct': 'A',
                'type': 'question'
            },
            {
                'id': 3,
                'question': 'Who is the author of the famous novel "To Kill a Mockingbird"?',
                'options': ['J.D. Salinger', 'Harper Lee', 'F. Scott Fitzgerald', 'Ernest Hemingway'],
                'correct': 'B',
                'type': 'question'
            }
        ]
        self.questions['A'] = random.sample(level_a_questions, 3)

        level_b_questions = [
            {
                'id': 1,
                'question': 'What is the capital city of Australia?',
                'options': ['Sydney', 'Canberra', 'Melbourne', 'Perth'],
                'correct': 'B',
                'reduced_options': ['Canberra', 'Perth'],
                'type': 'question'
            },
            {
                'id': 2,
                'question': 'Which country is famous for the Taj Mahal?',
                'options': ['India', 'China', 'Egypt', 'Italy'],
                'correct': 'A',
                'type': 'question',
                'reduced_options': ['India', 'Egypt'],
            },
            {
                'id': 3,
                'question': 'Who wrote the novel "1984"?',
                'options': ['George Orwell', 'J.R.R. Tolkien', 'Jane Austen', 'F. Scott Fitzgerald'],
                'correct': 'A',
                'reduced_options': ['George Orwell', 'Jane Austen'],
                'type': 'question'
            }
        ]
        self.questions['B'] = random.sample(level_b_questions, 3)

        level_c_questions = [
            {
                'id': 1,
                'question': 'Who wrote the play "Romeo and Juliet"?',
                'options': ['William Shakespeare', 'Charles Dickens', 'Jane Austen', 'F. Scott Fitzgerald'],
                'correct': 'A',
                'reduced_options': ['William Shakespeare', 'Jane Austen'],
                'reduced_correct': 'A',
                'type': 'question'
            },
            {
                'id': 2,
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
                'id': 3,
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
            }
        ]
        self.questions['C'] = random.sample(level_c_questions, 3)

        level_c_plus_questions = [
            {
                'question': 'What is the chemical symbol for gold?',
                'options': ['Au', 'Ag', 'Fe', 'Hg'],
                'correct': 'A',
                'type': 'question'
            },
            {
                'question': 'Who discovered penicillin?',
                'options': ['Alexander Fleming', 'Marie Curie', 'Albert Einstein', 'Isaac Newton'],
                'correct': 'A',
                'type': 'question'
            }
        ]
        self.questions['C+'] = random.sample(level_c_plus_questions, 2)

    def process_answer(self, player_id, answer):
        player = self.players[player_id]
        stage = player['stage']

        if answer.lower() == "correct_a":
            player['correct_answers'] += 1
            if stage == 'A':
                player['money'] += 5000
            elif stage == "C":
                player['board_step'] += 1
                self.chaser_step += 1
        elif answer.lower() == "sos":
            self.turn_off_lifeline(player_id)
            return
        elif answer.lower() == "incorrect_c" and stage == 'C':
            self.chaser_step += 1

        player['answered_count'] += 1

        if player['answered_count'] == 3 and stage == 'A':
            if player['correct_answers'] > 0:
                self.move_player_forward(player_id)
                if player['stage'] == 'B':
                    send_phase_b_message(player['connection'], player['money'])
            else:
                player['stage'] = 'A'
                player['correct_answers'] = 0
        elif stage == 'C':
            if player['board_step'] == 7:
                print("Player wins!")
            if player['board_step'] == self.chaser_step:
                print("Player lost! Chaser wins!")
                message = {
                    "data": {
                        "type": "game_over",
                        "message": "Player lost! Chaser wins!"
                    }
                }
                json_object = json.dumps(message)
                player["connection"].sendall(json_object.encode())

    def move_player_forward(self, player_id):
        player = self.players[player_id]
        player['answered_count'] = 0
        player['correct_answers'] = 0
        current_stage = player['stage']
        next_stage = self.get_next_stage(current_stage)
        player['stage'] = next_stage

    def get_next_stage(self, current_stage):
        if current_stage == 'A':
            return 'B'
        elif current_stage == 'B':
            return 'C'
        elif current_stage == 'C':
            return 'C+'

    def turn_off_lifeline(self, player_id):
        self.players[player_id]['lifeline'] = False


def send_game_summary(sock):
    summary = "Game over!\n"
    summary += "Thank you for playing!"
    sock.sendall(summary.encode())


def accept_wrapper(sock, game):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    player_id = addr[1]
    game.add_player(player_id, conn)


def send_phase_b_message(conn, current_amount):
    divided = current_amount / 2
    double = current_amount * 2

    message = {
        "data": {
            "type": "B",
            "message": "Congratulations!",
            "current_amount": current_amount,
            "choices": [
                {"step": 2, "value": double},
                {"step": 3, "value": current_amount},
                {"step": 4, "value": divided}
            ]
        }
    }

    json_object = json.dumps(message)
    conn.sendall(json_object.encode())


def send_question(conn, question):
    if question is None:
        send_game_summary(conn)
    else:
        data = {
            "data": question,
            "lifeline": game.players[player_id]['lifeline'],
            "stage": game.players[player_id]['stage']
        }
        data_json = json.dumps(data)
        conn.sendall(data_json.encode())


def handle_question_response(sock, game, player_id, response):
    game.process_answer(player_id, response.lower())
    next_question = game.get_current_question(player_id)
    if next_question:
        send_question(sock, next_question)
    else:
        print("Game over")


def handle_initial_response(sock, game, player_id, response):
    if response.lower() == 'yes':
        game.generate_questions()
        send_question(sock, game.get_current_question(player_id))
    else:
        sock.sendall("Thank you for playing!".encode())
        sel.unregister(sock)
        sock.close()
        game.remove_player(player_id)


def handle_phase_b_response(sock, game, player_id, board_step):
    game.update_step_player(player_id, board_step)
    if board_step == '2':
        game.update_money(player_id, game.get_money(player_id) * 2)
    elif board_step == '4':
        game.update_money(player_id, game.get_money(player_id) / 2)
    game.move_player_forward(player_id)
    handle_question_response(sock, game, player_id, board_step)


def service_connection(key, mask, game):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            message = recv_data.decode().strip()
            player_id = data.addr[1]
            if player_id in game.players:
                if message.lower() == 'yes':
                    handle_initial_response(sock, game, player_id, message)
                elif game.players[player_id]['stage'] == 'C+':
                    handle_game_over_response(sock, game, player_id, message)
                elif message.lower() == '2' or message.lower() == '3' or message.lower() == '4':
                    handle_phase_b_response(sock, game, player_id, message)
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

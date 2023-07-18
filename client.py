import json
import socket

def main():
    host = "127.0.0.1"
    port = 65432
    print("Welcome to chaser game!\n")
    yes_or_no = input("Would u like to play?")
    if yes_or_no == "yes":
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall("yes".encode())
            while True:
                # recieved data json
                response = sock.recv(1024).decode()
                # Deserialize the JSON string back into a hashmap
                received_data_dict = json.loads(response)
                if received_data_dict['type'] == 'question':
                    question_text = received_data_dict['question']
                    options = received_data_dict['options']
                    question_text += "\n"
                    for i, option in enumerate(options):
                        question_text += f"{chr(ord('A')+i)}) {option}\n"
                    print(question_text)
                    answer = input("Enter your answer:")
                    if answer.lower() == received_data_dict['correct'].lower():
                        sock.sendall("correct".encode())
                        print("Correct!")
                elif received_data_dict['type'] == 'B':
                    # Access the individual fields based on their keys
                    message = received_data_dict["message"]
                    type = received_data_dict["type"]
                    current_amount = received_data_dict["current_amount"]
                    choices = received_data_dict["choices"]

                    # Print the extracted values
                    print("Message:", message)
                    print("Type:", type)
                    print("Current Amount:", current_amount)
                    print("Choices:")
                    for choice in choices:
                        print("Step:", choice["step"])
                        print("Value:", choice["value"])
                    choice = input("Enter your choice (2/3/4): ")
                    if choice == '2' or choice == '3' or choice == '4':
                        sock.sendall(choice.encode())
                    else:
                        print("u didnt enter choice")




                elif received_data_dict['type'] == "game over":
                    break
    else:
        print("\nWe hope to see u playing with us!")
if __name__ == "__main__":
    main()
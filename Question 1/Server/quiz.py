import json
import tincanchat

NO_INPUT = "!!!NO_INPUT!!!"
END_OF_QUIZ = "!!!END!!!"
def start(client_socket):

    try:
        # Result variable to store user's name, answers and final mark
        results = {}
        final_mark = 0

        # Opening the json file
        file = open("quiz.json")
        quiz = json.load(file)

        message = "Enter your name: "
        tincanchat.send_msg(client_socket, message)
        print("sent a message from server")
        user_name = tincanchat.recv_msg(client_socket)
        print("User name: "+user_name)

        # First value is user's name
        results["Name"] = user_name

        # There's only two values a user can enter: t for true, f for false
        instructions = "Answer \"t\" for True and \"f\" for False"
        tincanchat.send_msg(client_socket, "!!!NO_INPUT!!!"+instructions)

        j = 1
        # For loop for items in json file(quiz)
        for item in quiz:

            # Answer enter by user
            tincanchat.send_msg(client_socket, item)
            answer = tincanchat.recv_msg(client_socket)
            # Correct answer from json file, which is first element of list
            correct_answer = quiz[item][0]

            # If user entered a value that's not t or f, show a warning
            if not answer.__eq__("t") and not answer.__eq__("f"):

                instructions = "please answer with \"t\" for True, and \"f\" for False"
                tincanchat.send_msg(client_socket, NO_INPUT+instructions)
                tincanchat.send_msg(client_socket, item)

                answer = tincanchat.recv_msg(client_socket)

            # If user answered correctly, increase the mark
            if answer.__eq__(correct_answer):
                tincanchat.send_msg(client_socket, NO_INPUT+"Correct")
                final_mark += 5
                answer = "correct"

            # If user answered incorrectly, don't change the mark, and output the right answer
            else:
                reply = ""

                if correct_answer.__eq__("f"):
                    reply = "Wrong, correct answer is: " + quiz[item][1]
                elif correct_answer.__eq__("t"):
                    reply = "Wrong, correct answer is true"

                tincanchat.send_msg(client_socket, NO_INPUT+reply)

                answer = "Wrong"

            # Add that user answer correctly or incorrectly to question X in results
            results["Question" + str(j)] = answer
            j += 1

        results["Result"] = final_mark

        reply = "Thanks for taking the test, your result is: " + str(final_mark) + "/100"
        tincanchat.send_msg(client_socket, END_OF_QUIZ + reply)

        # write results variable to a json file
        with open(user_name+"_results.json", "w") as write_file:
            json.dump(results, write_file)

        json.dumps(results)

    except (ConnectionError, BrokenPipeError):
        print("socket error from quiz.py")

    finally:
        print('closed connection')

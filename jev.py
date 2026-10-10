import requests
import json


def init():
    print('\nInitialising AI model...')
    ask(
        "Jeff walked up the poor staircase.",
        500,
        "What did Jeff do?",
        [
            "Not in story",
            "Walked up the perfect staircase.",
            "Walked down the perfect stair case.",
            "Walked up the terrible staircase.",
            "walked down the terrible staircase."
        ]
    )
    print('Initialised!')


def ask(text, words, question, answers):
    options = {}
    backup = {}
    i = 0
    for answer in answers:
        if i > len(answers)/2 and words >= 1300:
            backup[str(i)] = answer
        else:
            options[str(i)] = answer
        i += 1

    json = {
        "model": "tev1:4b",
        "state": text,
        "think": False,
        "questions": {
            question: {
                "type": "choice",
                "instructions": "What true, must be fully otherwise ",
                "criteria": options
            },
        }
    }

    print('\nJson Data:', repr(json))

    i = 0
    while True:

        response = requests.post(
            "http://localhost:11434/v1/systemone",
            json=json
        )

        print("Status:", response.status_code)
        print("Response:", response.text)

        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()

            choice = data["answers"][question]["choice"]
            prob = data['answers'][question]['probabilities'][choice]

            if prob >= 0.8:
                answer = answers[int(choice)]
            else:
                print('Not sure!')
                if len(backup) > 0:
                    print('Going through backup list!')
                    answer = ask(
                        text,
                        0,
                        question,
                        backup.values()
                    )
                else:
                    answer = 'Not in story'

            print('Answer:', choice, answer)

            return answer
        else:
            if i == 0:
                i += 1
            else:
                return answers[0]


if __name__ == "__main__":
    print(ask(
        "Jeff walked up the poor staircase.",
        500,
        "What did Jeff do?",
        [
            "Walked up the perfect staircase.",
            "Walked down the perfect stair case.",
            "walked down the terrible staircase."
        ],
    ))

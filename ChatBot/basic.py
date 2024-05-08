import json
from difflib import get_close_matches


def load_knoladege_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)  # noqa

    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chat_bot(path_to_knowledge: str):
    knowledge_base: dict = load_knoladege_base(path_to_knowledge)

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "quit" or user_input.lower() == "exit":
            break

        questions = [q["question"] for q in knowledge_base["questions"]]
        best_match: str | None = find_best_match(user_input, questions)

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer, Can you teach me?\n')
            new_answer: str = input('Type the answer or "skip" to skip or "exit" to exit: ') # noqa

            if new_answer.lower() == "exit":
                break
            elif new_answer.lower() != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer}) # noqa
                save_knowledge_base(path_to_knowledge, knowledge_base)
                print('Bot: Thank you! I learned a new response!')


def main() -> None:
    chat_bot('ChatBot/knowledge_base.json')


if __name__ == '__main__':
    main()

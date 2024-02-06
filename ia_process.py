import llm


class IAProcess:
    def __init__(self):
        self.default_model = "mistral-7b-openorca"

        return

    def query(self, text: str, model: str) -> str:
        """Process the question text and returns the answer from the IA prompt

        :param text: str
        :param model: str
        :return: str
        """
        print("IA NOW PROCESSING...")
        if model == "":
            model = llm.get_model(self.default_model)
        else:
            model = llm.get_model(model)

        response = model.prompt(text)

        answer = "IA ANSWER:\n"
        answer += str(response)

        return answer


if __name__ == "__main__":
    ia = IAProcess()

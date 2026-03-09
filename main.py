from wrapper.wrapper import LangGraphWrapper

rag = LangGraphWrapper("config/config.json")
pdf = input("enter pdf path: ").strip().replace('"','')
rag.load_pdf(pdf)
print("pdf loaded, ask ur question (type exit to quit):")

while True:
    question = input("question:")
    if question.lower() == "exit":
        break
    answer = rag.ask(question)
    print(answer)
    print("\n")
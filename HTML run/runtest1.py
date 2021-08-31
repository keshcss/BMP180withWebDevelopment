from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
app = Flask(__name__)
bot = ChatBot("Guide")

trainer = ListTrainer(bot)
trainer.train(['What is your name?', 'My name is Guide'])
trainer.train(['How are you?', 'I am good' ])
trainer.train(['Bye?', 'Bye, see you later' ])

conversation = [
    "Hello",
    "Hello!!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

trainer.train(conversation)

corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english')

@app.route("/get/")
def get_bot_response():    
    userText = request.args.get('msg')    
    return str(bot.get_response(userText)) 

if __name__ == '__main__':
   app.run(debug = False)

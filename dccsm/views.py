from flask import Blueprint, render_template, redirect
from .models import *



views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    # try:
        nodes = Node.query.all()
        directory = Directory.query.all()
        messages = MessageSimulation.query.order_by(MessageSimulation.id.desc()).all()
        blocks = MemoryBloc.query.all()

        all_nodes =  nodes
        directory = 'directory'
        messages = 'messages'
        blocks = 'blocks'
        for node in all_nodes:
            print(node.id)
    
        # context = {
        #     'nodes': nodes,
        #     'directory': directory,
        #     'messages': messages,
        #     'blocks': blocks,
        # }
        return render_template('index.html', all_nodes=all_nodes, directory=directory, messages=messages, blocks=blocks)
    # except Exception as e:
    #     return f"<h2>Error page ==> {e}</h2>"


# Generateur de message
def message_sender(type_message: str, source: str, dest: str, content_msg: str):
    MessageSimulation(type_message=type_message, source=source, destination=dest, content_msg=content_msg).save()


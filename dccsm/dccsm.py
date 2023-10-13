from flask import Blueprint, render_template, redirect, request, url_for
from .models import *

dccsm = Blueprint('dccsm', __name__)

@dccsm.route('/reset')
def reinitialisation_data():
    # try:
        Directory.query.delete()
        MessageSimulation.query.delete()
        MemoryBloc.query.delete()
        Node.query.delete()
        
        node1 = Node(name='Home', numero=0)
        node2 = Node(name='Local', numero=1)
        node3 = Node(name='Remote', numero=2)
      
        db.session.add(node1)
        db.session.add(node2)
        db.session.add(node3)
        

        block_0 = MemoryBloc(block_num=0, data='D0')
        block_1 = MemoryBloc(block_num=1, data='D1')
        block_2 = MemoryBloc(block_num=2, data='D2')
        block_3 = MemoryBloc(block_num=3, data='D3')

        db.session.add(block_0)
        db.session.add(block_1)
        db.session.add(block_2)
        db.session.add(block_3)

        dir1 = Directory(bloc=block_0, state='1', owner_bits='---')
        dir2 = Directory(bloc=block_1, state='1', owner_bits='---')
        dir3 = Directory(bloc=block_2, state='1', owner_bits='---')
        dir4 = Directory(bloc=block_3, state='1', owner_bits='---')

        db.session.add(dir1)
        db.session.add(dir2)
        db.session.add(dir3)
        db.session.add(dir4)

        db.session.commit()

        return redirect(url_for('views.home'))

    # except Exception as e:
    #     return f"<h2>Error page ==> {e}</h2>"


# def save_node(name: str, numero: int) -> bool:
#     try:
#         node = Node(name=name, numero=numero)
#         db.session.add(node)
#         db.session.commit()
#         return True
#     except:
#         return False
from flask import Blueprint, render_template, redirect, request, url_for
from .models import *

dccsm = Blueprint('dccsm', __name__)

def message_sender(type_message: str, source: str, dest: str, content_msg: str):
    similation_message = MessageSimulation(type_message=type_message, source=source, destination=dest, content_msg=content_msg)
    db.session.add(similation_message)
    db.session.commit()



def owner_bits(bits_list: list):
    if len(bits_list) >= 3:
        return '111'
    elif len(bits_list) == 2:
        if ['Local', 'Home'] == bits_list:
            return '110'
        if ['Local', 'Remote'] == bits_list:
            return '101'
        else:
            return '011'
    elif len(bits_list) == 1:
        if 'Local' in bits_list:
            return '100'
        if 'Home' in bits_list:
            return '010'
        else:
            return '001'
    else:
        return '000'


@dccsm.route('/read_data', methods=['POST'])
def read_data():
    try:
        if request.method == 'POST':            
            node_id = request.form.get('node')
            block_id = request.form.get('block')

            node = Node.query.get(node_id)
            block = Directory.query.get(block_id)

            if block.state != '3':
                caches_node = CacheNode.query.filter_by(node=node).filter_by(bloc=block.bloc).all()
                if caches_node:
                    cache_node = caches_node[-1]
                    if cache_node.state_cache != '2': 
                        cache_node.state_cache = '2' 
                        db.session.add(cache_node)
                        db.session.commit()
                else:
                    cache_node = CacheNode(node=node, bloc=block.bloc, state_cache='2')
                    db.session.add(cache_node)
                    db.session.commit()

                    node_home = Node.query.filter_by(numero=0).first()
                    MessageSimulation.query.delete()
                    message_sender(
                        'Read Miss',
                        f"Cache {node.name}",
                        f"Repertoire {node_home.name}",
                        f"{node.node_string}, {block.string_block}",
                    )
                    message_sender(
                        'Data Value Reply',
                        f"Repertoire {node_home.name}",
                        f"Cache {node.name}",
                        content_msg=f"{block.bloc.data}",
                    )
            else:
                caches_all = CacheNode.query.filter_by(state_cache='3') 
                cache_owner = None
                if caches_all:
                    cache_owner = caches_all[-1]

                caches_node = CacheNode.query.filter_by(node=node).filter_by(bloc=block.bloc).all()
                if caches_node:
                    cache_node = caches_node[-1]
                    if cache_node.state_cache != '2': 
                        cache_node.state_cache = '2' 
                        db.session.add(cache_node)
                        db.session.commit()

                    node_home = Node.query.filter_by(numero=0).first()
                    if cache_owner is not None:
                        MessageSimulation.query.delete()
                        message_sender(
                            'Fetch',
                            f"Repertoire {node_home.name}",
                            f"Cache {cache_owner.node.name}",
                            f"{block.string_block}",
                        )
                        message_sender(
                            'Data Write-Back',
                            f"Cache {cache_owner.node.name}",
                            f"Repertoire {node_home.name}",
                            f"{block.string_block}",
                        )
                        message_sender(
                            'Data Value Reply',
                            f"Repertoire {node_home.name}",
                            f"Cache {node.name}",
                            f"{block.string_block}",
                        )

                else:
                    cache_node = CacheNode(node=node, bloc=block.bloc, state_cache='2')
                    db.session.add(cache_node)
                    db.session.commit()

                    node_home = Node.query.filter_by(numero=0).first()
                    if cache_owner is not None:
                        MessageSimulation.query.delete()
                        message_sender(
                            'Fetch',
                            f"Repertoire {node_home.name}",
                            f"Cache {cache_owner.node.name}",
                            f"{block.string_block}",
                        )
                        message_sender(
                            'Data Write-Back',
                            f"Cache {cache_owner.node.name}",
                            f"Repertoire {node_home.name}",
                            f"{block.string_block}",
                        )
                        message_sender(
                            'Data Value Reply',
                            f"Repertoire {node_home.name}",
                            f"Cache {node.name}",
                            f"{block.string_block}",
                        )
            
            caches = CacheNode.query.filter_by(bloc=block.bloc).all()
            bits_list = []
            if caches:
                for c in caches:
                    bits_list.append(c.node.name)

                block.state = '2' 
                block.owner_bits = owner_bits(bits_list)
                db.session.add(block)
                db.session.commit()

            return redirect(url_for('views.home'))
        
    except Exception as e:
        return f"<h2>Error page ==> {e}</h2>"
    

@dccsm.route('/write_data', methods=['POST'])
def write_data():
    try:
        if request.method == 'POST':
            node_id = request.form.get('node')
            block_id = request.form.get('block')

            data = request.form.get('data')

            print("-----------------------------------------------")
            print(data)

            if data != '':
                node = Node.query.get(node_id)
                block = Directory.query.get(block_id)

                block_memory = MemoryBloc.query.get(block.id)
                block_memory.data = data
                db.session.add(block_memory)
                db.session.commit()

                node_home = Node.query.filter_by(numero=0).first()

                if block.state == '1':
                    MessageSimulation.query.delete()
                    message_sender(
                        'Write Miss',
                        f"Cache {node.name}",
                        f"Repertoire {node_home.name}",
                        f"{node.node_string}, {block.string_block}",
                    )
                    message_sender(
                        'Data Value Reply',
                        f"Repertoire {node_home.name}",
                        f"Cache {node.name}",
                        f"{block.string_block}",
                    )
                    cache_node = CacheNode(node=node, bloc=block.bloc, state_cache='3')
                    db.session.add(cache_node)
                    db.session.commit()

                    if node.name == 'Home':
                        bit_shared = '100'
                    elif node.name == 'Local':
                        bit_shared = '010'
                    elif node.name == 'Remote':
                        bit_shared = '001'
                    
                    block.state = '3' 
                    block.owner_bits = bit_shared
                    db.session.add(block)
                    db.session.commit()

                elif block.state == '2': 
                    MessageSimulation.query.delete()
                    message_sender(
                        'Data Value Reply',
                        f"Repertoire {node_home.name}",
                        f"Cache {node.name}",
                        f"{block.bloc.data}",
                    )

                    block_in_chached = CacheNode.query.filter_by(bloc=block_memory).all()
                    if block_in_chached:
                        for block_cache in block_in_chached:
                            message_sender(
                                'Invalidate',
                                f"Repertoire {node_home.name}",
                                f"Cache {block_cache.node.name}",
                                f"{block.string_block}",
                            )
                            block_cache.state_cache = '4' 
                            db.session.add(block_cache)
                            db.session.commit()
                            
                    
                    proprio = CacheNode.query.filter_by(bloc=block_memory).filter_by(node=node).all()
                    if proprio:
                        cached = proprio[-1]
                        cached.state_cache = '3'
                        db.session.add(cached)
                        db.session.commit()

                    else:
                        cache_node = CacheNode(node=node, bloc=block.bloc, state_cache='3')
                        db.session.add(cache_node)
                        db.session.commit()

                    if node.name == 'Home':
                        bit_shared = '100'
                    elif node.name == 'Local':
                        bit_shared = '010'
                    elif node.name == 'Remote':
                        bit_shared = '001'
                    block.state = '3'
                    block.owner_bits = bit_shared
                    db.session.add(block)
                    db.session.commit()

                elif block.state == '3':
                    MessageSimulation.query.delete()
                    message_sender(
                        'Write Miss',
                        f"Cache {node.name}",
                        f"Repertoire {node_home.name}",
                        f"{node.node_string}, {block.string_block}",
                    )

                    cache_modified = CacheNode.query.filter_by(bloc=block_memory).filter_by(state_cache='3').all()
                    if cache_modified:
                        modif_cache = cache_modified[-1]
                        modif_cache.state_cache = '4'
                        db.session.add(modif_cache)
                        db.session.commit()


                    message_sender(
                        'Fetch/Invalidate',
                        f"Repertoire {node_home.name}",
                        f"Cache {node.name}",
                        f"{node.node_string}",
                    )
                    message_sender(
                        'Data Write-Back',
                        f"Cache {node.name}",
                        f"Repertoire {node_home.name}",
                        f"{node.node_string}, {block.string_block}",
                    )
                    message_sender(
                        'Data Value Reply',
                        f"Repertoire {node_home.name}",
                        f"Cache {node.name}",
                        f"{node.node_string}, {block.string_block}",
                    )
                    
                    proprio = CacheNode.query.filter_by(bloc=block_memory).filter_by(node=node).all()
                    if proprio:
                        cached = proprio[-1]
                        cached.state_cache = '3'
                        db.session.add(cached)
                        db.session.commit()

                    else:
                        cache_node = CacheNode(node=node, bloc=block.bloc, state_cache='3')
                        db.session.add(cache_node)
                        db.session.commit()

                    if node.name == 'Home':
                        bit_shared = '100'
                    elif node.name == 'Local':
                        bit_shared = '010'
                    elif node.name == 'Remote':
                        bit_shared = '001'
                    block.state = '3'
                    block.owner_bits = bit_shared
                    db.session.add(block)
                    db.session.commit()
                    

        return redirect(url_for('views.home'))
        
    except Exception as e:
        return f"<h2>Error page ==> {e}</h2>"









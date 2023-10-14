from . import db


node_choice = (
    ('Home', 'Home'),
    ('Local', 'Local'),
    ('Remote', 'Remote'),
)

state_block = (
    ('1', 'Uncached'),
    ('2', 'Shared'),
    ('3', 'Modified'),
    ('4', 'Invalid'),
)

msg_type_choice = (
    ('1', "Read Miss"),
    ('2', "Write Miss"),
    ('3', "Data Value Reply"),
    ('4', "Invalidate"),
    ('5', "Fetch"),
    ('6', "Fetch/Invalidate"),
    ('7', "Data Write-Back"),
)

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, default='Home')
    numero = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Node {self.numero} - {self.name}"
    
    @property
    def node_string(self):
        return f"Node {self.numero}"
    
    @property
    def all_caches(self):
        return CacheNode.query.filter_by(node=self).order_by(CacheNode.id.desc()).all()
    

    
class MemoryBloc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block_num = db.Column(db.Integer, nullable=False)
    data = db.Column(db.String(20), nullable=False, default='--')
    directory_rel = db.relationship('Directory', backref=db.backref('bloc_rel', uselist=False), uselist=False)

    def __repr__(self) -> str:
        return f"B{self.block_num}"
    
    @property
    def string_block(self) -> str:
        return f"B{self.block_num}"
    
class Directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bloc_id = db.Column(db.Integer, db.ForeignKey('memory_bloc.id'), nullable=False)
    state = db.Column(db.String(30), default='1')
    owner_bits = db.Column(db.String(5))

    bloc = db.relationship('MemoryBloc', backref=db.backref('directory', uselist=False))

    def __repr__(self) -> str:
        return str(self.bloc)
    
    @property
    def string_block(self) -> str:
        return f"B{self.bloc.block_num}"
    
    @property
    def state_directory(self):
        state = self.state
        if state == '1':
            return 'Uncached'
        elif state == '2':
            return 'Shared'
        elif state == '3':
            return 'Modified'
        elif state == '4':
            return 'Invalid'
        else:
            return state
    
class CacheNode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'), nullable=False)
    bloc_id = db.Column(db.Integer, db.ForeignKey('memory_bloc.id'), nullable=False)
    state_cache = db.Column(db.String(20))

    node = db.relationship('Node', backref=db.backref('caches'))
    bloc = db.relationship('MemoryBloc', backref=db.backref('caches'))
    

    def __repr__(self) -> str:
        return f"{self.node.name} B{self.bloc.block_num}"
    
    @property
    def state_cache_state(self):
        state = self.state_cache
        if state == '2':
            return 'Shared'
        elif state == '3':
            return 'Modified'
        elif state == '4':
            return 'Invalid'
        else:
            return state
    
class MessageSimulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_message = db.Column(db.String(30), nullable=False)
    source = db.Column(db.String(30), nullable=False)
    destination = db.Column(db.String(30), nullable=False)
    content_msg = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return self.type_message
    
    @property
    def message(self):
        index = int(self.type_message)
        index -= 1
        return msg_type_choice[index][1]


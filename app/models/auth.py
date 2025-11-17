from flask_login import UserMixin
from app.models import db, bcrypt, login_manager

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    
    # User authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # User fields
    name = db.Column(db.String(100), nullable=False, server_default='')
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.TIMESTAMP, nullable=True)
    updated_at = db.Column(db.TIMESTAMP, nullable=True)
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def set_password(self, plain_txt_password):
        self.password_hash = bcrypt.generate_password_hash(plain_txt_password).decode(
            "utf-8"
        )

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE')))
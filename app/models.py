from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Your model definitions go here


class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    powers = db.relationship('Power', secondary='hero_powers', backref='heroes')

    def __repr__(self):
        return f'<Hero id={self.id}, name={self.name}, super_name={self.super_name}>'

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Power id={self.id}, name={self.name}, description={self.description}>'

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description.strip()) < 20:
            raise ValueError('Description must be at least 20 characters long')
        return description

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String(20), nullable=False)

    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError('Strength must be one of: Strong, Weak, Average')
        return strength
    
    def __repr__(self):
        return f'<HeroPower id={self.id}, hero_id={self.hero_id}, power_id={self.power_id}, strength={self.strength}>'

#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if 'description' in data:
            description = data['description']
            power.description = description
            try:
                db.session.commit()
                return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'Missing description field'}), 400
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    required_fields = ['strength', 'power_id', 'hero_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields (strength, power_id, hero_id)'}), 400

    strength = data['strength']
    power_id = data['power_id']
    hero_id = data['hero_id']
    
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    valid_strengths = ['Strong', 'Weak', 'Average']
    if strength not in valid_strengths:
        return jsonify({'error': 'Strength must be one of: Strong, Weak, Average'}), 400

    hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
    db.session.add(hero_power)

    try:
        db.session.commit()

        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
        }
        return jsonify(hero_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5555)

from flask import Blueprint
import json
from roadmaps.basic_skills import create_basic_skills

map_bp = Blueprint('roadmaps', __name__)


@map_bp.route('/basic-skills')
def basic_skills():
    create_basic_skills()
    with open('roadmaps/basic_skills.json', 'r') as openfile:
        basic_skills_map = json.load(openfile)
        return basic_skills_map


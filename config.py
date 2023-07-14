import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:08164462713@localhost:5432/nigeruni'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:aA#atinigerdb@atinigerdb.co5demze0mjs.eu-north-1.rds.amazonaws.com:5432/database_atiniger'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
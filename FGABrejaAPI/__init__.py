from flask import Flask


app = Flask(__name__)

from FGABrejaAPI import views, routes, tests

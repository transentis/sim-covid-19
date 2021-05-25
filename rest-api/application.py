from flask import Flask, redirect, url_for, request, make_response, jsonify

from BPTK_Py.server import BptkServer

from model import bptk

# Calling the BptkServer class
application = BptkServer(__name__, bptk) 

if __name__ == "__main__":
    application.run()
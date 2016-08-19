'''
Created on 22.07.2016

@author: Jonas
'''
from flask import Blueprint
from flask.globals import request, session
from son.editor.app.constants import get_parent, Category
from son.editor.app.exceptions import NameConflict, NotFound
from son.editor.app.util import prepareResponse, getJSON
from son.editor.vnfs import functionsimpl

vnfs_api = Blueprint("vnfs_api", __name__)


@vnfs_api.route('/<parentID>/functions/', methods=['GET'])
def get_vnfs(wsID, parentID):
    if get_parent(request) is Category.project:
        functions = functionsimpl.get_functions(session["userData"], wsID, parentID)
        return prepareResponse({"functions": functions})
    return prepareResponse("not yet implemented")


@vnfs_api.route('/<parentID>/functions/', methods=['POST'])
def create_vnf(wsID, parentID):
    try:
        if get_parent(request) is Category.project:
            vnf_data = getJSON(request)
            vnf_data = functionsimpl.create_function(session['userData'], wsID, parentID, vnf_data)
            return prepareResponse({"created": vnf_data}), 201
        # TODO implement for catalog and platform
        return prepareResponse("not implemented yet")
    except NameConflict as err:
        return prepareResponse(err.msg), 409
    except NotFound as err:
        return prepareResponse(err.msg), 404


@vnfs_api.route('/<parentID>/functions/<vnf_id>', methods=['PUT'])
def update_vnf(wsID, parentID, vnf_id):
    try:
        if get_parent(request) is Category.project:
            vnf_data = getJSON(request)
            vnf_data = functionsimpl.update_function(session['userData'], wsID, parentID, vnf_id, vnf_data)
            return prepareResponse(vnf_data)
        return prepareResponse("update vnf in project with id " + parentID)
    except NameConflict as err:
        return prepareResponse(err.msg), 409
    except NotFound as err:
        return prepareResponse(err.msg), 404


@vnfs_api.route('/<parentID>/functions/<vnfID>', methods=['DELETE'])
def delete_vnf(wsID, parentID, vnfID):
    try:
        deleted = functionsimpl.delete_function(session['userData'], wsID, parentID, vnfID)
        return prepareResponse({"deleted": deleted})
    except NotFound as err:
        return prepareResponse(err.msg), 404

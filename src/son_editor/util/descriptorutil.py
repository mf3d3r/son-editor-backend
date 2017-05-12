import json
import os

import yaml
import requests

from son_editor.util.requestutil import get_config

SCHEMA_ID_VNF = "vnf"
SCHEMA_ID_NS = "ns"

schemas = {}


def load_ns_vnf_from_disk(file: str, model):
    """
    Loads a vnf or network service descriptor from disk and initializes the given model

    :param file: the file path of the descriptor
    :param model: The database  model of the descriptor
    :return: the given updated model
    """
    with open(file, 'r') as stream:
        descriptor = yaml.safe_load(stream)
        model.__init__(descriptor=json.dumps(descriptor),
                       name=descriptor['name'],
                       vendor=descriptor['vendor'],
                       version=descriptor['version'])
        return model


def write_ns_vnf_to_disk(folder: str, model) -> None:
    """
    Saves the given model to disk as a yml file

    :param folder: the folder to write to, either "vnf" or "nsd"
        to specify if a vnf or network service needs to be saved
    :param model: The database  model of the descriptor
    :return: None
    """
    target_dir = os.path.dirname(get_file_path(folder, model))
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    with open(get_file_path(folder, model), 'w') as stream:
        data = json.loads(model.descriptor)
        yaml.safe_dump(data, stream, default_flow_style=False)


def get_file_path(folder: str, model) -> str:
    """
    Returns the filepath to the descriptor computed
    from the models vendor name and version

    :param folder: the folder to write to, either "vnf" or "nsd"
        to specify if a vnf or network service needs to be saved
    :param model: The database  model of the descriptor
    :return: None
    """
    project = model.project
    workspace = project.workspace
    return os.path.join(workspace.path,
                        "projects",
                        project.rel_path,
                        "sources",
                        folder,
                        (model.name + os.path.sep if folder == "vnf" else ""),
                        get_file_name(model))


def get_file_name(model) -> str:
    """
    Get the standard file name for a descriptor

    :param model: The database  model of the descriptor
    :return: The standard descriptor file name, computed from the models vendor name and version
    """
    return "{}-{}-{}.yml".format(model.vendor,
                                 model.name,
                                 model.version)


def update_workspace_descriptor(workspace) -> None:
    """
    Updates the workspace descriptor with data from the workspace model

    :param workspace: The workspace model
    """
    with open(os.path.join(workspace.path, "workspace.yml"), "r") as stream:
        ws_descriptor = yaml.safe_load(stream)

    ws_descriptor['catalogue_servers'] = []
    for cat in workspace.catalogues:
        catalogue_server = {'id': cat.name, 'url': cat.url, 'publish': cat.publish}
        ws_descriptor['catalogue_servers'].append(catalogue_server)
    ws_descriptor['service_platforms'] = {}
    ws_descriptor['default_service_platform'] = ''
    for plat in workspace.platforms:
        platform_server = {'url': plat.url, "credentials": {"token_file": plat.token_path}}
        ws_descriptor['service_platforms'][plat.name] = platform_server
        if plat.publish:
            ws_descriptor['default_service_platform'] = plat.name
    if not ws_descriptor['default_service_platform'] and ws_descriptor['service_platforms']:
        # if no default set, select "first" platform
        ws_descriptor['default_service_platform'] = \
            ws_descriptor['service_platforms'][ws_descriptor['service_platforms'].keys()[0]]['id']
    ws_descriptor['name'] = workspace.name
    ws_descriptor['schema_index'] = workspace.schema_index
    ws_descriptor['schemas_remote_master'] = get_config()["schemas"][workspace.schema_index]['url']

    with open(os.path.join(workspace.path, "workspace.yml"), "w") as stream:
        yaml.safe_dump(ws_descriptor, stream)


def load_workspace_descriptor(workspace) -> None:
    """
    Loads the workspace descriptor from disk and updates the database model

    :param workspace: The workspace database model
    """
    from son_editor.models.repository import Catalogue
    from son_editor.models.repository import Platform

    with open(os.path.join(workspace.path, "workspace.yml"), "r") as stream:
        ws_descriptor = yaml.safe_load(stream)
        if 'catalogue_servers' in ws_descriptor:
            catalogues = ws_descriptor['catalogue_servers']
            for catalogue_server in catalogues:
                workspace.catalogues.append(Catalogue(name=catalogue_server['id'],
                                                      url=catalogue_server['url'],
                                                      publish=catalogue_server['publish'] == 'yes'))
        if 'service_platforms' in ws_descriptor:
            platforms = ws_descriptor['service_platforms']
            for platform_id, platform in platforms.items():
                workspace.platforms.append(Platform(name=platform_id,
                                                    url=platform['url'],
                                                    publish=ws_descriptor['default_service_platform'] == platform_id))
        if 'schema_index' in ws_descriptor:
            workspace.schema_index = ws_descriptor['schema_index']


def load_project_descriptor(project) -> dict:
    """Loads the project descriptor from disk"""
    with open(os.path.join(project.workspace.path, "projects", project.rel_path, "project.yml"), "r") as stream:
        return yaml.safe_load(stream)


def write_project_descriptor(project, project_descriptor):
    """Writes the project database model to disk"""
    with open(os.path.join(project.workspace.path, "projects", project.rel_path, "project.yml"), "w") as stream:
        return yaml.safe_dump(project_descriptor, stream)


def sync_project_descriptor(project) -> None:
    """
    Updates the project model with data from the project descriptor and vice versa

    :param project: The projects database model
    """
    project_descriptor = load_project_descriptor(project)
    project_descriptor_pkg = project_descriptor['package']
    project_descriptor_pkg['name'] = project.name
    if project.description is not None:
        project_descriptor_pkg['description'] = project.description
    elif 'description' in project_descriptor_pkg:
        project.description = project_descriptor_pkg['description']

    if project.maintainer is not None:
        project_descriptor_pkg['maintainer'] = project.maintainer
    elif 'maintainer' in project_descriptor_pkg:
        project.maintainer = project_descriptor_pkg['maintainer']

    if project.vendor is not None:
        project_descriptor_pkg['vendor'] = project.vendor
    elif 'vendor' in project_descriptor_pkg:
        project.vendor = project_descriptor_pkg['vendor']

    if project.version is not None:
        project_descriptor_pkg['version'] = project.version
    elif 'version' in project_descriptor_pkg:
        project.version = project_descriptor_pkg['version']

    if project.publish_to is not None:
        project_descriptor_pkg['publish_to'] = project.publish_to.split(',')
    elif 'publish_to' in project_descriptor_pkg:
        project.publish_to = ','.join(project_descriptor_pkg['publish_to'])
    else:
        project.publish_to = "personal"  # maintain backward compatibility

    if project.repo_url is not None:
        project_descriptor_pkg['repo_url'] = project.repo_url
    elif 'repo_url' in project_descriptor_pkg:
        project.repo_url = project_descriptor_pkg['repo_url']

    write_project_descriptor(project, project_descriptor)


def load_schemas():
    """ Loads the schemas congigured under "schemas" from the schema remotes """
    schemas[SCHEMA_ID_VNF] = []
    schemas[SCHEMA_ID_NS] = []

    s = requests.session()

    for schema in get_config()["schemas"]:
        # load vnf schema
        vnf_schema = dict(schema)
        response = s.get(vnf_schema['url'] + "function-descriptor/vnfd-schema.yml")
        data = response.text
        vnf_schema['schema'] = yaml.safe_load(data)
        schemas[SCHEMA_ID_VNF].append(vnf_schema)

        # load ns schema
        ns_schema = dict(schema)
        response = s.get(vnf_schema['url'] + "service-descriptor/nsd-schema.yml")
        data = response.text
        ns_schema['schema'] = yaml.safe_load(data)
        schemas[SCHEMA_ID_NS].append(ns_schema)


def get_schemas():
    """ Get the schemas
    
    Will load the schemas if still empty
    """
    if not schemas:
        load_schemas()
    return schemas


def get_schema(schema_index, schema_id: str) -> dict:
    """
    Get the requested schema
    :param schema_index: The schema index referring to the "schema"-index in the configuration file
    :param schema_id: either "vnf" or "ns"
    :return: The requested schema 
    """
    return get_schemas()[schema_id][schema_index]["schema"]


def write_private_descriptor(workspace_path: str, is_vnf: bool, descriptor: dict):
    """
    Write the private descriptor into the private cataloge folder on disk
    
    :param workspace_path: The workspace path 
    :param is_vnf: If the descriptor is a vnf
    :param descriptor: the descriptor data
    :return: 
    """
    type_folder = "ns"
    if is_vnf:
        type_folder = "vnf"
    dirs = os.path.join(workspace_path,
                        type_folder,
                        descriptor['vendor'],
                        descriptor['name'],
                        descriptor['version'])
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    file_path = os.path.join(dirs, "descriptor.yml")
    with open(file_path, "w") as stream:
        return yaml.safe_dump(descriptor, stream)

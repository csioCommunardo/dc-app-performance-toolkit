import re
from locustio.common_utils import init_logger, confluence_measure

logger = init_logger(app_type='confluence')


@confluence_measure("csi_embed_sharepoint_document") 
def csi_embed_sharepoint_document(locust):
    r = locust.get('/rest/csi/spc/templaterenderer/vm/csi-embed-sharepoint-document', catch_response = True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    logger.locust_info(f'token: {token}, id: {id}')  # log information for debug when verbose is true in jira.yml file
    if 'Add a SharePoint Document' not in content:
        logger.error(f"'Add a SharePoint Document' was not found in {content}")
    assert 'Add a SharePoint Document' in content  # assert specific string in response content
    
    
@confluence_measure("csi_embed_sharepoint_list") 
def csi_embed_sharepoint_list(locust):
    r = locust.get('/rest/csi/spc/templaterenderer/vm/csi-embed-sharepoint-list', catch_response = True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    logger.locust_info(f'token: {token}, id: {id}')  # log information for debug when verbose is true in jira.yml file
    if 'Add a SharePoint List' not in content:
        logger.error(f"'Add a SharePoint List' was not found in {content}")
    assert 'Add a SharePoint List' in content  # assert specific string in response content
    
@confluence_measure("csi_adal_helper") 
def csi_adal_helper(locust):
    r = locust.get('/plugins/servlet/csi/adal-helper', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    logger.locust_info(f'token: {token}, id: {id}')  # log information for debug when verbose is true in jira.yml file
    if 'Redirect Target for adal' not in content:
        logger.error(f"'Redirect Target for adal' was not found in {content}")
    assert 'Redirect Target for adal' in content  # assert specific string in response content

@confluence_measure("csi_spc_license") 
def csi_spc_license(locust):
    r = locust.get('/rest/csi/spc/license', catch_response=True)  # call app-specific GET endpoint
    content = r.content.decode('utf-8')   # decode response content

    token_pattern_example = '"token":"(.+?)"'
    id_pattern_example = '"id":"(.+?)"'
    token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
    id = re.findall(id_pattern_example, content)    # get ID from response using regexp

    logger.locust_info(f'token: {token}, id: {id}')  # log information for debug when verbose is true in jira.yml file
    if 'licenseValid' not in content:
        logger.error(f"'licenseValid' was not found in {content}")
    assert 'licenseValid' in content  # assert specific string in response content

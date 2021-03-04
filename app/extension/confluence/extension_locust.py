import re
import random
from locustio.common_utils import confluence_measure, fetch_by_re, timestamp_int, \
    TEXT_HEADERS, NO_TOKEN_HEADERS, JSON_HEADERS, RESOURCE_HEADERS, generate_random_string, init_logger, \
    raise_if_login_failed
from locustio.confluence.requests_params import confluence_datasets, Login, ViewPage, ViewDashboard, ViewBlog, \
    CreateBlog, CreateEditPage, UploadAttachments, LikePage

logger = init_logger(app_type='confluence')


@confluence_measure("locust_csi_embed_sharepoint_document") 
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
    
    
@confluence_measure("locust_csi_embed_sharepoint_list") 
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
    
@confluence_measure("locust_csi_adal_helper") 
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

@confluence_measure("locust_csi_spc_license") 
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

@confluence_measure("locust_csi_view_page_document_macro")
def csi_view_page_document_macro(locust):
    
    raise_if_login_failed(locust)
    params = ViewPage()

    r = locust.get(f'/display/CSIO/Document+Macro+View', catch_response=True)
    content = r.content.decode('utf-8')
    if 'Created by' not in content or 'Save for later' not in content:
        logger.error(f'Fail to open page CSIO/Document+Macro+View: {content}')
    assert 'Created by' in content and 'Save for later' in content, 'Could not open page.'
    parent_page_id = fetch_by_re(params.parent_page_id_re, content)
    parsed_page_id = fetch_by_re(params.page_id_re, content)
    space_key = fetch_by_re(params.space_key_re, content)
    tree_request_id = fetch_by_re(params.tree_result_id_re, content)
    has_no_root = fetch_by_re(params.has_no_root_re, content)
    root_page_id = fetch_by_re(params.root_page_id_re, content)
    atl_token_view_issue = fetch_by_re(params.atl_token_view_issue_re, content)
    editable = fetch_by_re(params.editable_re, content)
    ancestor_ids = re.findall(params.ancestor_ids_re, content)

    ancestor_str = 'ancestors='
    for ancestor in ancestor_ids:
        ancestor_str = ancestor_str + str(ancestor) + '&'

    locust.session_data_storage['page_id'] = parsed_page_id
    locust.session_data_storage['has_no_root'] = has_no_root
    locust.session_data_storage['tree_request_id'] = tree_request_id
    locust.session_data_storage['root_page_id'] = root_page_id
    locust.session_data_storage['ancestors'] = ancestor_str
    locust.session_data_storage['space_key'] = space_key
    locust.session_data_storage['editable'] = editable
    locust.session_data_storage['atl_token_view_issue'] = atl_token_view_issue

    locust.get('/rest/helptips/1.0/tips', catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("110"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.get(f'/rest/likes/1.0/content/{parsed_page_id}/likes?commentLikes=true&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/highlighting/1.0/panel-items?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/mywork/latest/status/notification/count?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    r = locust.get(f'/rest/inlinecomments/1.0/comments?containerId={parsed_page_id}&_={timestamp_int()}',
                    catch_response=True)
    content = r.content.decode('utf-8')
    if 'authorDisplayName' not in content and '[]' not in content:
        logger.error(f'Could not open comments for page {parsed_page_id}: {content}')
    assert 'authorDisplayName' in content or '[]' in content, 'Could not open comments for page.'
    locust.get(f'/plugins/editor-loader/editor.action?parentPageId={parent_page_id}&pageId={parsed_page_id}'
                f'&spaceKey={space_key}&atl_after_login_redirect=/pages/viewpage.action'
                f'&timeout=12000&_={timestamp_int()}', catch_response=True)
    locust.get(f'/rest/watch-button/1.0/watchState/{parsed_page_id}?_={timestamp_int()}',
                catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("145"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("150"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("155"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("160"),
                headers=RESOURCE_HEADERS, catch_response=True)

@confluence_measure("locust_csi_view_page_list_macro")
def csi_view_page_list_macro(locust):
    
    raise_if_login_failed(locust)
    params = ViewPage()

    r = locust.get(f'/display/CSIO/List+Macro+View', catch_response=True)
    content = r.content.decode('utf-8')
    if 'Created by' not in content or 'Save for later' not in content:
        logger.error(f'Fail to open page CSIO/List+Macro+View: {content}')
    assert 'Created by' in content and 'Save for later' in content, 'Could not open page.'
    parent_page_id = fetch_by_re(params.parent_page_id_re, content)
    parsed_page_id = fetch_by_re(params.page_id_re, content)
    space_key = fetch_by_re(params.space_key_re, content)
    tree_request_id = fetch_by_re(params.tree_result_id_re, content)
    has_no_root = fetch_by_re(params.has_no_root_re, content)
    root_page_id = fetch_by_re(params.root_page_id_re, content)
    atl_token_view_issue = fetch_by_re(params.atl_token_view_issue_re, content)
    editable = fetch_by_re(params.editable_re, content)
    ancestor_ids = re.findall(params.ancestor_ids_re, content)

    ancestor_str = 'ancestors='
    for ancestor in ancestor_ids:
        ancestor_str = ancestor_str + str(ancestor) + '&'

    locust.session_data_storage['page_id'] = parsed_page_id
    locust.session_data_storage['has_no_root'] = has_no_root
    locust.session_data_storage['tree_request_id'] = tree_request_id
    locust.session_data_storage['root_page_id'] = root_page_id
    locust.session_data_storage['ancestors'] = ancestor_str
    locust.session_data_storage['space_key'] = space_key
    locust.session_data_storage['editable'] = editable
    locust.session_data_storage['atl_token_view_issue'] = atl_token_view_issue

    locust.get('/rest/helptips/1.0/tips', catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("110"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.get(f'/rest/likes/1.0/content/{parsed_page_id}/likes?commentLikes=true&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/highlighting/1.0/panel-items?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/mywork/latest/status/notification/count?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    r = locust.get(f'/rest/inlinecomments/1.0/comments?containerId={parsed_page_id}&_={timestamp_int()}',
                    catch_response=True)
    content = r.content.decode('utf-8')
    if 'authorDisplayName' not in content and '[]' not in content:
        logger.error(f'Could not open comments for page {parsed_page_id}: {content}')
    assert 'authorDisplayName' in content or '[]' in content, 'Could not open comments for page.'
    locust.get(f'/plugins/editor-loader/editor.action?parentPageId={parent_page_id}&pageId={parsed_page_id}'
                f'&spaceKey={space_key}&atl_after_login_redirect=/pages/viewpage.action'
                f'&timeout=12000&_={timestamp_int()}', catch_response=True)
    locust.get(f'/rest/watch-button/1.0/watchState/{parsed_page_id}?_={timestamp_int()}',
                catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("145"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("150"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("155"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("160"),
                headers=RESOURCE_HEADERS, catch_response=True)

@confluence_measure("locust_csi_view_blog_document_macro")
def csi_view_page_blog_document_macro(locust):
    
    raise_if_login_failed(locust)
    params = ViewPage()

    r = locust.get(f'/display/CSIO/2021/01/01/Blog+Document+Macro+View', catch_response=True)
    content = r.content.decode('utf-8')
    if 'Created by' not in content or 'Save for later' not in content:
        logger.error(f'Fail to open page CSIO/2021/01/01/Blog+Document+Macro+View: {content}')
    assert 'Created by' in content and 'Save for later' in content, 'Could not open page.'
    parent_page_id = fetch_by_re(params.parent_page_id_re, content)
    parsed_page_id = fetch_by_re(params.page_id_re, content)
    space_key = fetch_by_re(params.space_key_re, content)
    tree_request_id = fetch_by_re(params.tree_result_id_re, content)
    has_no_root = fetch_by_re(params.has_no_root_re, content)
    root_page_id = fetch_by_re(params.root_page_id_re, content)
    atl_token_view_issue = fetch_by_re(params.atl_token_view_issue_re, content)
    editable = fetch_by_re(params.editable_re, content)
    ancestor_ids = re.findall(params.ancestor_ids_re, content)

    ancestor_str = 'ancestors='
    for ancestor in ancestor_ids:
        ancestor_str = ancestor_str + str(ancestor) + '&'

    locust.session_data_storage['page_id'] = parsed_page_id
    locust.session_data_storage['has_no_root'] = has_no_root
    locust.session_data_storage['tree_request_id'] = tree_request_id
    locust.session_data_storage['root_page_id'] = root_page_id
    locust.session_data_storage['ancestors'] = ancestor_str
    locust.session_data_storage['space_key'] = space_key
    locust.session_data_storage['editable'] = editable
    locust.session_data_storage['atl_token_view_issue'] = atl_token_view_issue

    locust.get('/rest/helptips/1.0/tips', catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("110"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.get(f'/rest/likes/1.0/content/{parsed_page_id}/likes?commentLikes=true&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/highlighting/1.0/panel-items?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/mywork/latest/status/notification/count?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    r = locust.get(f'/rest/inlinecomments/1.0/comments?containerId={parsed_page_id}&_={timestamp_int()}',
                    catch_response=True)
    content = r.content.decode('utf-8')
    if 'authorDisplayName' not in content and '[]' not in content:
        logger.error(f'Could not open comments for page {parsed_page_id}: {content}')
    assert 'authorDisplayName' in content or '[]' in content, 'Could not open comments for page.'
    locust.get(f'/plugins/editor-loader/editor.action?parentPageId={parent_page_id}&pageId={parsed_page_id}'
                f'&spaceKey={space_key}&atl_after_login_redirect=/pages/viewpage.action'
                f'&timeout=12000&_={timestamp_int()}', catch_response=True)
    locust.get(f'/rest/watch-button/1.0/watchState/{parsed_page_id}?_={timestamp_int()}',
                catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("145"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("150"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("155"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("160"),
                headers=RESOURCE_HEADERS, catch_response=True)

@confluence_measure("locust_csi_view_blog_list_macro")
def csi_view_page_blog_list_macro(locust):
    
    raise_if_login_failed(locust)
    params = ViewPage()

    r = locust.get(f'/display/CSIO/2021/01/01/Blog+List+Macro+View', catch_response=True)
    content = r.content.decode('utf-8')
    if 'Created by' not in content or 'Save for later' not in content:
        logger.error(f'Fail to open page CSIO/2021/01/01/Blog+List+Macro+View: {content}')
    assert 'Created by' in content and 'Save for later' in content, 'Could not open page.'
    parent_page_id = fetch_by_re(params.parent_page_id_re, content)
    parsed_page_id = fetch_by_re(params.page_id_re, content)
    space_key = fetch_by_re(params.space_key_re, content)
    tree_request_id = fetch_by_re(params.tree_result_id_re, content)
    has_no_root = fetch_by_re(params.has_no_root_re, content)
    root_page_id = fetch_by_re(params.root_page_id_re, content)
    atl_token_view_issue = fetch_by_re(params.atl_token_view_issue_re, content)
    editable = fetch_by_re(params.editable_re, content)
    ancestor_ids = re.findall(params.ancestor_ids_re, content)

    ancestor_str = 'ancestors='
    for ancestor in ancestor_ids:
        ancestor_str = ancestor_str + str(ancestor) + '&'

    locust.session_data_storage['page_id'] = parsed_page_id
    locust.session_data_storage['has_no_root'] = has_no_root
    locust.session_data_storage['tree_request_id'] = tree_request_id
    locust.session_data_storage['root_page_id'] = root_page_id
    locust.session_data_storage['ancestors'] = ancestor_str
    locust.session_data_storage['space_key'] = space_key
    locust.session_data_storage['editable'] = editable
    locust.session_data_storage['atl_token_view_issue'] = atl_token_view_issue

    locust.get('/rest/helptips/1.0/tips', catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("110"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.get(f'/rest/likes/1.0/content/{parsed_page_id}/likes?commentLikes=true&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/highlighting/1.0/panel-items?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    locust.get(f'/rest/mywork/latest/status/notification/count?pageId={parsed_page_id}&_={timestamp_int()}',
                catch_response=True)
    r = locust.get(f'/rest/inlinecomments/1.0/comments?containerId={parsed_page_id}&_={timestamp_int()}',
                    catch_response=True)
    content = r.content.decode('utf-8')
    if 'authorDisplayName' not in content and '[]' not in content:
        logger.error(f'Could not open comments for page {parsed_page_id}: {content}')
    assert 'authorDisplayName' in content or '[]' in content, 'Could not open comments for page.'
    locust.get(f'/plugins/editor-loader/editor.action?parentPageId={parent_page_id}&pageId={parsed_page_id}'
                f'&spaceKey={space_key}&atl_after_login_redirect=/pages/viewpage.action'
                f'&timeout=12000&_={timestamp_int()}', catch_response=True)
    locust.get(f'/rest/watch-button/1.0/watchState/{parsed_page_id}?_={timestamp_int()}',
                catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("145"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("150"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("155"),
                headers=RESOURCE_HEADERS, catch_response=True)
    locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("160"),
                headers=RESOURCE_HEADERS, catch_response=True)

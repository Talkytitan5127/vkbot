#!/usr/bin/python3

import sys

def get_docs(data):
    attachs = []
    links = []
    id_iu8 = os.environ['iu8_peer']
    for elem in data:
        type_mes = elem['type']
        if type_mes == 'link':
            links.append(elem[type_mes]['url'])
            continue
        info_doc = elem[type_mes]
        if type_mes == 'doc':
            links.append(info_doc['url'])
        owner_id = info_doc['owner_id']
        media_id = info_doc['id']
        access_key = info_doc['access_key']
        pack = '{}{}_{}'.format(type_mes, owner_id, media_id)
        if owner_id != id_iu8:
            pack += '_{}'.format(access_key)
        attachs.append( pack )

    return attachs, links


def send_post(data):
    text_mes = data['text']
    attach_mes = []
    links = []
    template = '*' * 25 + '\n{}\n' + '*' * 25
    if 'attachments' in data.keys():
        try:
            attach_mes, links = get_docs(data['attachments'])
        except:
            text_mes += "\n\n Более подробную информацию смотрите в нашей группе"
    
    make_request(
        method='messages.send',
        data={
            'peer_id': 2000000000 + 2, # peer id of chat
            'message': template.format(text_mes + '\n\n' + ','.join(links)),
            'attachment': ','.join(attach_mes)
        }
    )

    return 'ok'


def run(data, method):
    global make_request
    make_request = method

    type_event = {
        'wall_post_new': send_post,
    }

    # data = json-package
    try:
        type_event[ data['type'] ](data['object'])
    except:
        return sys.exc_info()

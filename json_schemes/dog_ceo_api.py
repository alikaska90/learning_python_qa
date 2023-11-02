JSON_SCHEMA_ONE_ITEM = {
    'type': 'object',
    'properties': {
        'message': {'type': 'string'},
        'status': {'type': 'string'}
    }
}

JSON_SCHEMA_SEVERAL_ITEMS = {
    'type': 'object',
    'properties': {
        'message': {
            'type': 'array',
            'items': {'type': 'string'}
        },
        'status': {'type': 'string'}
    }
}

JSON_SCHEMA_ALL_BREEDS = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string'},
        'message': {
            'type': 'object',
            'properties': {
                '^[a-z]+$': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            }
        }
    }
}

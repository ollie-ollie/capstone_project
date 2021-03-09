from exceptions import RequestBodyError


def validate_post_request_body_actor(body):
    if not body or ('name' not in body
                    or 'age' not in body
                    or 'gender' not in body):
        raise RequestBodyError({
            'code': 'Request body error',
            'description': 'Request body was empty or valid keys are missing'
            }, 400)

    return True

def validate_patch_request_body_actor(body):
    if not body or ('name' not in body
                    and 'age' not in body
                    and 'gender' not in body):
        raise RequestBodyError({
            'code': 'Request body error',
            'description': 'Request body was empty or valid keys are missing'
            }, 400)

    return True

def validate_body_movie(body):
    if not body or ('title' not in body and 'release_date' not in body):
        raise RequestBodyError({
            'code': 'Request body error',
            'description': 'Request body was empty or valid keys are missing'
            }, 400)

    return True
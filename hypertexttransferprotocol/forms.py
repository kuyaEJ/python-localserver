def get(form, values, default_value):
    form_data = []
    for val in values.split(' '):
        form_data.append(form.get(val, default_value)[0])
    return form_data

def validate_user():
    # UNIQUE, all lowercase, input case insensitive, not null, not empty
    pass

def validate_pass():
    # one upper letter, one symbol [!@#$%&*+], not null, not empty
    pass

def validate_email():
    # x@y.z not empty, not null, unique, case insensitive
    pass

def validate_phone():
    # (xxx) xxx-xxxx not empty, not null, unique, no alphanumeric inputs
    pass
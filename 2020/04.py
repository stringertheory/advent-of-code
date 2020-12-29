

def f_maker(parser=lambda x: x, validator=lambda x: False):
    def f(string):
        value = parser(string)
        return {
            'raw': string,
            'value': value,
            'valid': validator(value),
        }
        return result
    return f
        
def parse_hgt(string):
    if string.endswith('in'):
        unit = 'in'
    elif string.endswith('cm'):
        unit = 'cm'
    else:
        return {
            'value': string,
            'unit': None,
        }
    return {
        'value': int(string[:-2]),
        'unit': unit,
    }

def validate_hgt(value):
    if value['unit'] == 'in':
        return (59 <= value['value'] <= 76)
    elif value['unit'] == 'cm':
        return (150 <= value['value'] <= 193)
    else:
        return False

def validate_hcl(s):
    if not (s.startswith('#') or len(s) == 7):
        return False
    try:
        int(s[1:], 16)
    except:
        return False
    else:
        return True

def validate_ecl(s):
    return s in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

def validate_pid(s):
    if len(s) != 9:
        return False
    try:
        int(s)
    except:
        return False
    else:
        return True
    
required = {
    'byr': f_maker(lambda x: int(x), lambda x: (1920 <= x <= 2002)),
    'iyr': f_maker(lambda x: int(x), lambda x: (2010 <= x <= 2020)),
    'eyr': f_maker(lambda x: int(x), lambda x: (2020 <= x <= 2030)),
    'hgt': f_maker(parse_hgt, validate_hgt),
    'hcl': f_maker(validator=validate_hcl),
    'ecl': f_maker(validator=validate_ecl),
    'pid': f_maker(validator=validate_pid),
}

optional = {
    'cid': f_maker(validator=lambda x: True),
}

def validate_one(passport):
    missing = set(required.keys()).difference(set(passport.keys()))
    if missing:
        return {
            'valid': False,
            'note': 'missing fields {}'.format(missing),
        }
    else:
        return {
            'valid': True,
        }

def validate_two(passport):

    clean = {
        'valid': False,
        'value': {},
    }
    for key, value in passport.items():
        f = required.get(key) or optional.get(key)
        if f:
            clean['value'][key] = f(value)
        else:
            clean['value'][key] = {
                'raw': value,
                'valid': None,
                'note': 'unknown key {}'.format(key),
            }

    missing = set(required.keys()).difference(set(passport.keys()))
    if missing:
        clean['valid'] = False
        clean['note'] = 'missing fields {}'.format(missing)
        return clean

    dirty = []
    for key in required:
        if not clean['value'][key]['valid']:
            dirty.append(key)
    if dirty:
        clean['valid'] = False
        clean['note'] = 'invalid fields {}'.format(dirty)
        return clean
    
    clean['valid'] = True
    return clean

def read_raw_passports(filename):

    with open(filename) as infile:
        text = infile.read().strip()

    result = []
    for i in text.split('\n\n'):
        values = [i.strip() for i in i.strip().split()]
        fields = {}
        for field in values:
            key, value = field.split(':')
            fields[key] = value

        result.append(fields)

    return result

# for p in read_raw_passports('input-04.txt'):
#     pprint.pprint(validate_two(p))
#     print()

clean = [validate_one(_) for _ in read_raw_passports('input-04.txt')]

print(len(clean), 'total')
print(len([i for i in clean if i['valid']]), 'valid')

clean = [validate_two(_) for _ in read_raw_passports('input-04.txt')]

print(len([i for i in clean if i['valid']]), 'valid 2')

def get_range(reflector_id: int):
    data = 6.0 # katedilen mesafe

    if reflector_id in list(range(1, 20)): # sari kirmizili reflektor alanina geldi
        data =  (reflector_id-1) * 4 + data
        return data

    data = 78.0
    if reflector_id in list(range(20, 60)):
        data = (reflector_id-19) * 0.05 + data
        return data
    data = 79.95

    if reflector_id == 60:
        data = 2.05 + data
        return data
    data = 82.0
        
    if reflector_id in list(range(61, 74)):
        data = (reflector_id-61) * 4 + data
        return data
    
    data = 130.0

    if reflector_id in list(range(74, 94)):
        data = (reflector_id-74) * 0.05 + data
        return data
    
    data = 130.95

    if reflector_id == 94:
        data = 3.05 + data
        return data
    data = 134.0

    if reflector_id in list(range(95, 107)):
        data = (reflector_id-95) * 4 + data
        return data


print(get_range(23))

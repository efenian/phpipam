def check_list(t_list='', t_item='', t_string=''):
    """ function to check list length and raise appropriate exception """
    not_found = t_string.capitalize()  + ' not found: ' + t_item
    ambiguous = 'Abiguous ' + t_string +  ' match: ' + t_item
    if len(t_list) == 0:
        raise ValueError(not_found)
    if len(t_list) > 1:
        raise ValueError(ambiguous)

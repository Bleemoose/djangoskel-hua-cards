from collections import Counter
from huaskel import settings

def count_occurences(password,character_set):
    """
    Count number of occurences of any characters in character_set in password
    """

    no_occ = 0

    c = Counter(password)
    for x in c:
        if x in character_set:
            no_occ = no_occ + c[x]

    return no_occ

def occurences_of_special(password):
    """
    Counts how many times do a special characters appear in the password
    """
    return count_occurences(password , settings.PASSWORD_SPECIAL_CHARACTERS)

def occurences_of_digits(password):
    """
    Counts how many times do digits appear in the password
    """
    digits=['0','1','2','3','4','5','6','7','8','9']

    return count_occurences(password , digits)

def password_is_ok(password):
    """
    Check the complexity of the password
    """
    is_ok_special_characters = occurences_of_special(password) >= settings.PASSWORD_NUMBER_SPECIAL
    is_ok_digits = occurences_of_digits(password) >= settings.PASSWORD_NUMBER_DIGITS
    is_ok_length = len(password) >= settings.PASSWORD_MINIMUM_LENGTH
    return( is_ok_special_characters & is_ok_digits & is_ok_length )

def password_policy():
    """
    Returns the current password
    """

    str_pol = 'must '

    if settings.PASSWORD_NUMBER_SPECIAL > 0:
        str_special = 'contain at least %d characters out of the following %s' %(settings.PASSWORD_NUMBER_SPECIAL,
                       ''.join( settings.PASSWORD_SPECIAL_CHARACTERS) )
    if settings.PASSWORD_NUMBER_DIGITS > 0:
        str_digits = 'contain at least %d digits' %settings.PASSWORD_NUMBER_DIGITS

    if str_special and str_digits:
        str_pol = str_pol + str_special + ' and ' + str_digits
    elif str_special:
        str_pol = str_pol + str_special
    elif str_digits:
        str_pol = str_pol + str_digits
    else:
        str_pol = ''

    return(str_pol)

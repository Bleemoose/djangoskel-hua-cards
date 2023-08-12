import ldap
from huaskel import settings

def decodeAttribute(entry, attribute):
    if attribute in entry:
        return entry[attribute][0].decode('utf8')
    else:
        return None

def convertToDict(entry):
    return {
        'givenName' : decodeAttribute(entry, settings.GIVEN_NAME_LDAP_ATTRIBUTE),
        'sn' : decodeAttribute(entry, settings.SURNAME_LDAP_ATTRIBUTE),
        'mail' : decodeAttribute(entry, settings.EXTERNAL_MAIL_LDAP_ATTRIBUTE),
        'title' : decodeAttribute(entry, settings.TITLE_LDAP_ATTRIBUTE),
        'department' : decodeAttribute(entry, settings.DEPARTMENT_LDAP_ATTRIBUTE),
    }

class ldapConnection:

    handler = None

    def connect(self):
       """
       Connect to LDAP
       """
       self.handler = ldap.initialize( settings.AUTH_LDAP_SERVER_URI )
       if settings.AUTH_LDAP_START_TLS:
           self.handler.start_tls_s()

       self.handler.simple_bind( settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD)

    def verify(self, uid, externalMail):
        """
        Verify that user externalMail is correct
        """
        query = '(&(' + settings.EXTERNAL_MAIL_LDAP_ATTRIBUTE + '=' + externalMail + ')(uid=' + uid + '))'
        result = self.handler.search_s(settings.AUTH_LDAP_BASE_DN, ldap.SCOPE_SUBTREE, query)
        if len(result) == 1:
            return True
        else:
            return False


    def getUserMail(self, uid):
        """
        get user externalMail
        """
        query = '(uid=%s)' %uid
        result = self.handler.search_s(settings.AUTH_LDAP_BASE_DN, ldap.SCOPE_SUBTREE, query)
        if len(result) == 1:
            ldapEntry = result[0][1]
            if settings.EXTERNAL_MAIL_LDAP_ATTRIBUTE in ldapEntry:
                return ldapEntry[settings.EXTERNAL_MAIL_LDAP_ATTRIBUTE][0].decode('utf8')
            else:
                return None
        else:
            return None

    def getUserInfo(self, uid):
        """
        get user information: username, givenName, sn and externalMail
        """
        query = '(uid=%s)' %uid
        result = self.handler.search_s(settings.AUTH_LDAP_BASE_DN, ldap.SCOPE_SUBTREE, query)
        if len(result) == 1:
            return convertToDict( result[0][1] )
        else:
            return None

    def close(self):
        self.handler.unbind_s()

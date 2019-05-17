'''
We are given a personal information string S, which may represent either an email address or a phone number.
We would like to mask this personal information according to the following rules:

1. Email address:
We define a name to be a string of length ≥ 2 consisting of only lowercase letters a-z or uppercase letters A-Z.
An email address starts with a name, followed by the symbol '@', followed by a name, followed by the dot '.' and followed by a name.
All email addresses are guaranteed to be valid and in the format of "name1@name2.name3".
To mask an email, all names must be converted to lowercase and all letters between the first and last letter of the first name must be replaced by 5 asterisks '*'.

2. Phone number:
A phone number is a string consisting of only the digits 0-9 or the characters from the set {'+', '-', '(', ')', ' '}. You may assume a phone number contains 10 to 13 digits.
The last 10 digits make up the local number, while the digits before those make up the country code. Note that the country code is optional. We want to expose only the last 4 digits and mask all other digits.
The local number should be formatted and masked as "***-***-1111", where 1 represents the exposed digits.
To mask a phone number with country code like "+111 111 111 1111", we write it in the form "+***-***-***-1111".  The '+' sign and the first '-' sign before the local number should only exist if there is a country code.  For example, a 12 digit phone number mask should start with "+**-".
Note that extraneous characters like "(", ")", " ", as well as extra dashes or plus signs not part of the above formatting scheme should be removed.
Return the correct "mask" of the information provided.

Notes:
S.length <= 40.
Emails have length at least 8.
Phone numbers have length at least 10.

'''

class Solution:
    def maskPII(self, S):
        """
        :type S: str
        :rtype: str
        """
        if S[0].isalpha():
            return self.mask_email(S)
        else:
            return self.mask_phone(S)

    ''' Assume we are getting an email address, and it is correctly formatted'''
    def mask_email(self, email):
        email = email.lower()
        username, domain = email.split('@')

        result = username[0] + '*****' + username[-1] + '@'
        result = result + domain
        return result

    # identify a local or an international number and call the correct masking method
    # Local nums: either have country code 1, or no country code and exactly 10 digits
    #             and no country code
    # International: have a non-1 country code
    #             To identify country code we look for either of these patterns:
    #               +ccc-    or cc(nnn)  where 'c' is a coutry code digit and 'n' is a phone number digit
    def mask_phone(self, s):
        # Remove any digits that are not [+-()d]
        clean_num = [d for d in s if d.isdigit()]
        local_num = clean_num[-10:]
        if len(clean_num) > 10:
            country_code = clean_num[0:-10]
        else:
            country_code = []


        result = ''.join(local_num[-4:])
        local_num = country_code + local_num[0:-4]
        while len(local_num) > 2:
            result = '***-' + result
            local_num = local_num[3:]

        if local_num:
            result = '*' * len(local_num) + '-' + result

        if country_code:
            result = '+' + result

        return result



    def mask_phone_too_complicated(self, s):
        # Remove any digits that are not [+-()d]
        clean_num = [d for d in s if d in '+-()0123456789']

        country_code = '1'
        local_num = clean_num

        # Check for +ccc- format for country code
        if clean_num[0] == '+':
            if '(' in clean_num:
                cc_end = clean_num.index('(')
            elif '-' in clean_num:
                cc_end = clean_num.index('-')

            country_code = clean_num[1:cc_end]
            local_num = clean_num[cc_end:]

        # Check for format cc(nnn)nnnn
        elif '(' in clean_num:
            paren_start = clean_num.index('(')
            if paren_start > 0:
                country_code = clean_num[0:paren_start]
                local_num = clean_num[paren_start:]

        # Strip all but digits from localnum
        local_num = [d for d in local_num if d.isdigit()]

        country_code = ''.join([d for d in country_code if d.isdigit()])
        if country_code == '1':
            result = '***-***-' + ''.join(local_num[-4:])

        else:
            result = ''.join(local_num[-4:])
            local_num = list(country_code) + local_num[0:-4]
            while len(local_num) > 2:
                result = '***-' + result
                local_num = local_num[3:]

            if local_num:
                result = '*' * len(local_num) + '-' + result

            result = '+' + result
            # Add in country code
            # if country_code:
            #     result = '+' + '*' * len(country_code) + '-' + result
            # else:
            #     result = '+' + result


        return result

    def test(self):
        
        test_cases = [
            "+1(19)5 246 5964",
            "+(501321)-50-23431",
            "86-(10)12345678",
            '+11(415)-518-4473',
            "1(2615)712-6-686",
            "alex@idiom.com"
    
        ]

        for tc in test_cases:
            print(tc, ' -> ', self.maskPII(tc))


Solution().test()

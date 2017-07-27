# owa_brute
Horizontal Brute Forcing tool for OWA

Includes a flag for issuing a domain discover request. You can find the domain within the WWW-Authenticate header of a failed authentication attempt. You should also see 'NTLM' within the same header indicating that NTLM authentication is available. 

Brute Forcing features:
- UN/PW Lists : Provide large number of usernames and passwords
- Horizontal attack : Attack will iterate off of password rather than username.
- Frequency tracking : Prevent account lockout by dictating minimum time between attempts (per user tracking). Default is 30 minutes. If lockout policy is > 3 attempts per 30 minutes, than set value to 10 minutes. 
- Scramble User list : Avoids patterns in authentication by changing the username order during each iteration. 

Tool has been lightly tested. Please let me know if you encounter issues. 

Dependencies:
pip3 install requests_ntlm

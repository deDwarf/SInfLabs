from unittest import TestCase
from Crypto.PublicKey import DSA as LIB_DSA
from app.DSA.dsa import DSA
import app.DSA.utils.dsa_keygen as keygen


class TestDSA(TestCase):

    common_params = dict(
        p=130084120578419659631351055120986923276185471290527395776016514846910152061425822654858978525469339244891727456925286137231914514017237899601947681268087618782181376922091229779101535317920996317829875142670852291329812095514293848738075243010758024763644024533830541417781254285022974804575763908304768042211,
        q=1264171192471153939244571712621422814298151329033,
        g=112760727537342413189250256294029447419664001935075661771737725055560449856713163114983975064104694777935555225209555293801777234333271407226393849626059842936633623432976850281310555886968886368915710430473670362791063443857080382929202579747473475934213202930772675048208585847850794258001812676320454601601
    )

    keys = dict(
        x=475784412254223463800106448777030749352740890436,
        y=106189223974264157928462986923635547581901114444744849636452898778135170301290833120382480754789392937922251861906237030977488332161892377850130659511423759677235608851092800937042646200652871375588448782341731602857657760833205775126464577822131811134001917811961177244860419862494698633313347700089730234859
    )

    def test_dsa(self):
        x = self.keys.get('x')
        y = self.keys.get('y')
        msg = "Any message you would like to sign off"
        signature = DSA.sign(msg, self.common_params, x)
        res = DSA.verify(msg, signature, self.common_params, y)
        self.assertTrue(res)

        signature['s'] += 3
        res = DSA.verify(msg, signature, self.common_params, y)
        self.assertFalse(res)

    def test_dsa_with_key_generation(self):
        x = keygen.generate_private_key(self.common_params)
        y = keygen.generate_public_key(self.common_params, x)
        msg = "Any message you would like to sign off"
        signature = DSA.sign(msg, self.common_params, x)
        res = DSA.verify(msg, signature, self.common_params, y)
        self.assertTrue(res)

        signature['s'] += 3
        res = DSA.verify(msg, signature, self.common_params, y)
        self.assertFalse(res)

# ////////////////////////// # ////////////////////
    @staticmethod
    def __generate_valid_key():
        key = LIB_DSA.generate(1024)
        [print('{}: {}'.format(i, key._key[i])) for i in key._key]


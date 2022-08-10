# import logging
# import unittest

# from commands import subscribe_slash_commands

# from discord.app_commands import CommandTree


# class TestStringMethods(unittest.TestCase):
#     def test_upper(self):
#         logging.error("hasca")
#         self.assertEqual("foo".upper(), "FOO")

#     def test_isupper(self):
#         self.assertTrue("FOO".isupper())
#         self.assertFalse("Foo".isupper())

#     def test_split(self):
#         s = "hello world"
#         self.assertEqual(s.split(), ["hello", "world"])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

#     def test_commands(self):
#         ...


# if __name__ == "__main__":
#     a = unittest.main(verbosity=1)
#     print(a.result)

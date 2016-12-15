import binascii
import os

prefix_customer = 'uploads/customer/'


def upload_user_profile(instance, filename):
    key = binascii.b2a_hex(os.urandom(5))
    file_base, extension = filename.split(".")
    path_file = u"{0:s}/user-{1:s}.{2:s}".format(
        str(instance.user.id), str(key), extension)
    return os.path.join(prefix_customer, path_file)

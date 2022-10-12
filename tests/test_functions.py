from src.functions import *
from os.path import exists
from os import remove
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import pytest


@pytest.fixture(autouse=True)
def init_test_files():
    filenames = ['test1.txt', 'test2.txt', 'test3.txt']
    for filename in filenames:
        with open(filename, 'w') as file:
            file.write(filename)


def clear_directory():
    files = ['sign_key', 'sign_key.pub', 'test1.txt', 'test2.txt', 'test3.txt', 'test1.sig', 'test2.sig', 'test3.sig']
    for file in files:
        remove(file)


def test_generate_key_pair_creates_files():
    generate_key_pair('.')
    assert exists('sign_key')
    assert exists('sign_key.pub')


def test_get_key_from_yandex_ok():
    key = get_key_from_yandex("https://disk.yandex.ru/d/PpYs5t5hujPEzA")
    assert isinstance(key, RSA.RsaKey)


def test_get_key_from_file_ok():
    key = get_key_from_file('sign_key')
    assert isinstance(key, RSA.RsaKey)


def test_get_key_from_file_error():
    key = get_key_from_file('12312312')
    assert key is None


@pytest.mark.parametrize("key_path", ['sign_key', 'https://disk.yandex.ru/d/PpYs5t5hujPEzA'])
def test_get_key_returns_key(key_path):
    assert isinstance(get_key(key_path), RSA.RsaKey)


def test_get_hash_ok(init_test_files):
    assert isinstance(get_hash("test1.txt"), SHA256.SHA256Hash)


def test_get_hash_not_unique():
    assert get_hash("test1.txt").hexdigest() == get_hash("test1.txt").hexdigest()


def test_get_signature_returns_bytes():
    assert isinstance(get_signature(get_key("sign_key"), "test1.txt"), bytes)


@pytest.mark.parametrize(
    "test_file, sign_name",
    [("test1.txt", "test1.sig"), ("test2.txt", "test2.sig"), ("test3.txt", "test3.sig")]
)
def test_sign_creates_right_files(test_file, sign_name):
    sign(get_key("sign_key"), test_file)
    assert exists(sign_name)


def test_verify_signature_ok():
    verify_signature(get_key("sign_key.pub"), "test1.txt", "test1.sig")
    assert True


def test_verify_invalid_signature():
    with pytest.raises(ValueError):
        verify_signature(get_key("sign_key.pub"), "test1.txt", "test2.sig")
    clear_directory()

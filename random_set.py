#coding: utf-8

import random, string

import redis

def randomword(words, length):
    return ''.join(random.choice(words) for i in range(length))


def get_words():
    word_file="/usr/share/dict/words"
    words = open(word_file).read().splitlines()
    return words[:1000]


def get_mapping(words, length=1000):
    d = {}
    for word in words:
        d[word] = random.randint(1, length)
    return d


def random_set(client, words, length=1000):
    d = get_mapping(words, length)
    client.mset(d)


def random_hset(client, words, length=1000):
    d = get_mapping(words, length)
    client.hmset("hashName", d)


def random_lpush(client, words, length=1000):
    value = random.randint(1, length)
    client.lpush("listName", *words)


def random_zadd(client, words, length=1000):
    d = get_mapping(words, length)
    client.zadd("myset", **d)


def main():
    words = get_words()
    client = redis.Redis(db=0)
    print "Flush all data before insert new"
    client.flushall()

    random_set(client, words)
    print "random_set done"
    random_hset(client, words)
    print "random_hset done"
    random_lpush(client, words)
    print "random_lpush done"
    random_zadd(client, words)
    print "All Done"

if __name__ == "__main__":
    main()



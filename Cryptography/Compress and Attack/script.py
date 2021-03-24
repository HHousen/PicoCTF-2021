import sys
import random
import threading
import time


class TwoTriesGuess(object):
    def __init__(self, oracle, prefix, letter, complement):
        """ Create Guess object.
    `prefix` is a known prefix to prepend with the guessed letter.
    `letter` is the new guessed letter.
    `complement` the alphabet complement to use for detecting false-positives.
    """
        self.oracle = oracle
        self.prefix = prefix
        self.letter = letter
        self.complement = complement

        self.good_length = None  # length of the presumed good guess
        self.bad_length = None  # length of the presumed bad guess

        return

    def __len__(self):
        return self.good_length

    def __str__(self):
        return self.prefix + self.letter

    def __repr__(self):
        return "%s(%s+%s->%s)" % (
            self.__class__.__name__,
            repr(self.prefix),
            repr(self.letter),
            "unknown length"
            if self.good_length is None
            else "%u,%u" % (self.good_length, self.bad_length),
        )

    def keep(self):
        """ return True if the good guess should be kept. """
        return self.good_length < self.bad_length

    def discard(self):
        """ return True if the good guess should be discarded. """
        return self.good_length > self.bad_length

    def run(self):
        """ implement the logic behind determining the length of this guess """

        # run it!
        self.good_length = self.oracle.oracle(
            self.prefix + self.letter + self.complement
        )
        self.bad_length = self.oracle.oracle(
            self.prefix + self.complement + self.letter
        )

        return


class TwoTriesBlockCipherGuess(TwoTriesGuess):
    def range(self):
        """ Default range for 8 or 16 bytes block cipher. """
        return range(0, 20)

    def guesses(self, uncompressible_bytes):
        good = self.oracle.oracle(
            uncompressible_bytes + self.prefix + self.letter + self.complement
        )
        bad = self.oracle.oracle(
            uncompressible_bytes + self.prefix + self.complement + self.letter
        )
        return good, bad

    def run(self):
        """ implement the logic behind determining the length of this guess """
        # print 'guess', self.prefix, self.letter

        ref = ref_good, ref_bad = self.guesses(uncompressible_bytes="")
        if ref_good != ref_bad:
            # print 'keep ref', repr(ref)
            self.good_length, self.bad_length = ref
            return

        for n in self.range():
            bytes = self.oracle.get_uncompressible_bytes(n)
            this = this_good, this_bad = self.guesses(uncompressible_bytes=bytes)
            if this_good != ref_good or this_bad != ref_bad:
                self.good_length, self.bad_length = this
                # print 'keep this', n, repr(ref), '->', repr(this)
                return

        # print 'not found'
        return


class CompressionOracleRunner():
    def __init__(self, guess):
        # threading.Thread.__init__(self)
        self.guess = guess
        return

    def run(self):
        return self.guess.run()
    
    def start(self):
        return self.run()


class CompressionOracle(object):
    def __init__(
        self,
        seed,
        alphabet,
        max_threads=1,
        complement_size=[20, 200],
        retries=5,
        lookaheads=1,
        guess_provider=TwoTriesGuess,
    ):
        assert max_threads > 0, "max_threads cannot be <= 0"
        self.seed = seed
        self.max_threads = max_threads
        self.alphabet = alphabet
        self.retries = retries
        self.lookaheads = lookaheads
        self.complement_size = complement_size

        self.__tries = []

        self.retreived_guesses = None
        self.guess_provider = guess_provider
        return

    def oracle(self):
        """ Must be overriden by subclasses and implement the logic to query the compression oracle. """
        raise NotImplemented("oracle() must be overriden")

    def prepare(self):
        """ May be overriden by subclasses and make any initialization before running the attack. """
        return

    def cleanup(self):
        """ May be overriden by subclasses and cleanup any ressources after running the attack. """
        return

    def get_uncompressible_bytes(self, length):
        """ This must return a string which should not compress well. It could
      be random data or it could be a sequence of bytes garanteed to not
      contain any repetition.

      Subclasses can override this method, the default implementation
      returns a random string of letters complementary to the alphabet.
    """

        possible_complement = bytearray([chr(i) for i in range(256)])
        possible_complement.translate(possible_complement, self.alphabet)
        if len(possible_complement) == 0:
            possible_complement = bytearray([chr(i) for i in range(256)])

        return bytearray(
            [chr(random.choice(possible_complement)) for _ in range(length)]
        )

    def prepare_complement(self):
        """ Prepare an alphabet complement for the Two-Tries method. """

        if type(self.complement_size) in (list, tuple):
            size = random.randint(*self.complement_size)
        else:
            size = self.complement_size

        possible_complement = bytearray([chr(i) for i in range(256)])
        possible_complement.translate(possible_complement, self.alphabet)
        if len(possible_complement) != 0:
            return bytearray(random.sample(possible_complement, 2) * size)

        return bytearray([chr(random.randint(0, 0xFF)) for _ in range(2)] * size)

    def __run_all(self, guesses):

        queue = guesses[:]

        while len(queue) > 0:
            # start as many threads as permitted
            g = queue.pop(0)

            t = CompressionOracleRunner(g)
            t.start()

            if len(queue) == 0:
                break

        kept = [g for g in guesses if g.keep()]
        return kept

    def run(self):
        """ run the attack against the comression oracle. """

        complement = self.prepare_complement()
        guesses = [self.seed]

        self.prepare()

        retry = 0
        round = 0
        lookahead = 0
        while True:

            # append each letter in the keyspace to our current tries.
            oldguesses, guesses = guesses, []
            for guess in oldguesses:
                for letter in self.alphabet:
                    if lookahead > 0:
                        guesses.append(
                            self.guess_provider(
                                self, guess.prefix, guess.letter + letter, complement
                            )
                        )
                    else:
                        guesses.append(
                            self.guess_provider(self, str(guess), letter, complement)
                        )

            starttime = time.time()

            # testing phase
            kept = self.__run_all(guesses)

            print "In round %u, ran all %u guesses in %u seconds" % (
                round,
                len(guesses),
                time.time() - starttime,
            )

            # print repr(kept)
            if len(kept) == 0:
                print "Couldn't guess the next letter after %s" % (
                    repr([str(g) for g in oldguesses]),
                )
                if retry >= self.retries:
                    if lookahead >= self.lookaheads:
                        print "stopping after %u lookahead" % (self.lookaheads,)
                        break
                    else:
                        # when performing lookahead, do not keep the known bad guesses.
                        guesses = [guess for guess in guesses if not guess.discard()]
                        lookahead += 1
                        retry = 0
                        print "performing lookahead (%u/%u) with %u potential candidates" % (
                            lookahead,
                            self.lookaheads,
                            len(guesses),
                        )
                        continue
                else:
                    retry += 1
                    print "changing complement (%u/%u) and retrying with old guesses." % (
                        retry,
                        self.retries,
                    )
                    guesses = oldguesses
                    complement = self.prepare_complement()
                    continue
            else:
                retry = 0
                lookahead = 0

            _min = min([len(g) for g in kept])
            # print 'keeping guesses with minimal length: %u' % (_min, )

            # switch over the new guesses
            guesses = [g for g in kept if len(g) == _min]
            if len(guesses) > 0:
                print "After round #%u, kept: %s+%s" % (
                    round,
                    repr(guesses[0].prefix),
                    repr([guess.letter for guess in guesses]),
                )

            self.retreived_guesses = guesses

            if kept[0].letter == "}":
                break

            round += 1

        self.cleanup()

        return self.retreived_guesses

# Code unique to this challenge written by HHousen below this line
# `CompressionOracle.__run_all` modified to not use threading as well.
# `CompressionOracle.run` modified to break if the "}" character is found.
from pwn import *


class Client(CompressionOracle):
    def prepare(self):
        host = "mercury.picoctf.net"
        port = 50899
        io = connect(host, port)
        self.io = io
    def oracle(self, guess_data):
        # Return the length of `guess_data` after the vulnerable server has compressed it.
        for attempt in range(10):
            try:
                self.io.sendlineafter("Enter your text to be encrypted: ", guess_data)
                nonce = self.io.recvline()
                encrypted_data = self.io.recvline()
                length_data = self.io.recvline().strip()
                try:
                    length = int(length_data)
                except ValueError:
                    # If for whatever reason the length is not shown, return a high number
                    print("Non-int length: " + length_data)
                    return 999
            except EOFError:
                # Reconnect if fails to send `guess_data`
                print("Retrying connection...")
                time.sleep(0.5)
                self.prepare()
            else:
                break
        else:
            # All attempts failed
            sys.exit(1)

        return length

# Create a list of possible values for each character of the flag.
alphabet = string.ascii_lowercase + "_}{"
c = Client(seed="picoCTF", alphabet=alphabet)
c.run()
print "Flag: " + c.retreived_guesses[0].prefix + c.retreived_guesses[0].letter

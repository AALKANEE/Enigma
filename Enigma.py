class Rotor:
    def __init__(self, wiring, notch, position=0):
        """
        Initializes a rotor
        wiring: A string representing the internal wiring of the rotor
        notch: The position where the rotor causes the next rotor to rotate
        position: The current position of the rotor
        """
        self.wiring = wiring
        self.notch = notch
        self.position = position

    def encode_forward(self, c):
        """
        Encodes a character in the forward direction.
        This simulates the character passing through the rotor from right to left
        """
        index = (ord(c) - ord('A') + self.position) % 26
        return chr((ord(self.wiring[index]) - ord('A') - self.position) % 26 + ord('A'))

    def encode_backward(self, c):
        """
        Encodes a character in the backward direction.
        This simulates the character passing through the rotor from left to right
        """
        index = (self.wiring.index(chr((ord(c) - ord('A') + self.position) % 26 + ord('A'))) - self.position) % 26
        return chr(index + ord('A'))

    def rotate(self):
        """
         Rotates the rotor by one position.
        Returns True if the rotor has reached its notch position, causing the next rotor to rotate.
        """
        self.position = (self.position + 1) % 26
        return self.position == self.notch


class Reflector:
    def __init__(self, wiring):
        """
         Initializes a reflector.
         wiring: A string representing the internal wiring of the reflector.
        """
        self.wiring = wiring

    def reflect(self, c):
        """
        Reflects the character using the reflector's wiring
        """
        return self.wiring[ord(c) - ord('A')]


class Plugboard:
    def __init__(self, wiring):
        """
        Initializes the plugboard.
        wiring: A dictionary representing the letter swaps on the plugboard.
        """
        self.wiring = wiring

    def swap(self, c):
        """
        swaps the character using the plugboard settings
        """
        return self.wiring.get(c, c)


class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        """
        Initializes the Enigma machine with a set of rotors, a reflector, and a plugboard.
        rotors: A list of Rotor objects
        reflector: A Reflector object
        plugboard: A Plugboard object
        """
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def encode_letter(self, c):
        """
        Encodes a single letter using the Enigma machine.
        The letter passes through the plugboard, the rotors (forward and backward), the reflector,
        and then the plugboard again.
        """

        # Plugboard swap
        c = self.plugboard.swap(c)
        # Forward through the rotors
        for rotor in self.rotors:
            c = rotor.encode_forward(c)

        # Reflector
        c = self.reflector.reflect(c)

        # Backward through the rotors
        for rotor in reversed(self.rotors):
            c = rotor.encode_backward(c)

        # Plugboard swap
        c = self.plugboard.swap(c)

        # Rotate rotors
        for rotor in self.rotors:
            if not rotor.rotate():
                break

        return c

    def encode_message(self, message):
        """
        Encodes an entire message by encoding each letter individually.
        Only alphabetic characters are encoded; others are ignored
        """
        return ''.join(self.encode_letter(c) for c in message if c.isalpha())


# Initial settings for the Enigma machine
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16)  # Rotor I with notch at position 16 (Q)
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4)  # Rotor II with notch at position 4 (E)
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21)  # Rotor III with notch at position 21 (V)
reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")  # Reflector B
plugboard = Plugboard({'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'})  # Simple plugboard settings

#create the enigma machine
enigma= EnigmaMachine([rotor1, rotor2, rotor3],reflector,plugboard)

#get input from the postman
message = input("Enter a message to encode: ").upper()

#Encode the message
encoded_message = enigma.encode_message(message)
print(f"Encoded Message: {encoded_message}")

#ARYAN ALKANE
#FJDPPNJWJWU
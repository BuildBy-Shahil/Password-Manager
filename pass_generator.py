import random
class RandomPassword:
    @staticmethod
    def generate_random_password():
        # Returns Randomly generated Strong password
        random_password_list = []
        uppercase_letters = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

        lowercase_letters = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]

        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        symbols = [
            '!', '@', '#', '$', '%', '^', '&', '*',
            '(', ')', '-', '_', '=', '+',
            '[', ']', '{', '}', '\\', '|',
            ';', ':', "'", '"', ',', '.', '<', '>', '/', '?'
        ]

        for i in range(4):
            up_caps = random.choice(uppercase_letters)
            lo_caps = random.choice(lowercase_letters)
            num = random.choice(digits)
            symbol = random.choice(symbols)
            random_password_list.append([up_caps, lo_caps, num, symbol])

        password_list = []

        for password in random_password_list:
            for letter in password:
                # print(letter)
                password_list.append(letter)

        random.shuffle(password_list)
        strong_password = "".join(password_list)
        return strong_password
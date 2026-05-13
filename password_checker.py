import re
import random

# ============================================
# LEET SPEAK SUBSTITUTIONS
# ============================================
leet_map = {
    'a': ['@', '4'], 'b': ['8'], 'e': ['3'],
    'g': ['5'], 'i': ['!', '1'], 'o': ['0'],
    'p': ['9'], 's': ['$'], 't': ['7'],
    'l': ['1'], 'z': ['2']
}

# ============================================
# WORD BANK
# ============================================
action_words = ['eat', 'run', 'jump', 'read', 'walk', 'push', 'pull', 'hunt']
object_words = ['frog', 'hat', 'dog', 'cup', 'key', 'bat', 'box', 'car']
power_words  = ['God', 'king', 'rock', 'fire', 'iron', 'storm', 'blade', 'force']
desc_words   = ['dark', 'blue', 'cold', 'bold', 'fast', 'wild', 'deep', 'tall']

specials  = '!@#$%^&*()-+_=[]{}|;:,.<>?/~`"\'\\'
safe_nums = '23456789'
consec    = ['1234','2345','3456','4567','5678','6789','7890','0123',
             '9876','8765','7654','6543','5432','4321','3210']

# ============================================
# HELPERS
# ============================================
def apply_leet(char, intensity='high'):
    lc = char.lower()
    if lc in leet_map:
        if intensity == 'high' or random.random() > 0.5:
            return random.choice(leet_map[lc])
    return char.upper() if random.random() > 0.5 else char.lower()

def has_consec(pw):
    return any(p in pw for p in consec)

def count_upper(pw):   return len(re.findall(r'[A-Z]', pw))
def count_lower(pw):   return len(re.findall(r'[a-z]', pw))
def count_nums(pw):    return len(re.findall(r'[0-9]', pw))
def count_special(pw): return len(re.findall(r'!@#$%^&*()-+_=[]{}|;:,.<>?/~`"\'\\', pw))

def rand(lst): return random.choice(lst)

# ============================================
# CHECKS — exactly 7, matching what user sees
# ============================================
def get_checks(pw, name):
    name_in_pw = name and name.lower() in pw.lower()
    length_ok  = len(pw) >= 8

    length_label = (
        f"Length: 12+ characters (excellent)" if len(pw) >= 12
        else f"Length: 8+ characters" if len(pw) >= 8
        else f"Length: too short — minimum 8 (you have {len(pw)})"
    )

    return [
        {'ok': length_ok,            'label': length_label},
        {'ok': count_upper(pw) >= 2,   'label': f"Uppercase: 2+ letters" if count_upper(pw) >= 2 else f"Uppercase: need at least 2 (you have {count_upper(pw)})"},
        {'ok': count_lower(pw) >= 2,   'label': f"Lowercase: 2+ letters" if count_lower(pw) >= 2 else f"Lowercase: need at least 2 (you have {count_lower(pw)})"},
        {'ok': count_nums(pw) >= 2,    'label': f"Numbers: 2+ digits" if count_nums(pw) >= 2 else f"Numbers: need at least 2 (you have {count_nums(pw)})"},
        {'ok': count_special(pw) >= 2, 'label': f"Special characters: 2+" if count_special(pw) >= 2 else f"Special characters: need at least 2 (you have {count_special(pw)})"},
        {'ok': not has_consec(pw),     'label': "No consecutive number patterns" if not has_consec(pw) else "Consecutive numbers detected — avoid patterns like 1234 or 5678"},
        {'ok': not name_in_pw,         'label': f"Name not directly in password" if not name_in_pw else f"Your name '{name}' was found — easily guessable"},
    ]

def meets_all(pw, name):
    return all(c['ok'] for c in get_checks(pw, name))

# ============================================
# CHECKER
# ============================================
def check_password(pw, name=''):
    checks = get_checks(pw, name)
    score  = sum(1 for c in checks if c['ok'])
    pct    = round((score / len(checks)) * 100)

    if pct == 100: strength = "Very Strong"
    elif pct >= 70: strength = "Strong"
    elif pct >= 50: strength = "Medium"
    else:           strength = "Weak"

    print(f"\n{'='*45}")
    print(f"  Your password is {pct}% strong — {strength}")
    print(f"{'='*45}")
    for c in checks:
        icon = "✓" if c['ok'] else "✗"
        print(f"  {icon} {c['label']}")
    print(f"{'='*45}\n")
    return pct

# ============================================
# SHORT PASSWORD GENERATOR (8-13 chars)
# ============================================
def build_short_password(name):
    uppers = [c for c in 'ABCDEFGHJKMNPQRSTVWXY' if c not in name.upper()] or list('ABCDEFGHJK')
    lowers = [c for c in 'abcdefghjkmnpqrstvwxy' if c not in name.lower()] or list('abcdefghjk')

    for _ in range(300):
        parts = []
        letters = [c for c in name if c.isalpha()]
        chosen  = random.sample(letters, min(3, len(letters)))
        for c in chosen:
            parts.append(apply_leet(c, 'high'))
        parts.append(rand(uppers))
        parts.append(rand(uppers))
        parts.append(rand(lowers))
        parts.append(rand(lowers))
        parts.append(rand(list(specials)))
        parts.append(rand(list(specials)))
        n1 = rand(list(safe_nums))
        n2 = rand([n for n in safe_nums if abs(int(n) - int(n1)) > 1])
        parts.append(n1)
        parts.append(n2)
        random.shuffle(parts)
        pw = ''.join(parts)[:13]
        if meets_all(pw, name):
            return pw
    return f"X@{name[:2].upper()}!7z#9K"[:13]

# ============================================
# LONG PASSWORD GENERATOR (13-20 chars)
# ============================================
def build_long_password(name):
    for _ in range(300):
        w1  = rand(action_words + desc_words)
        w2  = rand(object_words + power_words)
        ns  = name[:4]
        w1t = ''.join(apply_leet(c, 'low') for c in w1)
        w2t = ''.join(apply_leet(c, 'low') for c in w2)
        nt  = ''.join(apply_leet(c, 'low') for c in ns)
        sep = rand(['-', '_', '=', '&', '+'])
        pw  = rand([
            f"{w1t}{sep}{nt}{sep}{w2t}",
            f"{nt}{sep}{w1t}{sep}{w2t}",
            f"{w2t}{sep}{nt}{sep}{w1t}"
        ])[:20]
        if count_nums(pw) < 2:
            pw = (pw + rand(list(safe_nums)) + rand(list(safe_nums)))[:20]
        if count_special(pw) < 2:
            pw = (pw + rand(list('!@#$')) + rand(list('!@#$')))[:20]
        if count_upper(pw) < 2:
            pw = (pw + rand(list('ABCDEFGHJK')) + rand(list('ABCDEFGHJK')))[:20]
        if meets_all(pw, name):
            return pw
    return f"{name[:3]}-R0ck&F1re-99"[:20]

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print("=" * 45)
    print("      🔐 PASSWORD STRENGTH CHECKER 🔐")
    print("=" * 45)

    username = input("\nEnter your name: ").strip()
    print(f"\nHello {username}! Let's check or generate your password.\n")

    use_short = True

    while True:
        print("What would you like to do?")
        print("  1. Check my own password")
        print("  2. Generate a strong password")
        print("  3. Exit")

        choice = input("\nChoose (1, 2 or 3): ").strip()

        if choice == '1':
            pw = input("\nEnter your password: ")
            check_password(pw, username)

        elif choice == '2':
            while True:
                print("\nGenerating your password...")
                if use_short:
                    pw    = build_short_password(username)
                    style = "Short & complex (8-13 characters)"
                else:
                    pw    = build_long_password(username)
                    style = "Long & memorable (13-20 characters)"

                print(f"\nGenerated password ({style}):\n  {pw}")
                check_password(pw, username)

                again = input("Generate another one? (yes/no): ").strip().lower()
                if again == 'yes':
                    use_short = not use_short
                else:
                    print(f"\nYour final password: {pw}")
                    print("Save it somewhere safe!\n")
                    break

        elif choice == '3':
            print(f"\nGoodbye {username}! Stay secure! 🔐\n")
            break

        else:
            print("\nInvalid option. Please choose 1, 2 or 3.\n")
import re
back = "[uúoóaá]"
front = "[üöõû]"
neutral = "[ieíé]"
consonants = "[pbtdgkfvszcmnlrjhyx]"
def assignClass(stem):
    #Vowel classes:
    # B: ends with a back vowel
    # F: ends with a front vowel
    # FN: front, followed by any number of neutral vowels
    # N: one neutral vowel, no other vowels
    # NN: two neutral vowels, no other vowels
    # NNN: more than two neutral vowels, no other vowels
    # BN: back, followed by neutral
    # BNN: back, followed by two neutrals

    if re.match(".*"+back+consonants+"*$",stem):
        return "B"
    elif re.match(".*"+front+consonants+"*$",stem):
        return "F"
    elif re.match(".*"+neutral+consonants+"*$",stem):
        if re.match(".*"+front,stem):
            return "FN"
        elif re.match(".*"+back+consonants+"*"+neutral+consonants+"*$",stem):
            if re.match(".*e"+consonants+"*$",stem):
                return "BE"
            elif re.match(".*é"+consonants+"*$",stem):
                return "Be"
            else:
                return "Bi"

        elif re.match(".*"+back+consonants+"*"+neutral+consonants+"*"+neutral+consonants+"*$",stem):
            if re.match(".*e"+consonants+"*$",stem):
                return "BNE"
            elif re.match(".*é"+consonants+"*$",stem):
                return "BNe"
            else:
                return "BNi"

        elif re.match(".*"+back,stem):
            return "BNNN"
        elif re.match(".*"+neutral+consonants+"*"+neutral+consonants+"*"+neutral+consonants+"*$",stem):
            return "NNN"
        elif re.match(".*"+neutral+consonants+"*"+neutral+consonants+"*$",stem):
            return "NN"
        else:
            return "N"
    else:
        return stem
    
annotation = []    
with open("Hungarian_corpus_fortagging","r") as f:
    lines = f.readlines()
    for l in lines:
        print(l.strip())
        print(assignClass(l.strip()))
        annotation.append([l.strip(),assignClass(l.strip())])
        
with open ("Hungarian_corpus_annotated","w") as f:
    for l in annotation:
        f.write("\n")
        f.write("\t".join(l))
        
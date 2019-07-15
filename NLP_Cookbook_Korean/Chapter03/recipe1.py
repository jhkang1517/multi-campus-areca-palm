from nltk.tokenize import LineTokenizer, SpaceTokenizer, TweetTokenizer
from nltk import word_tokenize

lTokenizer = LineTokenizer();
print("Line tokenizer 출력 : ", lTokenizer.tokenize("My name is Maximus Decimus Meridius, commander of the Armies of the North, General of the Felix Legions and loyal servant to the true emperor, Marcus Aurelius.\nFather to a murdered son, husband to a murdered wife. \nAnd I will have my vengeance, in this life or the next."))

rawText = "By 11 o'clock on Sunday, the doctor shall open the dispensary."
sTokenizer = SpaceTokenizer()
print("Space Tokenizer 출력 :", sTokenizer.tokenize(rawText))

print("Word Tokenizer 출력 : ", word_tokenize(rawText))

tTokenizer = TweetTokenizer()
print("Tweet Tokenizer 출력 : ", tTokenizer.tokenize("This is a cooool #dummysmiley: :-) :-P <3"))
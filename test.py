from translate import Translator

# Create a Translator object specifying the source and destination languages
translator = Translator(from_lang="english", to_lang="arabic")

# Define the text to be translated
text_to_translate = "  So you're running a little late today. And you haven't had your fresh cup of coffee yet. No matter the weather or traffic, you can't just have fresh coffee and bagels. The Java Cafe."

# Perform the translation
translation = translator.translate(text_to_translate)

# Print the translated text
print(translation)

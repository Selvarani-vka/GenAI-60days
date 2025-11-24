from langchain_community.document_loaders import TextLoader
text_loc=TextLoader("Newdoc.txt")
text_load1=text_loc.load()
print(text_load1)



import re
import os
from nltk import sent_tokenize

# For NER
import spacy
nlp = spacy.load('en_core_web_sm')

def sortedByValue( dict ):
    return sorted( dict , key=lambda x: dict[x])

dir = 'TXT'

csv = open( 'quotations.csv' , 'w' , encoding = 'utf-8' )

for txt in os.listdir(dir):

    quotations = []
    if re.search( r'txt$' , txt ):
        print( txt )
        year = re.split( r'_' , txt )[0]
        print(year)
        with open( os.path.join( dir, txt ) , encoding = 'utf-8' ) as fh:
            full_text = fh.read()
            sentences = sent_tokenize(full_text)
            for s in sentences:
                if re.search( r'sovereign' , s , re.IGNORECASE ):
                    quotations.append( re.sub( r',' , '' , s ) )

            if len(quotations) > 0:
                start = sentences[:15]
                NER = dict()
                for s in start:
                    tagged_text = nlp(s)
                    for named_entity in tagged_text.ents:
                        if named_entity.label_ == 'GPE' and not( re.search( r'new york' , str(named_entity) , re.IGNORECASE )):
                            key = str( named_entity).strip()
                            NER[ key ] = NER.get( key , 0) + 1

                if len(NER) > 0:
                    country = sortedByValue(NER)[0]
                else:
                    country = 'Unknown'

            for q in quotations:
                csv.write( f'{txt},{q},y_{year},ctry_{country}\n' )

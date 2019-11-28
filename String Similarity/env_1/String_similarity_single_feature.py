import codecs, difflib, Levenshtein, distance

"""
the performance of the string metrics is not very good, has the risk of not identifying
the different addresses, especially the addresses is very similiar
so I think we can try combine the address with city and country
"""


a_text = "151 cambridge terrace"
b_text = "9 mckerrow place"
c_text = "151 cambridge Street"
#  if met abbreviation situation, we can use Semantics and syntax analysis
e_text = "New Zealand"
f_text = "NZ"



diff1 = difflib.SequenceMatcher(a_text.lower(),b_text.lower()).ratio()
lev1 = Levenshtein.ratio(a_text.lower(),b_text.lower())
sor1 = 1 - distance.sorensen(a_text.lower(),b_text.lower())
jac1 = 1 - distance.jaccard(a_text.lower(),b_text.lower())

print("text a VS text b: ")
print("diff",diff1)
print("lev",lev1)
print("sor",sor1)
print("jac",jac1)

diff2 = difflib.SequenceMatcher(a_text.lower(),c_text.lower()).ratio()
lev2 = Levenshtein.ratio(a_text.lower(),c_text.lower())
sor2 = 1 - distance.sorensen(a_text.lower(),c_text.lower())
jac2 = 1 - distance.jaccard(a_text.lower(),c_text.lower())

print("text a VS text c: ")
print("diff",diff2)
print("lev",lev2)
print("sor",sor2)
print("jac",jac2)


diff3 = difflib.SequenceMatcher(e_text.lower(),f_text.lower()).ratio()
lev3 = Levenshtein.ratio(e_text.lower(),f_text.lower())
sor3 = 1 - distance.sorensen(e_text.lower(),f_text.lower())
jac3 = 1 - distance.jaccard(e_text.lower(),f_text.lower())

print("text a VS text c: ")
print("diff",diff3)
print("lev",lev3)
print("sor",sor3)
print("jac",jac3)

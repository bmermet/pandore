Required :

django-haystack : 'pip install -e git+https://github.com/toastdriven/django-haystack.git@master#egg=django-haystack'
solr - infos for install : http://django-haystack.readthedocs.org/en/latest/installing_search_engines.html
>> but solr 3.5 doesn't exist anymore, dl 3.6.1 instead

Need to put the output of './manage.py build_solr_schema' in the conf directory of solr
/!\ In the conf directory of solr, do : 'cp lang/stopwords_en.txt ./' (because our solr version will be too new)

Run again the './manage.py build_solr_schema > schema.xml' and put the output in the conf directory.

Create the index with './manage.py rebuild_index'

And then it should work :)

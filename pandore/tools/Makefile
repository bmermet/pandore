.PHONY : testdir

start :
	python2 manage.py runserver

schema :
	python2 manage.py build_solr_schema > schema.xml
	mv schema.xml ../apache-solr-3.6.1/example/solr/conf/
	python2 manage.py rebuild_index

solr :
	java -jar ../apache-solr-3.6.1/example/start.jar

testdir:
	rm -rf testdir
	-mkdir testdir
	-cd testdir && head -10 ../list | xargs mkdir

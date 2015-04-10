# citation-washer

A grimy little Python script to impose uniformity and nice formatting on your BibTex references querying Google Scholar. 

This is useful because you'll often get citations from a variety of sources, each of which will in general have slightly different capitalization and mechanics. 

You could fix them by hand, but that would be boring. 

So this program searches Google scholar by title, author, and year, and then replaces your old dirty BibTex with clean, uniform, GScholar-style Bibtex.

Google Scholar does not have a public API, so we have to rely on third-party scraping tools :(

Characterizing the reliability and desireability of this approach is left as an exercise for the reader. 

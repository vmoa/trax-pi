# Static Files

The directory contains static files, both those intended to be served
by flask under `/static` and as a holding place for other files.  The
`java.png` file, for instance, is a snapshot of the old Java interface
for reference.

## Notes on index.html

The file `index.html` is a static launcher page to open T-Rax and set
the window size. For now it is served by Apache so copy it to docroot:

```
sudo cp index.html /var/www/html/
```

Best practices have Flask sitting behind a WCGI server rather than
serving directly. That could change how to install this file, but
that's a future enhancement.

Fluttr CLI
==========

This project is a small library written in python for interacting with the
[fluttrly](http://fluttrly.com) service.  Also provided is a program
designed to act as a command line interface to this library.  The library could
be used to write other python programs that interact with fluttrly, or for
small scripting jobs for manipulating fluttrly lists.  

The CLI client is designed to take a fluttrly list as its first argument, and
some subcommand as the second argument.  Omitting the subcommand will display
the list.  The subcommands include add, rm, and toggle.  Here is an example of
how to interact with the CLI:

     bensonk@localhost $ ./fluttr.py fluttr-cli     
     Nothing to do!
     bensonk@localhost $ ./fluttr.py fluttr-cli add Write more documentation
     1) [ ] Write more documentation
     bensonk@localhost $ ./fluttr.py fluttr-cli add Help an old lady across the street
     1) [ ] Help an old lady across the street
     2) [ ] Write more documentation
     bensonk@localhost $ ./fluttr.py fluttr-cli add Change the oil
     1) [ ] Change the oil
     2) [ ] Help an old lady across the street
     3) [ ] Write more documentation
     bensonk@localhost $ ./fluttr.py fluttr-cli toggle 3
     1) [ ] Change the oil
     2) [ ] Help an old lady across the street
     3) [X] Write more documentation
     bensonk@localhost $ ./fluttr.py fluttr-cli rm 2
     1) [ ] Change the oil
     2) [X] Write more documentation

Bug reports, feature requests, and especially patches are welcome. :-)

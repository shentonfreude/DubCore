=========
 DubCore
=========

Sample application using Repoze.BFG with the colander/deform schema
and form libraires. Mainly a learning tool, but some of the exercises
here may point out issues with the schema/form libraries.

The idea is a simple CMS-like app with Dublin Core (DC) metadata attached
to content types.

Pages
=====

Currenly, there's a top-level Pages content type, and under it you may
create Page objects.  Page objects have a 'data' body and DC metadata
including Title, Description, and Date. Content is stored in the ZODB,
which is pleasantly easy to use and transparent.

More Content Types
==================

It should be easy to add common objects like Folder (at which point we
get hierarchies), File, Image, Link, etc.

Search
======

Search should be implemented.

Relation to Actual Stuff
========================

This came out of a sprint to build a CMS framework on top of
Repoze.BFG, Colander, Deform, etc. Configuration of schemas, content,
workflow, etc is to be done declaratively by YAML so it should lower
the barrier to entry for use.

http://svn.repoze.org/reward/






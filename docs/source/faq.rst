FAQ
===

I received an empty result from Merlin.
 No data was received from the source.  Adjust x, y, and acquired parameters and verify the Chipmunk instance located at CHIPMUNK_URL has data.

Merlin issued a symmetric data error.
 This means that there are missing observations from one or more data layers.  The data layers should be checked at the source for the given location.  This is a built-in QA check on the data which may be replaced by injecting a new ```date_fn``` into the Merlin profile.

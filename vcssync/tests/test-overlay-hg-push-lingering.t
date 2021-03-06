#require hg41+

  $ . $TESTDIR/vcssync/tests/helpers.sh
  $ standardoverlayenv > /dev/null 2>&1

Leave overlayed changesets in local repo then attempt to push in a later
invocation. This simulates failure to push on a previous run.

  $ overlay-hg-repos http://localhost:$HGPORT/overlay-source http://localhost:$HGPORT/overlay-dest \
  >   repo --into subdir >/dev/null 2>&1

  $ overlay-hg-repos http://localhost:$HGPORT/overlay-source http://localhost:$HGPORT/overlay-dest \
  >   repo --into subdir --result-push-url http://localhost:$HGPORT/overlay-dest
  executing: hg strip --no-backup -r 'not public()'
  resolving destination revision: tip
  executing: hg identify http://localhost:$HGPORT/overlay-dest -r tip
  hg> 88dd2a5005e6
  commencing overlay of http://localhost:$HGPORT/overlay-source
  executing: hg overlay http://localhost:$HGPORT/overlay-source --into subdir -d 88dd2a5005e6e795674d8253cec4dde9f9f77457
  hg> 76f0fc85e215 -> 67c9543981c6: initial - add source-file0 and source-file1
  hg> d92cc0ff6f1a -> eaf64eb11964: add dir0/file0
  2 new changesets; new tip is eaf64eb119642ef85b4d952a49d0f5c815d5bcd1
  pushing 2 new changesets on head eaf64eb119642ef85b4d952a49d0f5c815d5bcd1 to http://localhost:$HGPORT/overlay-dest
  1:67c9543981c6: initial - add source-file0 and source-file1
  2:eaf64eb11964: add dir0/file0
  executing: hg push -r eaf64eb119642ef85b4d952a49d0f5c815d5bcd1 http://localhost:$HGPORT/overlay-dest
  hg> pushing to http://localhost:$HGPORT/overlay-dest
  hg> searching for changes
  hg> remote: adding changesets
  hg> remote: adding manifests
  hg> remote: adding file changes
  hg> remote: added 2 changesets with 3 changes to 3 files

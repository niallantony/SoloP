# SOLOP 1.1.0

## BACKLOG:

- [1]: Supress unpassed arguments - refactor
- [18]: Add argparse options for more detailed help
- [19]: Timestamps for tasks
- [37]: TEST: parentless task visibility
- [39]: TEST: validations
- [2]: Implement milestones
- [3]: Implement versioning/releases
- [5]: Add git commit hooks
- [11]: Add config file for priority labels
- [12]: Add config file for visibility options
- [13]: Add recommended next task
- [15]: Make interactive client
- [20]: Feature wishlists
- [22]: Highlighting critical tasks/bottlenecks
- [26]: TEST: Tests for pull
	- [29]: Test multiple children
	- [28]: Test multiple parents
	- [27]: Test nested tasks pull
- [30]: Pull duplicate items (when sharing parents) (Perhaps something like a merge conflict)
- [31]: Merge pulled list with existing
- [32]: TEST: list_parser.p
- [14]: BUG: can't work with broken json file (e.g. tasks:{} <- is dict/not list
- [6]: Git branch hook for in progress
- [7]: Add timestamps
- [8]: Add metrics (e.g. 'Done Today...')
- [9]: Add archiving
- [10]: Allow importing
- [16]: Improve MD doc formatting
	- [25]: Decorators for TEST BUG etc
- [17]: Implement dependencies
- [21]: Progress markers?
- [23]: Warning for too many tasks in progress (configurable in progress cap?)
- [24]: BUG:CLI catching of InvalidTaskError
- [33]: CLI for altering future attributes of tasks (dependencies, notes, etc...)
- [34]: TEST: unnesting tasks which are present in children - but have no parent
- [36]: Make interactive client
- [49]: Generate package
- [50]: TEST: CLI interface commands
- [60]: Test Merger and ListParser fully

## IN PROGRESS:


## DONE:

- [35]: TEST: swapping children
- [38]: Test --xmake
- [4]: Implement PULL from MD command
- [40]: Implement nested tasks
- [41]: Implement in_progress and done sections
- [42]: Implement custom headers
- [43]: Implement priority levels
- [44]: TEST: Fix new-line error in task
- [45]: Throw meaningful exceptions for mismatched arguments - CLI
- [46]: Parse CLI args in a more loosely coupled way
- [47]: Sort section headings in meaningful way (in progress not after Done etc...)
- [48]: BUG: case sensitivity in status messages
- [51]: CLI interface accepts multiple arguments
- [52]: Refactor MD sections as objects to allow easier nesting
- [53]: BUG: duplicate IDs? (Problem with nesting?)
- [54]: Add un-child action
- [55]: Add guards against duplicate IDs
- [56]: BUG: Nested tasks in different sections
- [57]: TEST: unchild action
- [58]: Delete task, move children to new parent
- [59]: Add confirmation for deletion

( This document was generated with SoloP )
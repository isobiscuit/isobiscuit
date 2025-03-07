
# IsoBiscuit
IsoBiscuit is a tool for visualizing processes etc. where these are stored in "biscuits". This works with sectors, so that the memory can be loaded and initialized before executing the .biscuit.

## Installation
You can install isobiscuit with pip \
`pip install isobiscuit`

## Create Biscuits
You can create your biscuit with \
`biscuit init mybiscuit`

## Build Biscuit
You can build a biscuit to a .biscuit with
`biscuit build mybiscuit`

## Run a biscuit
You got now an `.biscuit`, now you can run your `any_dot_biscuit_file.biscuit` with\
`biscuit run any_dot_biscuit_file`\
you have to write it without `.biscuit`

## Links
### [BBin Format](./bbin.md)
### [The Biscuit File Format](./biscuit-file-format.md)
### [Biscuit Calls](./biscuit_calls.md)
### [Biscuit Assembly](./biasm.md)
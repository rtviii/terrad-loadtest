-⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯

 Grabbing metrics from sysstat:

  - [ ]  memory consumption
    - Brendan gregg's  `sar`
  - [ ]  network bandwidth
    - some `iftop` like summary
  - [ ]  file size transferred
  - [ ]  swap space barely seems to budge. no pageouts

 Should probably test scenarios on the spectrum from:
  - few users making many heavy requests | avg users making avg requests | many users making few/light requests
    - doesn't make much sense in the context where all requests are similar
  - short bursts | build-teardown stages | semi-lenghty saturation scenario
    (high load for ~10 min)


# The given

- the server is testnet
- few testnet endpoints alternative to the mainnet's most popular ones

# General observations

- the processes seems cpu bound
    - means heavier machines can process more/sec (at least up to some
      threshold)
    - also probably means that this analysis is not super representative.
      16GB/4CPUs

- yet swap memory barely budges, no page-ins even with highest load
    Hence, without any smattering of idea about how the core works -- wondering
    if it makes sense to cache the recent blocks
- read/writes seem minimal via `iostat`

# Bad

- we don't much data-heavy stuff

